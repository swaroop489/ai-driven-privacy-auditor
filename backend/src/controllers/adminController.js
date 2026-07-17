const User = require('../models/User');
const Upload = require('../models/Upload');
const Violation = require('../models/Violation');

const ADMIN_STREAM_INTERVAL_MS = Number(process.env.ADMIN_STREAM_INTERVAL_MS || 5000);

async function getAdminSnapshot() {
  const [
    userCount,
    uploadCount,
    violationCount,
    highRiskCount,
    violations
  ] = await Promise.all([
    User.countDocuments(),
    Upload.countDocuments(),
    Violation.countDocuments(),
    Violation.countDocuments({ severity: 'HIGH' }),
    Violation.find({})
      .sort({ createdAt: -1 })
      .limit(50)
      .populate({
        path: 'upload',
        populate: {
          path: 'user',
          select: 'name email'
        }
      })
      .lean()
  ]);

  return {
    stats: {
      userCount,
      uploadCount,
      violationCount,
      highRiskCount
    },
    violations
  };
}


const getSystemStats = async (req, res) => {
  try {
    const { stats } = await getAdminSnapshot();

    res.json({
      ...stats
    });
  } catch (error) {
    res.status(500).json({ message: 'Server Error', error: error.message });
  }
};


const getGlobalViolations = async (req, res) => {
  try {
    const { violations } = await getAdminSnapshot();

    res.json(violations);
  } catch (error) {
    res.status(500).json({ message: 'Server Error', error: error.message });
  }
};

const streamAdminUpdates = async (req, res) => {
  try {
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache, no-transform');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('X-Accel-Buffering', 'no');
    res.flushHeaders?.();
    res.write(`retry: ${ADMIN_STREAM_INTERVAL_MS}\n\n`);

    req.socket.setTimeout(0);

    let lastSignature = '';
    let isAlive = true;

    const pushSnapshot = async () => {
      if (!isAlive) {
        return;
      }

      try {
        const snapshot = await getAdminSnapshot();
        const signature = JSON.stringify(snapshot);

        if (signature !== lastSignature) {
          lastSignature = signature;
          res.write(`event: snapshot\n`);
          res.write(`data: ${signature}\n\n`);
        } else {
          res.write(`event: heartbeat\n`);
          res.write(`data: {"ok":true}\n\n`);
        }
      } catch (error) {
        res.write(`event: error\n`);
        res.write(`data: ${JSON.stringify({ message: error.message })}\n\n`);
      }
    };

    await pushSnapshot();
    const interval = setInterval(pushSnapshot, ADMIN_STREAM_INTERVAL_MS);

    req.on('close', () => {
      isAlive = false;
      clearInterval(interval);
    });
  } catch (error) {
    res.status(500).json({ message: 'Server Error', error: error.message });
  }
};

module.exports = {
  getSystemStats,
  getGlobalViolations,
  streamAdminUpdates
};
