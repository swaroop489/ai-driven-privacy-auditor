const Upload = require("../models/Upload");
const Violation = require("../models/Violation");
const AuditLog = require("../models/AuditLog");

async function getSystemStats() {
  const totalUploads = await Upload.countDocuments();
  const blockedUploads = await Upload.countDocuments({ action: "BLOCK" });
  const warnedUploads = await Upload.countDocuments({ action: "WARN" });

  const violationsByType = await Violation.aggregate([
    { $group: { _id: "$type", count: { $sum: 1 } } }
  ]);

  return {
    totalUploads,
    blockedUploads,
    warnedUploads,
    violationsByType
  };
}

async function getAllUploads(query) {
  const page = Number(query.page) || 1;
  const limit = Number(query.limit) || 20;
  const skip = (page - 1) * limit;

  const filter = {};

  if (query.action) filter.action = query.action;

  const uploads = await Upload.find(filter)
    .populate("user", "email role")
    .sort({ createdAt: -1 })
    .skip(skip)
    .limit(limit)
    .lean();

  const uploadIds = uploads.map(u => u._id);

  const violations = await Violation.find({
    upload: { $in: uploadIds }
  }).lean();

  const groupedViolations = violations.reduce((acc, v) => {
    acc[v.upload] = acc[v.upload] || [];
    acc[v.upload].push(v);
    return acc;
  }, {});

  const total = await Upload.countDocuments(filter);

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

async function getAuditLogs(query) {
  const page = Number(query.page) || 1;
  const limit = Number(query.limit) || 20;
  const skip = (page - 1) * limit;

  const logs = await AuditLog.find()
    .populate("user", "email")
    .populate("upload")
    .sort({ createdAt: -1 })
    .skip(skip)
    .limit(limit)
    .lean();

  const total = await AuditLog.countDocuments();

  return {
    logs,
    pagination: {
      total,
      page,
      limit,
      totalPages: Math.ceil(total / limit)
    }
  };
}

module.exports = {
  getSystemStats,
  getAllUploads,
  getAuditLogs
};
