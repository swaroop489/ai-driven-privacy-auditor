const express = require('express');
const cors = require('cors');
const userRoutes = require('./routes/userRoutes');
const uploadRoutes = require('./routes/uploadRoutes');
const userUploadRoutes = require('./routes/userUploadRoutes');
const adminRoutes = require('./routes/adminRoutes');
const chatRoutes = require('./routes/chatRoutes');

const app = express();

// Middleware
app.use(express.json());
app.use(cors());

// Routes
app.use('/api/users', userRoutes);
app.use('/api/upload', uploadRoutes);
app.use('/api/user-uploads', userUploadRoutes);
app.use('/api/admin', adminRoutes);
app.use('/api/chat', chatRoutes);

app.get('/', (req, res) => {
    res.send('API is running...');
});

module.exports = app;
