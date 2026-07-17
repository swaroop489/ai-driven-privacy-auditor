const axios = require("axios");
const http = require("http");
const https = require("https");

const NLP_SERVICE_URL = process.env.NLP_SERVICE_URL;
const NLP_TIMEOUT_MS = Number(process.env.NLP_TIMEOUT_MS || 15000);

const nlpHttpClient = axios.create({
  timeout: NLP_TIMEOUT_MS,
  httpAgent: new http.Agent({ keepAlive: true, maxSockets: 25 }),
  httpsAgent: new https.Agent({ keepAlive: true, maxSockets: 25 }),
  headers: {
    "Content-Type": "application/json"
  }
});

async function analyzeText(text) {
  try {
    const response = await nlpHttpClient.post(NLP_SERVICE_URL, { text });
    return response.data;
  } catch (error) {
    console.error(`NLP Service Error: ${error.message} (URL: ${NLP_SERVICE_URL})`);
    throw new Error(`NLP Service failed: ${error.response?.data?.detail || error.message}`);
  }
}

module.exports = {
  analyzeText
};
