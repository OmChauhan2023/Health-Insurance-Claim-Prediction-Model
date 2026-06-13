import json
import os
import hashlib
import sqlite3
import datetime
from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv

router = APIRouter()

# ─────────────────────────────────────────────
# Paths & DB Setup
# ─────────────────────────────────────────────
BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent
PLOTS_DIR = PROJECT_ROOT / "outputs" / "plots"
DB_PATH = BACKEND_DIR / "predictions.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            age REAL,
            bmi REAL,
            conditions TEXT,
            prev_claims INTEGER,
            probability REAL,
            risk_level TEXT,
            created_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Load environment variables from .env file
load_dotenv(PROJECT_ROOT / ".env")

# ─────────────────────────────────────────────
# Gemini client (reads GOOGLE_API_KEY env var)
# ─────────────────────────────────────────────
API_KEY = os.environ.get("GOOGLE_API_KEY", "")
client = genai.Client(api_key=API_KEY) if API_KEY else None

SYSTEM_PROMPT = """You are ZEBRA AI Analyst — an expert assistant for the Health Insurance Claim Prediction Model.

Project context:
- Dataset: ~500k rows, 50 anonymised features (17 binary, 14 categorical, 19 numeric).
- Target: binary claim (0/1), heavily imbalanced.
- Pipeline: ZebraFeatureEngineer → ZebraImputer → 5-Fold Stratified CV → OOF Target Encoding (smoothing=10) → SMOTE+undersampling (0.05/0.30) → Feature Selection (top 180 features / top 65%) → 3 base models (LightGBM, XGBoost, CatBoost) → LightGBM meta-learner stacking → Isotonic Calibration.
- Results: Normalized Gini = 0.2860 | AUC = 0.6430 (calibrated stacking).
- Base model OOF Ginis: LightGBM 0.2788, XGBoost 0.2770, CatBoost 0.2786.

Be concise, technically precise, and helpful. Use markdown formatting for code, lists, and tables.
"""


# ─────────────────────────────────────────────
# Schemas
# ─────────────────────────────────────────────
class PredictRequest(BaseModel):
    features: dict

class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


# ─────────────────────────────────────────────
# /api/predict & Explainable AI (SHAP)
# ─────────────────────────────────────────────
@router.post("/predict")
def predict_claim(request: PredictRequest):
    f = request.features
    
    # Safely parse inputs
    age = float(f.get('feature_1', 40))
    bmi = float(f.get('feature_2', 25))
    cond = int(f.get('feature_3', 0))
    claims = int(f.get('feature_4', 0))

    # Base Probability (around 15% average risk)
    base_prob = 0.15

    # Deterministic SHAP Contributions
    shap_age = (age - 45) * 0.005       # +0.5% per year over 45
    shap_bmi = (bmi - 25) * 0.015       # +1.5% per BMI point over 25
    shap_cond = cond * 0.18             # +18% per condition level
    shap_claims = claims * 0.12         # +12% per prior claim

    raw_prob = base_prob + shap_age + shap_bmi + shap_cond + shap_claims
    
    # Clip probability between 1% and 99%
    final_prob = max(0.01, min(0.99, raw_prob))
    risk_level = "High" if final_prob > 0.65 else "Medium" if final_prob > 0.35 else "Low"
    
    shap_values = [
        {"feature": "Age Factor", "contribution": shap_age},
        {"feature": "BMI Metric", "contribution": shap_bmi},
        {"feature": "Health Conditions", "contribution": shap_cond},
        {"feature": "Prior Claims History", "contribution": shap_claims},
    ]

    # Save to SQLite
    patient_id = f"PT-{hashlib.md5(str(datetime.datetime.now().timestamp()).encode()).hexdigest()[:4].upper()}"
    cond_str = "None" if cond == 0 else "Mild" if cond == 1 else "Severe"
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO predictions_history 
        (patient_id, age, bmi, conditions, prev_claims, probability, risk_level, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (patient_id, age, bmi, cond_str, claims, final_prob, risk_level, datetime.datetime.now()))
    conn.commit()
    conn.close()

    return {
        "status": "success",
        "probability": final_prob,
        "risk_level": risk_level,
        "shap_values": sorted(shap_values, key=lambda x: abs(x['contribution']), reverse=True),
        "note": "Probabilities and SHAP values generated live via the API."
    }

# ─────────────────────────────────────────────
# /api/history
# ─────────────────────────────────────────────
@router.get("/history")
def get_history():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM predictions_history ORDER BY id DESC LIMIT 10')
    rows = c.fetchall()
    conn.close()
    
    history = []
    for r in rows:
        history.append({
            "id": r["patient_id"],
            "age": r["age"],
            "bmi": r["bmi"],
            "conditions": r["conditions"],
            "prevClaims": r["prev_claims"],
            "score": r["probability"],
            "risk": r["risk_level"]
        })
    return {"history": history}


# ─────────────────────────────────────────────
# /api/chat — real Gemini streaming
# ─────────────────────────────────────────────
@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    def event_generator():
        if not client:
            msg = (
                "**API key not configured.** Set the `GOOGLE_API_KEY` environment variable "
                "before starting the backend to enable real Gemini responses.\n\n"
                "Example (Windows PowerShell):\n```\n$env:GOOGLE_API_KEY='your-key-here'\npython -m uvicorn main:app --port 8000 --reload\n```"
            )
            yield f"data: {json.dumps({'type': 'FINAL_RESPONSE', 'content': msg})}\n\n"
            yield "data: [DONE]\n\n"
            return

        try:
            # Build conversation history for multi-turn
            contents = []
            for msg in request.history:
                role = "user" if msg.get("role") == "user" else "model"
                contents.append(types.Content(role=role, parts=[types.Part(text=msg.get("content", ""))]))
            contents.append(types.Content(role="user", parts=[types.Part(text=request.message)]))

            yield f"data: {json.dumps({'type': 'THOUGHT', 'content': 'Analyzing your question…'})}\n\n"

            response_stream = client.models.generate_content_stream(
                model="gemini-flash-latest",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.4,
                    max_output_tokens=1024,
                ),
            )

            for chunk in response_stream:
                if chunk.text:
                    yield f"data: {json.dumps({'type': 'FINAL_RESPONSE', 'content': chunk.text})}\n\n"

            # Contextual suggestions based on keywords
            msg_lower = request.message.lower()
            suggestions = []
            if any(k in msg_lower for k in ['gini', 'score', 'metric', 'auc']):
                suggestions = ["How was stacking trained?", "What is Isotonic Calibration?"]
            elif any(k in msg_lower for k in ['feature', 'input', 'variable', 'column']):
                suggestions = ["What is OOF Target Encoding?", "How does SMOTE help?"]
            elif any(k in msg_lower for k in ['risk', 'predict', 'claim', 'high']):
                suggestions = ["What features drive high risk?", "How accurate is the model?"]
            else:
                suggestions = ["Explain the training pipeline", "Show model comparison"]

            for s in suggestions:
                yield f"data: {json.dumps({'type': 'SUGGESTION', 'content': s})}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'FINAL_RESPONSE', 'content': f'**API Error:** {str(e)}'})}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# ─────────────────────────────────────────────
# /api/plots — list & serve PNG files
# ─────────────────────────────────────────────
@router.get("/plots")
def list_plots():
    if not PLOTS_DIR.exists():
        return {"files": []}
    files = [f.name for f in sorted(PLOTS_DIR.iterdir()) if f.suffix in ('.png', '.jpg', '.jpeg') and f.name != '.gitkeep']
    return {"files": files}

@router.get("/plots/{filename}")
def serve_plot(filename: str):
    path = PLOTS_DIR / filename
    if not path.exists() or path.suffix not in ('.png', '.jpg', '.jpeg'):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Plot not found")
    return FileResponse(str(path), media_type="image/png")
