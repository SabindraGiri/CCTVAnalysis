import React, { useState } from 'react';
import axios from 'axios';

const PYTHON_API_URL = 'https://cctvanalysis.onrender.com';//

function UploadVideo() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [responseMessage, setResponseMessage] = useState('');

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a video file first!');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post(`${PYTHON_API_URL}/analyze`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const { message, total_frames, detected_objects, activity } = response.data;

      let resultText = `${message}\n\nTotal Frames: ${total_frames}\n\nDetected Objects:\n`;
      for (const [label, count] of Object.entries(detected_objects)) {
        resultText += `- ${label}: ${count}\n`;
      }

      if (activity) {
        resultText += `\nActivity Recognition:\n`;
        if (activity.loitering) resultText += `⚠️ Loitering Detected\n`;
        if (activity.group_gathering) resultText += `👥 Group Gathering Detected\n`;
        resultText += `🏃 Motion: ${activity.motion || 'Unknown'}\n`;
      }      

      setResponseMessage(resultText);
    } catch (error) {
      console.error('Error uploading video:', error);
      setResponseMessage('Failed to upload or analyze video.');
    }
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <h2>📹 Upload CCTV Video for Analysis</h2>

      <input type="file" accept="video/*" onChange={handleFileChange} style={{ margin: '1rem 0' }} />
      <br />
      <button onClick={handleUpload} style={{ padding: '10px', fontSize: '16px' }}>
        Upload and Analyze
      </button>

      <div style={{ marginTop: '2rem', whiteSpace: 'pre-wrap' }}>
        <h3>Analysis Result:</h3>
        <p>{responseMessage}</p>
      </div>
    </div>
  );
}

export default UploadVideo;
