const express = require("express");
const { fetchUserUploads } = require("../controllers/userUploadController");
const { protect } = require("../middlewares/authMiddleware");

const router = express.Router();

router.get("/my-uploads", protect, fetchUserUploads);

module.exports = router;
