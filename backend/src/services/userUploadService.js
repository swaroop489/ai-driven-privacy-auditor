// fetch user uploads with pagination & filters

const Upload = require("../models/Upload");
const Violation = require("../models/Violation");

async function getUserUploads(userId, query) {
  const page = Number(query.page) || 1;
  const limit = Number(query.limit) || 10;
  const skip = (page - 1) * limit;

  const filter = { user: userId };

  if (query.action) filter.action = query.action;
  if (query.inputType) filter.inputType = query.inputType;

  const uploads = await Upload.find(filter)
    .sort({ createdAt: -1 })
    .skip(skip)
    .limit(limit)
    .lean();

  const total = await Upload.countDocuments(filter);

  const uploadIds = uploads.map(u => u._id);

  const violations = await Violation.find({
    upload: { $in: uploadIds }
  }).lean();

  const groupedViolations = violations.reduce((acc, v) => {
    acc[v.upload] = acc[v.upload] || [];
    acc[v.upload].push(v);
    return acc;
  }, {});

  return {
    uploads: uploads.map(u => ({
      ...u,
      violations: groupedViolations[u._id] || []
    })),
    pagination: {
      total,
      page,
      limit,
      totalPages: Math.ceil(total / limit)
    }
  };
}

module.exports = {
  getUserUploads
};
