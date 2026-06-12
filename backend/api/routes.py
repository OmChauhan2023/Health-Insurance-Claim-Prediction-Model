import json
import os
import hashlib
from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv

router = APIRouter()

# ─────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────
BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent
PLOTS_DIR = PROJECT_ROOT / "outputs" / "plots"

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
- Pipeline: ZebraFeatureEngineer → ZebraImputer → 5-Fold Stratified CV → OOF Target Encoding (smoothing=10) → SMOTE+undersampling (0.05/0.30) → Feature Selection (top 65%) → 3 base models (LightGBM, XGBoost, CatBoost) → LightGBM meta-learner stacking → Isotonic Calibration.
- Results: OOF Gini = 0.8420 | AUC = 0.9210 (calibrated stacking).
- Base model OOF Ginis: LightGBM 0.793, XGBoost 0.812, CatBoost 0.778.
- Blend weights for ensemble: LightGBM 28.1%, XGBoost 53.9%, CatBoost 18.0%.

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
# /api/predict
# ─────────────────────────────────────────────
@router.post("/predict")
def predict_claim(request: PredictRequest):
    features_str = str(sorted(request.features.items()))
    hash_val = int(hashlib.md5(features_str.encode()).hexdigest(), 16)
    mock_prob = (hash_val % 10000) / 10000.0
    return {
        "status": "success",
        "probability": mock_prob,
        "risk_level": "High" if mock_prob > 0.7 else "Medium" if mock_prob > 0.4 else "Low",
        "note": "Deterministic mock (base models not persisted during training).",
    }


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
                model="gemini-2.0-flash",
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
