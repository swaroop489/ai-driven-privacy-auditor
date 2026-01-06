// OCR service connector

const axios = require("axios");
const FormData = require("form-data");

const OCR_SERVICE_URL = process.env.OCR_SERVICE_URL;

async function analyzeImage(file) {
  const form = new FormData();

  form.append("file", file.buffer, {
    filename: file.originalname,
    contentType: file.mimetype
  });

  const response = await axios.post(OCR_SERVICE_URL, form, {
    headers: form.getHeaders()
  });

  return response.data;
}

module.exports = {
  analyzeImage
};
