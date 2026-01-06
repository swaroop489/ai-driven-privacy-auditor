// NLP service connector

const axios = require("axios");

const NLP_SERVICE_URL = process.env.NLP_SERVICE_URL;

async function analyzeText(text) {
  const response = await axios.post(NLP_SERVICE_URL, { text });
  return response.data;
}

module.exports = {
  analyzeText
};
