// NLP service connector

const axios = require("axios");

const NLP_SERVICE_URL = process.env.NLP_SERVICE_URL;

async function analyzeText(text) {
  try {
    const response = await axios.post(NLP_SERVICE_URL, { text });
    return response.data;
  } catch (error) {
    console.error(`NLP Service Error: ${error.message} (URL: ${NLP_SERVICE_URL})`);
    // Return empty result to avoid crashing the whole flow? Or rethrow?
    // User sees "Something went wrong", so maybe text analysis failed.
    // Let's propagate a clearer error.
    throw new Error(`NLP Service failed: ${error.response?.data?.detail || error.message}`);
  }
}

module.exports = {
  analyzeText
};
