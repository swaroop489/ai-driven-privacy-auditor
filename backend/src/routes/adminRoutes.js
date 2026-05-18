const express = require('express');
const jwt = require('jsonwebtoken');
const User = require('../models/User');
const { protect } = require('../middlewares/authMiddleware');
const { admin } = require('../middlewares/adminMiddleware');
const { getSystemStats, getGlobalViolations, streamAdminUpdates } = require('../controllers/adminController');

const router = express.Router();

router.get('/stats', protect, admin, getSystemStats);
router.get('/violations', protect, admin, getGlobalViolations);

router.get('/stream', async (req, res, next) => {
  try {
    const bearerToken = req.headers.authorization?.startsWith('Bearer ')
      ? req.headers.authorization.split(' ')[1]
      : null;
    const token = req.query.token || bearerToken;

    if (!token) {
      return res.status(401).json({ message: 'Not authorized, no token' });
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = await User.findById(decoded.id).select('-password');

    if (!req.user) {
      return res.status(401).json({ message: 'User not found' });
    }

    if (req.user.role !== 'admin') {
      return res.status(401).json({ message: 'Not authorized as an admin' });
    }

    return streamAdminUpdates(req, res);
  } catch (error) {
    return res.status(401).json({ message: 'Not authorized, token failed' });
  }
});

module.exports = router;
