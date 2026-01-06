// upload routes

const express = require("express");
const multer = require("multer");
const { uploadContent } = require("../controllers/uploadController");
const { protect } = require("../middlewares/authMiddleware");

const router = express.Router();

const upload = multer({
  storage: multer.memoryStorage()
});

router.post(
  "/",
  protect,
  upload.single("file"),
  uploadContent
);

module.exports = router;
