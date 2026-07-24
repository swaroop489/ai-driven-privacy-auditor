const rateLimit = require('express-rate-limit');


const apiLimiter = rateLimit({
    windowMs: 1 * 60 * 1000, 
    max: 60, 
    message: { message: 'Too many requests from this IP, please try again after a minute.' },
    standardHeaders: true, 
    legacyHeaders: false, 
});

module.exports = { apiLimiter };
