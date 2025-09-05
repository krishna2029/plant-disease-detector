from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np
from typing import List
import logging

from models.disease_detector import DiseaseDetector
from utils.image_processor import ImageProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Plant Disease Detector API",
    description="API for detecting diseases in plant leaves using machine learning",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
disease_detector = DiseaseDetector()
image_processor = ImageProcessor()

@app.on_event("startup")
async def startup_event():
    """Initialize the ML model on startup"""
    try:
        await disease_detector.load_model()
        logger.info("Disease detection model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Plant Disease Detector API is running"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "model_loaded": disease_detector.is_loaded(),
        "version": "1.0.0"
    }

@app.post("/api/detect")
async def detect_disease(file: UploadFile = File(...)):
    """
    Detect plant disease from uploaded image
    
    Args:
        file: Uploaded image file
        
    Returns:
        JSON response with detection results
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="File must be an image"
            )
        
        # Read and process image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Process image for ML model
        processed_image = image_processor.preprocess_image(image)
        
        # Perform disease detection
        prediction = await disease_detector.predict(processed_image)
        
        # Format response
        response = {
            "disease": prediction["disease"],
            "confidence": float(prediction["confidence"]),
            "recommendations": prediction["recommendations"]
        }
        
        logger.info(f"Detection completed: {prediction['disease']} ({prediction['confidence']:.2f})")
        
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"Error during disease detection: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )

@app.get("/api/diseases")
async def get_supported_diseases():
    """Get list of diseases that can be detected"""
    diseases = disease_detector.get_supported_diseases()
    return {"diseases": diseases}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
