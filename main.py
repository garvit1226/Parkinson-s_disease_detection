from pathlib import Path
import joblib
import numpy as np
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"

MODEL_PATH = MODEL_DIR / "svm_model.pkl"
SCALER_PATH = MODEL_DIR / "scaler.pkl"

app = FastAPI(title="Parkinson's Disease Detection")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

model = None
scaler = None
load_error = None

try:
    if MODEL_PATH.exists() and SCALER_PATH.exists():
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
    else:
        load_error = "Model files not found. Add svm_model.pkl and scaler.pkl to the model folder."
except Exception as exc:
    load_error = f"Could not load model files: {exc}"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "model_ready": model is not None and scaler is not None,
            "load_error": load_error,
        },
    )


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "model_loaded": model is not None and scaler is not None,
        "message": load_error or "SVM model and scaler are ready.",
    }


@app.post("/api/predict")
async def predict(payload: dict):
    if model is None or scaler is None:
        return {
            "success": False,
            "error": load_error or "Model is not loaded."
        }

    try:
        # IMPORTANT:
        # The frontend must send features in EXACTLY the same order
        # used when training the SVM.
        values = payload.get("features")

        if not isinstance(values, list) or len(values) != 22:
            return {
                "success": False,
                "error": "Please provide exactly 22 feature values."
            }

        X = np.asarray(values, dtype=float).reshape(1, -1)
        X_scaled = scaler.transform(X)

        prediction = int(model.predict(X_scaled)[0])

        confidence = None
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(X_scaled)[0]
            confidence = round(float(np.max(probabilities)) * 100, 2)

        return {
            "success": True,
            "prediction": prediction,
            "result": "Parkinson's Positive" if prediction == 1 else "Parkinson's Negative",
            "confidence": confidence,
        }

    except Exception as exc:
        return {
            "success": False,
            "error": str(exc)
        }
