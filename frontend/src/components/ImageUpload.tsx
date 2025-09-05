import React, { useState, useCallback } from 'react';
import './ImageUpload.css';

interface ImageUploadProps {
  onImageUpload: (file: File) => void;
  loading: boolean;
}

const ImageUpload: React.FC<ImageUploadProps> = ({ onImageUpload, loading }) => {
  const [dragOver, setDragOver] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  }, []);

  const handleFileInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFileSelect(files[0]);
    }
  }, []);

  const handleFileSelect = (file: File) => {
    // Validate file type
    if (!file.type.startsWith('image/')) {
      alert('Please select an image file');
      return;
    }

    // Create preview URL
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);

    // Call parent handler
    onImageUpload(file);
  };

  return (
    <div className="image-upload-container">
      <div
        className={`upload-area ${dragOver ? 'drag-over' : ''} ${loading ? 'loading' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {previewUrl ? (
          <div className="preview-container">
            <img src={previewUrl} alt="Preview" className="image-preview" />
            {loading && <div className="loading-overlay">Analyzing...</div>}
          </div>
        ) : (
          <div className="upload-prompt">
            <div className="upload-icon">📷</div>
            <p>Drag and drop a leaf image here, or click to select</p>
            <input
              type="file"
              accept="image/*"
              onChange={handleFileInputChange}
              className="file-input"
              disabled={loading}
            />
          </div>
        )}
      </div>
      
      {previewUrl && (
        <button 
          className="upload-another-btn"
          onClick={() => {
            setPreviewUrl(null);
            URL.revokeObjectURL(previewUrl);
          }}
          disabled={loading}
        >
          Upload Another Image
        </button>
      )}
    </div>
  );
};

export default ImageUpload;
