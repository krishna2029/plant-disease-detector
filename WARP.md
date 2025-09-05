# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Architecture

This is a full-stack plant disease detection application with a clear separation between frontend and backend:

### Backend Architecture (FastAPI + ML)
- **FastAPI Application** (`backend/main.py`): RESTful API server with CORS middleware configured for React frontend
- **ML Model Layer** (`backend/models/disease_detector.py`): TensorFlow/Keras CNN model for disease classification
  - Uses demo model by default but supports loading trained models from `models/plant_disease_model.h5`
  - Supports 10 disease classes including "Healthy", "Bacterial Spot", "Early Blight", etc.
  - Includes comprehensive treatment recommendations for each disease
- **Image Processing** (`backend/utils/image_processor.py`): PIL/OpenCV-based image preprocessing
  - Handles image resizing, normalization, and quality validation
  - Includes advanced features like CLAHE enhancement and leaf region detection
- **API Endpoints**: 
  - `POST /api/detect`: Main disease detection endpoint
  - `GET /health`: Health check with model status
  - `GET /api/diseases`: List supported diseases

### Frontend Architecture (React + TypeScript)
- **Main App** (`frontend/src/App.tsx`): State management for detection results and loading states
- **ImageUpload Component**: Drag-and-drop interface with preview functionality
- **ResultsDisplay Component**: Confidence visualization and treatment recommendations
- **Type Safety**: TypeScript interfaces for API responses (`DetectionResult`)

### Key Integration Points
- Frontend communicates with backend via `http://localhost:5000/api/detect`
- File upload uses FormData for multipart/form-data requests
- Error handling and loading states managed in React components

## Development Commands

### Backend Development
```bash
# Setup backend environment
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt

# Start development server
python main.py
# Alternative: uvicorn main:app --host 0.0.0.0 --port 5000 --reload

# Test API endpoints
curl http://localhost:5000/health
curl -X POST "http://localhost:5000/api/detect" -F "file=@path/to/image.jpg"
```

### Frontend Development
```bash
# Setup frontend environment
cd frontend
npm install

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

### Running Both Services
The application requires both backend and frontend running simultaneously:
1. Backend on `http://localhost:5000`
2. Frontend on `http://localhost:3000`

## Model Development

### Current Model Status
- Uses demo CNN model by default (`_create_demo_model()`)
- Model path: `backend/models/plant_disease_model.h5` (if available)
- Input shape: 224x224x3 (RGB images)
- Output: 10 classes with softmax activation

### Adding New Diseases
1. Update `class_names` list in `disease_detector.py`
2. Add treatment recommendations to `recommendations` dictionary
3. Retrain model with new disease data
4. Save trained model to `backend/models/plant_disease_model.h5`

### Image Processing Pipeline
1. PIL Image validation and conversion to RGB
2. Resize to 224x224 using LANCZOS resampling
3. Normalization to [0,1] range
4. Optional enhancements: CLAHE, leaf region detection
5. Quality validation: blur detection, brightness checks

## Development Patterns

### Error Handling
- Backend uses HTTPException for API errors
- Image processing failures return safe fallback responses
- Frontend handles network errors gracefully

### Async Pattern
- FastAPI uses async/await for I/O operations
- Model loading and prediction are async methods
- Image processing remains synchronous within async handlers

### Type Safety
- Backend uses Pydantic-style type hints
- Frontend uses TypeScript interfaces for API responses
- Consistent typing between frontend and backend data structures

## Testing Strategy

### Backend Testing
- Test API endpoints with sample images
- Validate image preprocessing pipeline
- Mock model predictions for consistent testing
- Test error scenarios (invalid files, processing failures)

### Frontend Testing
- Component testing with React Testing Library
- Mock API responses for predictable testing
- Test drag-and-drop functionality
- Validate confidence score visualization

## Deployment Considerations

### Production Requirements
- Replace demo ML model with trained production model
- Use production ASGI server (gunicorn + uvicorn workers)
- Serve React build through nginx or similar
- Configure proper CORS origins for production domains
- Add rate limiting and input validation
- Implement proper logging and monitoring

### Environment Configuration
- Backend uses python-dotenv for environment variables
- Consider containerizing both services with Docker
- Model files should be managed separately from code deployment
