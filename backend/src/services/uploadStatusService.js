const Upload = require("../models/Upload");

async function getUploadStatus(jobId, userId) {
  const upload = await Upload.findOne({ jobId, user: userId })
    .lean();

  return upload;
}

module.exports = {
  getUploadStatus
};
