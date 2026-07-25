const express = require("express");
const axios = require("axios");
const { protect } = require("../middlewares/authMiddleware");

const router = express.Router();
const NLP_SERVICE_URL = process.env.NLP_SERVICE_URL || "http://localhost:8000/api/v1/predict";
const CHAT_URL = NLP_SERVICE_URL.replace("/predict", "/chat");

router.post("/", protect, async (req, res) => {
    try {
        const response = await axios.post(CHAT_URL, { query: req.body.query });
        res.json(response.data);
    } catch (error) {
        console.error("Chat error:", error);
        res.status(500).json({ error: "Chat failed" });
    }
});

module.exports = router;
