import React from 'react';
import { DetectionResult } from '../App';
import './ResultsDisplay.css';

interface ResultsDisplayProps {
  result: DetectionResult;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ result }) => {
  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return '#4CAF50'; // Green
    if (confidence >= 0.6) return '#FF9800'; // Orange
    return '#F44336'; // Red
  };

  const getConfidenceLabel = (confidence: number) => {
    if (confidence >= 0.8) return 'High Confidence';
    if (confidence >= 0.6) return 'Medium Confidence';
    return 'Low Confidence';
  };

  return (
    <div className="results-container">
      <h2>Detection Results</h2>
      
      <div className="disease-info">
        <h3 className="disease-name">{result.disease}</h3>
        <div className="confidence-container">
          <div className="confidence-bar">
            <div
              className="confidence-fill"
              style={{
                width: `${result.confidence * 100}%`,
                backgroundColor: getConfidenceColor(result.confidence)
              }}
            />
          </div>
          <span className="confidence-text">
            {(result.confidence * 100).toFixed(1)}% - {getConfidenceLabel(result.confidence)}
          </span>
        </div>
      </div>

      {result.recommendations && result.recommendations.length > 0 && (
        <div className="recommendations">
          <h4>Treatment Recommendations:</h4>
          <ul>
            {result.recommendations.map((recommendation, index) => (
              <li key={index}>{recommendation}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="disclaimer">
        <p><strong>Disclaimer:</strong> This is an automated analysis and should not replace professional agricultural advice. For severe cases or persistent issues, consult with an agricultural expert or plant pathologist.</p>
      </div>
    </div>
  );
};

export default ResultsDisplay;
