// admin controller
const User = require('../models/User');
const Upload = require('../models/Upload');
const Violation = require('../models/Violation');

// @desc    Get system stats
// @route   GET /api/admin/stats
// @access  Private/Admin
const getSystemStats = async (req, res) => {
  try {
    const userCount = await User.countDocuments();
    const uploadCount = await Upload.countDocuments();
    const violationCount = await Violation.countDocuments();

    // Optional: Count by severity
    const highRiskCount = await Violation.countDocuments({ severity: 'HIGH' });

    res.json({
      userCount,
      uploadCount,
      violationCount,
      highRiskCount
    });
  } catch (error) {
    res.status(500).json({ message: 'Server Error', error: error.message });
  }
};

// @desc    Get recent violations
// @route   GET /api/admin/violations
// @access  Private/Admin
const getGlobalViolations = async (req, res) => {
  try {
    // Fetch last 50 violations, populated with upload and user info
    const violations = await Violation.find({})
      .sort({ createdAt: -1 })
      .limit(50)
      .populate({
        path: 'upload',
        populate: {
          path: 'user',
          select: 'name email'
        }
      });

    res.json(violations);
  } catch (error) {
    res.status(500).json({ message: 'Server Error', error: error.message });
  }
};

module.exports = {
  getSystemStats,
  getGlobalViolations
};
