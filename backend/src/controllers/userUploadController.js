const { getUserUploads } = require("../services/userUploadService");

async function fetchUserUploads(req, res, next) {
  try {
    const result = await getUserUploads(req.user._id, req.query);

    return res.status(200).json({
      success: true,
      ...result
    });
  } catch (error) {
    next(error);
  }
}

module.exports = {
  fetchUserUploads
};
