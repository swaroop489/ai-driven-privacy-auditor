// upload controller

const { uploadToS3 } = require("../middlewares/s3Upload");
const { auditContent } = require("../services/auditService");

async function uploadContent(req, res, next) {
  try {
    const { text } = req.body;
    const image = req.file || null;
    let fileUrl = null;

    if (!text && !image) {
      return res.status(400).json({
        success: false,
        message: "Text or image is required"
      });
    }

    // Process S3 upload if in production and image exists
    if (process.env.NODE_ENV === 'production' && image) {
      try {
        fileUrl = await uploadToS3(image.buffer, image.mimetype, image.originalname);
      } catch (s3Error) {
        console.error("S3 Upload Error:", s3Error);
        // Continue without blocking, or fail? Failing seems safer for "Privacy Auditor" but allow fallback for now or handle as error
        // For now, let's log and proceed, but maybe we should fail if persistence is critical.
        // Given user request "Fully on AWS", failure of AWS S3 should probably be critical in prod.
        return res.status(500).json({ success: false, message: "Failed to upload file to storage" });
      }
    }

    const auditResult = await auditContent({
      text,
      image,
      userId: req.user._id,
      fileUrl
    });

    return res.status(200).json({
      success: true,
      action: auditResult.action,
      violationCount: auditResult.violationCount,
      violations: auditResult.violations
    });

  } catch (error) {
    next(error);
  }
}

module.exports = {
  uploadContent
};
