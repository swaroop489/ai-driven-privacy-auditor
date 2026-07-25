const { redisClient, isRedisConnected } = require('../utils/redisClient');
const crypto = require('crypto');

const cacheMiddleware = (ttlSeconds = 3600) => {
    return async (req, res, next) => {
        if (!isRedisConnected) {
            return next();
        }

        if (req.method !== 'POST') return next();

        try {
            const payload = JSON.stringify(req.body);
            const hash = crypto.createHash('sha256').update(payload).digest('hex');
            const key = `audit_cache:${hash}`;

            const cachedResponse = await redisClient.get(key);

            if (cachedResponse) {
                return res.status(200).json(JSON.parse(cachedResponse));
            }

            const originalJson = res.json.bind(res);
            res.json = (body) => {
                if (res.statusCode >= 200 && res.statusCode < 300) {
                    redisClient.setEx(key, ttlSeconds, JSON.stringify(body)).catch(err => console.error("Redis Cache Error:", err));
                }
                originalJson(body);
            };

            next();
        } catch (error) {
            console.error("Cache Middleware Error:", error);
            next();
        }
    };
};

module.exports = cacheMiddleware;
