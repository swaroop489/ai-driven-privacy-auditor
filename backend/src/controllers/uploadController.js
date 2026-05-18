// upload controller

const crypto = require("crypto");
const { uploadToS3, uploadTextToS3 } = require("../middlewares/s3Upload");
const { auditContent } = require("../services/auditService");
const Upload = require("../models/Upload");

function shouldUseAwsLambda() {
  return (
    process.env.NODE_ENV === "production" &&
    String(process.env.USE_AWS_LAMBDA).toLowerCase() === "true"
  );
}

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

    // In production, route single payloads through S3 so Lambda can process them asynchronously.
    if (shouldUseAwsLambda() && (text || image) && !(text && image)) {
      const jobId = crypto.randomUUID();
      const inputType = text ? "TEXT" : "IMAGE";

      try {
        const metadata = {
          jobid: jobId,
          userid: String(req.user._id),
          inputtype: inputType
        };

        if (text) {
          fileUrl = await uploadTextToS3(text, "pii-scan.txt", metadata);
        } else if (image) {
          fileUrl = await uploadToS3(image.buffer, image.mimetype, image.originalname, metadata);
        }

        await Upload.create({
          jobId,
          user: req.user._id,
          inputType,
          scanMode: "ASYNC",
          status: "PENDING",
          action: "ALLOW",
          violationCount: 0,
          fileUrl,
          sourceKey: fileUrl
        });

        return res.status(202).json({
          success: true,
          mode: "AWS_LAMBDA",
          message: "Content uploaded. AWS Lambda will process the scan asynchronously.",
          fileUrl,
          jobId
        });
      } catch (s3Error) {
        console.error("S3 Upload Error:", s3Error);
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
