const { createClient } = require('redis');

const redisClient = createClient({
    url: process.env.REDIS_URL || 'redis://localhost:6379',
    socket: {
        reconnectStrategy: false 
    }
});

redisClient.on('error', (err) => {

});

let isRedisConnected = false;

const connectRedis = async () => {
    try {
        await redisClient.connect();
        isRedisConnected = true;
        console.log('Redis connected successfully for Caching and Rate Limiting');
    } catch (error) {
        console.error('Redis connection failed:', error.message);
        console.log('Continuing without Redis (Cache/Rate-Limits bypassed).');
    }
};

module.exports = { redisClient, connectRedis, isRedisConnected };
