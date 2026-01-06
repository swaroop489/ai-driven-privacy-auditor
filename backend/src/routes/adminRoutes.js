const express = require('express');
const { protect } = require('../middlewares/authMiddleware');
const { admin } = require('../middlewares/adminMiddleware');
const { getSystemStats, getGlobalViolations } = require('../controllers/adminController');

const router = express.Router();

router.get('/stats', protect, admin, getSystemStats);
router.get('/violations', protect, admin, getGlobalViolations);

module.exports = router;
