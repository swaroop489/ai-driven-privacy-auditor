const mongoose = require('mongoose');

const uploadSchema = mongoose.Schema({
  jobId: {
    type: String,
    index: true,
    sparse: true,
  },
  user: {
    type: mongoose.Schema.Types.ObjectId,
    required: true,
    ref: 'User',
  },
  inputType: {
    type: String,
    enum: ['TEXT', 'IMAGE', 'TEXT_IMAGE'],
    required: true,
  },
  fileUrl: {
    type: String, // Store S3 URL if uploaded
  },
  sourceKey: {
    type: String,
    index: true,
    sparse: true,
  },
  scanMode: {
    type: String,
    enum: ['SYNC', 'ASYNC'],
    default: 'SYNC',
  },
  status: {
    type: String,
    enum: ['PENDING', 'PROCESSING', 'COMPLETED', 'FAILED'],
    default: 'COMPLETED',
  },
  errorMessage: {
    type: String,
  },
  action: {
    type: String,
    enum: ['ALLOW', 'WARN', 'BLOCK'],
    required: true,
  },
  violationCount: {
    type: Number,
    required: true,
    default: 0,
  },
}, {
  timestamps: true,
});

const Upload = mongoose.model('Upload', uploadSchema);

module.exports = Upload;
