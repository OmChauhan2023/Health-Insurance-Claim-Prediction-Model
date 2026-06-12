import json
import os
import hashlib
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import google.generativeai as genai

router = APIRouter()

# Configure standard Gemini API (Requires GOOGLE_API_KEY env var)
# genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

class PredictRequest(BaseModel):
    features: dict

class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []

@router.post("/predict")
def predict_claim(request: PredictRequest):
    """
    Mock prediction endpoint.
    Since the base models (LightGBM, XGBoost, CatBoost) were not saved in the outputs
    directory during training, we simulate a prediction based on feature hash.
    In production, this would load the models and run `model.predict_proba()`.
    """
    # Deterministic mock probability based on input features
    features_str = str(sorted(request.features.items()))
    hash_val = int(hashlib.md5(features_str.encode()).hexdigest(), 16)
    mock_prob = (hash_val % 10000) / 10000.0
    
    return {
        "status": "success",
        "probability": mock_prob,
        "risk_level": "High" if mock_prob > 0.7 else "Medium" if mock_prob > 0.4 else "Low",
        "note": "Mocked prediction (models not saved in outputs)"
    }

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Standard Gemini streaming endpoint for AI Chat.
    """
    # In a real app, you would pass the context of the CSV data here.
    system_prompt = (
        "You are a Health Insurance Data Analyst assistant. "
        "Your role is to help users understand the claim prediction model and its features. "
        "Provide insights on what factors might lead to high risk claims."
    )
    
    def event_generator():
        try:
            # Note: We are simulating a streaming response since API key might not be set
            # In production:
            # model = genai.GenerativeModel('gemini-pro')
            # response = model.generate_content(system_prompt + request.message, stream=True)
            # for chunk in response: ...
            
            # Simulated Thought Process
            yield f"data: {json.dumps({'type': 'THOUGHT', 'content': 'Analyzing the user request...'})}\n\n"
            yield f"data: {json.dumps({'type': 'THOUGHT', 'content': 'Checking the model metrics and parameters...'})}\n\n"
            
            # Simulated Final Response
            response_text = f"Based on the insurance data model, the key features driving claim risk are typically age, BMI, and medical history. You asked: '{request.message}'. I recommend looking into feature importance charts to see the exact impact."
            
            for word in response_text.split(" "):
                yield f"data: {json.dumps({'type': 'FINAL_RESPONSE', 'content': word + ' '})}\n\n"
            
            # Simulated Suggestions
            yield f"data: {json.dumps({'type': 'SUGGESTION', 'content': 'Show feature importance'})}\n\n"
            yield f"data: {json.dumps({'type': 'SUGGESTION', 'content': 'Explain model Gini score'})}\n\n"
            
            yield "data: [DONE]\n\n"
        except Exception as e:
            error_dict = {"type": "FINAL_RESPONSE", "content": f"\n\n**API Error**: {str(e)}"}
            yield f"data: {json.dumps(error_dict)}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
