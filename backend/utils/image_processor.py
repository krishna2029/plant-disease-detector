import cv2
import numpy as np
from PIL import Image
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    """
    Image preprocessing utilities for plant disease detection
    """
    
    def __init__(self, target_size: Tuple[int, int] = (224, 224)):
        self.target_size = target_size
    
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Preprocess image for ML model input
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed numpy array ready for model prediction
        """
        try:
            # Resize image
            image = image.resize(self.target_size, Image.Resampling.LANCZOS)
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Ensure 3 channels (RGB)
            if len(img_array.shape) == 2:
                img_array = np.stack([img_array] * 3, axis=-1)
            elif img_array.shape[2] == 4:  # RGBA
                img_array = img_array[:, :, :3]
            
            # Normalize pixel values to [0, 1]
            img_array = img_array.astype(np.float32) / 255.0
            
            return img_array
            
        except Exception as e:
            logger.error(f"Image preprocessing failed: {e}")
            raise ValueError(f"Failed to preprocess image: {e}")
    
    def enhance_image(self, image: Image.Image) -> Image.Image:
        """
        Apply image enhancement techniques
        
        Args:
            image: PIL Image object
            
        Returns:
            Enhanced PIL Image
        """
        try:
            # Convert PIL to OpenCV format
            img_array = np.array(image)
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
            lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            
            # Convert back to RGB and PIL
            enhanced_rgb = cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)
            return Image.fromarray(enhanced_rgb)
            
        except Exception as e:
            logger.warning(f"Image enhancement failed, using original: {e}")
            return image
    
    def detect_leaf_regions(self, image: Image.Image) -> Image.Image:
        """
        Attempt to isolate leaf regions in the image
        
        Args:
            image: PIL Image object
            
        Returns:
            Image with leaf regions highlighted/isolated
        """
        try:
            img_array = np.array(image)
            
            # Convert to HSV for better color-based segmentation
            hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            
            # Define range for green colors (leaves)
            lower_green = np.array([35, 40, 40])
            upper_green = np.array([85, 255, 255])
            
            # Create mask for green regions
            mask = cv2.inRange(hsv, lower_green, upper_green)
            
            # Apply morphological operations to clean up the mask
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # Apply mask to original image
            result = img_array.copy()
            result[mask == 0] = [0, 0, 0]  # Black out non-leaf areas
            
            return Image.fromarray(result)
            
        except Exception as e:
            logger.warning(f"Leaf detection failed, using original: {e}")
            return image
    
    def validate_image_quality(self, image: Image.Image) -> Tuple[bool, str]:
        """
        Validate if image is suitable for disease detection
        
        Args:
            image: PIL Image object
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            # Check minimum resolution
            min_size = 100
            if image.width < min_size or image.height < min_size:
                return False, f"Image too small. Minimum size: {min_size}x{min_size}"
            
            # Check if image is too dark or too bright
            img_array = np.array(image.convert('L'))  # Convert to grayscale
            mean_brightness = np.mean(img_array)
            
            if mean_brightness < 30:
                return False, "Image too dark. Please use better lighting."
            elif mean_brightness > 220:
                return False, "Image too bright. Please reduce lighting."
            
            # Check for blur (using Laplacian variance)
            img_gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
            laplacian_var = cv2.Laplacian(img_gray, cv2.CV_64F).var()
            
            if laplacian_var < 100:  # Threshold for blur detection
                return False, "Image appears blurry. Please take a clearer photo."
            
            return True, "Image quality is acceptable"
            
        except Exception as e:
            logger.error(f"Image quality validation failed: {e}")
            return True, "Could not validate image quality, proceeding anyway"
