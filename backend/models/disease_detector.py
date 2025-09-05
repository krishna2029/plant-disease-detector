import tensorflow as tf
import numpy as np
from typing import Dict, List, Optional
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class DiseaseDetector:
    """
    Plant disease detection model using TensorFlow
    """
    
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.model_path = model_path or "models/plant_disease_model.h5"
        self.class_names = [
            "Healthy",
            "Bacterial Spot",
            "Early Blight", 
            "Late Blight",
            "Leaf Mold",
            "Septoria Leaf Spot",
            "Spider Mites",
            "Target Spot",
            "Yellow Leaf Curl Virus",
            "Mosaic Virus"
        ]
        
        # Disease recommendations mapping
        self.recommendations = {
            "Healthy": [
                "Your plant appears healthy! Continue current care practices.",
                "Maintain proper watering and ensure good air circulation.",
                "Monitor regularly for any changes."
            ],
            "Bacterial Spot": [
                "Remove affected leaves and dispose of them properly.",
                "Apply copper-based fungicide spray.",
                "Improve air circulation around plants.",
                "Water at soil level to avoid wetting leaves.",
                "Consider using drip irrigation."
            ],
            "Early Blight": [
                "Remove and destroy infected plant debris.",
                "Apply fungicide containing chlorothalonil or copper.",
                "Ensure proper plant spacing for air circulation.",
                "Water early in the day so leaves dry quickly.",
                "Consider crop rotation next season."
            ],
            "Late Blight": [
                "Remove affected plants immediately to prevent spread.",
                "Apply preventive fungicide spray (copper or mancozeb).",
                "Ensure good drainage and avoid overhead watering.",
                "Increase air circulation between plants.",
                "Monitor weather conditions - disease spreads in cool, wet weather."
            ],
            "Leaf Mold": [
                "Improve greenhouse ventilation if growing indoors.",
                "Reduce humidity around plants.",
                "Remove infected leaves immediately.",
                "Apply fungicide spray in the evening.",
                "Consider resistant varieties for future planting."
            ],
            "Septoria Leaf Spot": [
                "Remove infected leaves from bottom of plant first.",
                "Apply organic fungicide or neem oil spray.",
                "Mulch around plants to prevent soil splash.",
                "Water at ground level only.",
                "Stake plants to improve air circulation."
            ],
            "Spider Mites": [
                "Spray plants with water to dislodge mites.",
                "Apply insecticidal soap or neem oil.",
                "Increase humidity around plants.",
                "Introduce beneficial insects like ladybugs.",
                "Remove heavily infested leaves."
            ],
            "Target Spot": [
                "Remove infected plant debris immediately.",
                "Apply preventive fungicide treatment.",
                "Improve air circulation and reduce humidity.",
                "Avoid overhead watering.",
                "Consider soil sterilization for severe cases."
            ],
            "Yellow Leaf Curl Virus": [
                "Remove infected plants to prevent spread.",
                "Control whitefly populations (vector of virus).",
                "Use reflective mulch to deter insects.",
                "Plant virus-resistant varieties.",
                "Monitor and remove weeds that may harbor the virus."
            ],
            "Mosaic Virus": [
                "Remove and destroy infected plants immediately.",
                "Disinfect tools between plants.",
                "Control aphid populations (virus vector).",
                "Wash hands thoroughly when handling plants.",
                "Plant virus-resistant cultivars in future."
            ]
        }
    
    async def load_model(self):
        """Load the pre-trained model"""
        try:
            # For demo purposes, create a simple mock model
            # In production, you would load a pre-trained model
            if os.path.exists(self.model_path):
                self.model = tf.keras.models.load_model(self.model_path)
            else:
                # Create a simple CNN model for demonstration
                self.model = self._create_demo_model()
                logger.warning("Using demo model. Replace with trained model for production.")
            
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            # Create a fallback demo model
            self.model = self._create_demo_model()
    
    def _create_demo_model(self):
        """Create a simple demo model for testing purposes"""
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(224, 224, 3)),
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(len(self.class_names), activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    async def predict(self, image: np.ndarray) -> Dict:
        """
        Predict disease from preprocessed image
        
        Args:
            image: Preprocessed image array
            
        Returns:
            Dictionary with prediction results
        """
        if self.model is None:
            await self.load_model()
        
        try:
            # Add batch dimension if needed
            if len(image.shape) == 3:
                image = np.expand_dims(image, axis=0)
            
            # Make prediction
            predictions = self.model.predict(image, verbose=0)
            
            # Get the class with highest probability
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            disease_name = self.class_names[predicted_class_idx]
            
            # Get recommendations
            recommendations = self.recommendations.get(disease_name, [
                "Consult with a plant pathologist for specific treatment advice.",
                "Monitor the plant closely for changes.",
                "Consider isolating the plant if symptoms worsen."
            ])
            
            return {
                "disease": disease_name,
                "confidence": confidence,
                "recommendations": recommendations,
                "all_predictions": {
                    self.class_names[i]: float(predictions[0][i]) 
                    for i in range(len(self.class_names))
                }
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            # Return a safe fallback response
            return {
                "disease": "Analysis Failed",
                "confidence": 0.0,
                "recommendations": [
                    "Unable to analyze image. Please try again with a clearer image.",
                    "Ensure the image shows a clear view of plant leaves.",
                    "Contact support if the problem persists."
                ]
            }
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None
    
    def get_supported_diseases(self) -> List[str]:
        """Get list of diseases that can be detected"""
        return self.class_names.copy()
