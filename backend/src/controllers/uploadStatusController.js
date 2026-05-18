const { getUploadStatus } = require("../services/uploadStatusService");

async function fetchUploadStatus(req, res, next) {
  try {
    const { jobId } = req.params;
    const upload = await getUploadStatus(jobId, req.user._id);

    if (!upload) {
      return res.status(404).json({
        success: false,
        message: "Upload job not found"
      });
    }

    return res.status(200).json({
      success: true,
      upload
    });
  } catch (error) {
    next(error);
  }
}

module.exports = {
  fetchUploadStatus
};
