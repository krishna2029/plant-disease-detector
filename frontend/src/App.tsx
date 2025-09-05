import React, { useState } from 'react';
import './App.css';
import ImageUpload from './components/ImageUpload';
import ResultsDisplay from './components/ResultsDisplay';

export interface DetectionResult {
  disease: string;
  confidence: number;
  recommendations: string[];
}

function App() {
  const [result, setResult] = useState<DetectionResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleImageUpload = async (imageFile: File) => {
    setLoading(true);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('image', imageFile);

      const response = await fetch('http://localhost:5000/api/detect', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to analyze image');
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error analyzing image:', error);
      // Handle error - could set an error state here
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Plant Disease Detector</h1>
        <p>Upload an image of a plant leaf to detect potential diseases</p>
      </header>
      
      <main className="App-main">
        <ImageUpload onImageUpload={handleImageUpload} loading={loading} />
        {result && <ResultsDisplay result={result} />}
      </main>
    </div>
  );
}

export default App;
