```
backend/
│
├── src/
│   ├── app.js                         # Express app setup
│   ├── server.js                      # App entry point
│   │
│   ├── config/
│   │   ├── db.js                      # MongoDB Atlas connection
│   │   ├── aws.js                     # AWS SDK + S3 config
│   │   ├── cloudRun.js                # Cloud Run API URLs
│   │   └── env.js                     # Environment variable loader
│   │
│   ├── models/
│   │   ├── User.js                    # Schema: username, email, password, role
│   │   ├── Upload.js                  # Schema: fileURL, userID, auditStatus
│   │   ├── Violation.js               # Schema: type, detectedText, severity
│   │   └── AuditLog.js                # Schema: userID, action, timestamp
│   │
│   ├── controllers/
│   │   ├── userController.js          # Login, register, JWT token issue
│   │   ├── uploadController.js        # File/text upload
│   │   ├── auditController.js         # Call NLP/OCR microservices
│   │   ├── reportController.js        # Admin dashboard data
│   │   └── alertController.js         # Email/notification alerts
│   │
│   ├── routes/
│   │   ├── userRoutes.js              # /api/users/
│   │   ├── uploadRoutes.js            # /api/uploads/
│   │   ├── auditRoutes.js             # /api/audit/
│   │   ├── reportRoutes.js            # /api/reports/
│   │   └── adminRoutes.js             # /api/admin/
│   │
│   ├── middlewares/
│   │   ├── authMiddleware.js          # Verify JWT, roles
│   │   ├── errorHandler.js            # Global error handling
│   │   └── s3Upload.js                # Upload middleware for S3
│   │
│   ├── services/
│   │   ├── nlpService.js              # Communicate with NLP Cloud Run
│   │   ├── ocrService.js              # Communicate with OCR Cloud Run
│   │   ├── auditService.js            # Aggregates results, flags content
│   │   ├── emailService.js            # Sends admin alerts
│   │   └── logService.js              # Writes to AuditLog collection
│   │
│   ├── utils/
│   │   ├── regexPatterns.js           # Backup regex for phone, ID, etc.
│   │   ├── constants.js               # App constants (thresholds, roles)
│   │   ├── responseHelper.js          # Consistent API responses
│   │   └── logger.js                  # Winston or console logger
│   │
│   └── tests/
│       ├── user.test.js
│       ├── upload.test.js
│       └── audit.test.js
│
├── package.json
├── .env
├── .eslintrc.json
└── README.md

```
