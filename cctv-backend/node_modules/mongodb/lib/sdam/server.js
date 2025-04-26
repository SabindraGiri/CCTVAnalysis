const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
  res.send('Backend is working!');
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

const axios = require('axios');

// Example function to call Python API
async function callPythonAPI(fileData) {
  try {
    const response = await axios.post('http://localhost:5001/analyze', fileData);
    console.log(response.data);
  } catch (error) {
    console.error(error);
  }
}
