const axios = require("axios");
const FormData = require("form-data");
const http = require("http");
const https = require("https");

const OCR_SERVICE_URL = process.env.OCR_SERVICE_URL;
const OCR_TIMEOUT_MS = Number(process.env.OCR_TIMEOUT_MS || 30000);

const ocrHttpClient = axios.create({
  timeout: OCR_TIMEOUT_MS,
  httpAgent: new http.Agent({ keepAlive: true, maxSockets: 25 }),
  httpsAgent: new https.Agent({ keepAlive: true, maxSockets: 25 })
});

async function analyzeImage(file) {
  const form = new FormData();

  form.append("file", file.buffer, {
    filename: file.originalname,
    contentType: file.mimetype
  });

  try {
    const response = await ocrHttpClient.post(OCR_SERVICE_URL, form, {
      headers: form.getHeaders()
    });
    return response.data;
  } catch (error) {
    console.error(`OCR Service Error: ${error.message} (URL: ${OCR_SERVICE_URL})`);
    throw new Error(`OCR Service failed: ${error.response?.data?.detail || error.message}`);
  }
}

module.exports = {
  analyzeImage
};
