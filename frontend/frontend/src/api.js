import axios from 'axios';

// Define your backend APIs
const BACKEND_API_URL = 'http://localhost:5000';
const PYTHON_API_URL = 'http://localhost:5001';

// Example API call to Node.js backend
export const getBackendData = async () => {
    return await axios.get(`${BACKEND_API_URL}/`);
};

// Example API call to Python backend
export const analyzeVideo = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    return await axios.post(`${PYTHON_API_URL}/analyze`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
};
