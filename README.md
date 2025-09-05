# Plant Disease Detector 🌱

A web application that uses machine learning and React to detect diseases in plant leaves from uploaded images.

## Features

- **AI-Powered Detection**: Uses TensorFlow/Keras deep learning model to identify plant diseases
- **User-Friendly Interface**: Modern React frontend with drag-and-drop image upload
- **Real-time Analysis**: Fast disease detection with confidence scores
- **Treatment Recommendations**: Provides actionable advice for each detected condition
- **Multiple Disease Support**: Detects common plant diseases including:
  - Bacterial Spot
  - Early Blight
  - Late Blight
  - Leaf Mold
  - Septoria Leaf Spot
  - Spider Mites
  - Target Spot
  - Yellow Leaf Curl Virus
  - Mosaic Virus

## Project Structure

```
plant-disease-detector/
├── frontend/                 # React TypeScript application
│   ├── public/
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── ImageUpload.tsx
│   │   │   ├── ResultsDisplay.tsx
│   │   │   └── *.css
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   └── tsconfig.json
├── backend/                  # FastAPI Python backend
│   ├── models/               # ML model and detection logic
│   │   └── disease_detector.py
│   ├── utils/                # Image processing utilities
│   │   └── image_processor.py
│   ├── main.py              # FastAPI application
│   └── requirements.txt
└── README.md
```

## Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- npm or yarn
- pip

## Setup Instructions

### 1. Clone and Navigate to Project

```bash
git clone <repository-url>
cd plant-disease-detector
```

### 2. Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:
   ```bash
   python main.py
   ```

The backend will be available at `http://localhost:5000`

### 3. Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## Usage

1. **Access the Application**: Open your browser and go to `http://localhost:3000`

2. **Upload an Image**: 
   - Drag and drop a leaf image onto the upload area, or
   - Click to browse and select an image file

3. **View Results**: 
   - Wait for the AI analysis to complete
   - Review the detected disease and confidence score
   - Read the treatment recommendations

4. **Upload Another**: Click "Upload Another Image" to analyze more plants

## API Endpoints

### Backend API (FastAPI)

- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /api/detect` - Upload image for disease detection
- `GET /api/diseases` - List of supported diseases

### Example API Usage

```bash
# Health check
curl http://localhost:5000/health

# Disease detection (with image file)
curl -X POST "http://localhost:5000/api/detect" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@path/to/leaf/image.jpg"
```

## Development

### Adding New Diseases

1. Update the `class_names` list in `backend/models/disease_detector.py`
2. Add corresponding treatment recommendations to the `recommendations` dictionary
3. Retrain or update the ML model to recognize the new disease

### Customizing the UI

- Modify components in `frontend/src/components/`
- Update styling in the respective `.css` files
- Adjust the main layout in `frontend/src/App.tsx`

### Model Improvements

- Replace the demo model with a trained model by updating `backend/models/disease_detector.py`
- Add more sophisticated image preprocessing in `backend/utils/image_processor.py`
- Implement model versioning and A/B testing

## Technologies Used

### Frontend
- React 18
- TypeScript
- CSS3 with modern features (backdrop-filter, gradients)
- Drag-and-drop file upload

### Backend
- FastAPI (Python web framework)
- TensorFlow/Keras (ML framework)
- Pillow (Image processing)
- OpenCV (Computer vision)
- Uvicorn (ASGI server)

### ML/AI
- Convolutional Neural Networks (CNN)
- Image preprocessing and augmentation
- Transfer learning capabilities

## Deployment

### Docker Deployment (Recommended)

Create a `docker-compose.yml` file:

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

### Production Considerations

- Use a production-ready web server (nginx) for the frontend
- Use a production ASGI server (gunicorn with uvicorn workers) for the backend
- Add proper logging and monitoring
- Implement rate limiting and security measures
- Use environment variables for configuration
- Add SSL/TLS certificates

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This application is for educational and research purposes. The disease detection results should not be used as the sole basis for agricultural decisions. Always consult with professional agricultural experts or plant pathologists for accurate diagnosis and treatment recommendations.

## Support

If you encounter any issues or have questions:

1. Check the console logs for error messages
2. Ensure both backend and frontend servers are running
3. Verify that all dependencies are installed correctly
4. Open an issue on the GitHub repository

---

**Happy Plant Health Monitoring! 🌿**
