// admin controller

const {
  getSystemStats,
  getAllUploads,
  getAuditLogs
} = require("../services/adminService");

async function fetchStats(req, res, next) {
  try {
    const stats = await getSystemStats();
    res.status(200).json({ success: true, stats });
  } catch (e) {
    next(e);
  }
}

async function fetchAllUploads(req, res, next) {
  try {
    const result = await getAllUploads(req.query);
    res.status(200).json({ success: true, ...result });
  } catch (e) {
    next(e);
  }
}

async function fetchAuditLogs(req, res, next) {
  try {
    const result = await getAuditLogs(req.query);
    res.status(200).json({ success: true, ...result });
  } catch (e) {
    next(e);
  }
}

module.exports = {
  fetchStats,
  fetchAllUploads,
  fetchAuditLogs
};
