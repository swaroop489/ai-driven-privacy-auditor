const express = require("express");
const multer = require("multer");
const { uploadContent } = require("../controllers/uploadController");
const { fetchUploadStatus } = require("../controllers/uploadStatusController");
const { protect } = require("../middlewares/authMiddleware");
const cacheMiddleware = require("../middlewares/cacheMiddleware");

const router = express.Router();

const upload = multer({
  storage: multer.memoryStorage()
});

router.post(
  "/",
  protect,
  upload.single("file"),
  cacheMiddleware(3600),
  uploadContent
);

router.get(
  "/status/:jobId",
  protect,
  fetchUploadStatus
);

module.exports = router;
