// upload controller

const { auditContent } = require("../services/auditService");

async function uploadContent(req, res, next) {
  try {
    const { text } = req.body;
    const image = req.file || null;

    if (!text && !image) {
      return res.status(400).json({
        success: false,
        message: "Text or image is required"
      });
    }

    const auditResult = await auditContent({
      text,
      image,
      userId: req.user._id
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
