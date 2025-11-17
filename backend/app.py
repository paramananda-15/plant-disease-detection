# backend/app.py - ENHANCED WITH PRODUCT RECOMMENDATIONS
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
from pathlib import Path
from predict import (
    predict_image, predict_top_k, get_products,
    get_disease_info, get_treatment_advice, CLASS_NAMES
)

app = FastAPI(
    title="PlantVillage Disease Detection & Product Recommendation API",
    version="2.0.0",
    description="AI-powered plant disease detection with treatment product recommendations"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def root():
    return {
        "service": "PlantVillage Disease Detection & Product Recommendation",
        "version": "2.0.0",
        "classes": len(CLASS_NAMES),
        "features": ["Disease Detection", "Product Recommendations", "Treatment Advice"]
    }


@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": True}


@app.get("/classes")
def get_classes():
    return {"classes": CLASS_NAMES, "total": len(CLASS_NAMES)}


@app.post("/predict")
async def predict(image: UploadFile = File(...)):
    """
    Predict plant disease and get product recommendations
    """
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    file_path = UPLOAD_DIR / image.filename
    try:
        # Save uploaded image
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # Predict disease
        label, confidence = predict_image(str(file_path))
        top_3 = predict_top_k(str(file_path), k=3)

        # Get disease information
        disease_info = get_disease_info(label)

        # Get product recommendations
        products = get_products(label)

        # Get treatment advice
        treatment = get_treatment_advice(label)

        return JSONResponse(content={
            "success": True,
            "prediction": {
                "label": label,
                "display_name": label.replace("___", " - ").replace("_", " "),
                "confidence": round(confidence, 4),
                "top_3": [
                    {
                        "label": lbl,
                        "display_name": lbl.replace("___", " - ").replace("_", " "),
                        "confidence": round(conf, 4)
                    }
                    for lbl, conf in top_3
                ]
            },
            "disease_info": disease_info,
            "products": products,
            "treatment_advice": treatment,
            "filename": image.filename
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    finally:
        if file_path.exists():
            file_path.unlink()


@app.get("/products/{disease_name}")
def get_disease_products(disease_name: str):
    """Get products for a specific disease"""
    products = get_products(disease_name)
    if not products:
        raise HTTPException(status_code=404, detail="Disease not found or no products available")
    return {"disease": disease_name, "products": products}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
