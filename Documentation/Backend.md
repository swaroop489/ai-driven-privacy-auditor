```
backend/
├── src/
│   ├── config/
│   │   ├── db.js                 # MongoDB Atlas connection
│   │   ├── aws.js                # AWS SDK (S3, Lambda) config
│   │   └── env.js                # Environment variables
│   │
│   ├── controllers/
│   │   ├── uploadController.js   # Handles file/text uploads
│   │   ├── auditController.js    # Communicates with NLP/OCR microservices
│   │   ├── reportController.js   # Admin analytics, flagged users
│   │   └── userController.js     # Authentication, roles
│   │
│   ├── models/
│   │   ├── User.js
│   │   ├── Upload.js
│   │   ├── AuditLog.js
│   │   └── Violation.js
│   │
│   ├── routes/
│   │   ├── uploadRoutes.js
│   │   ├── auditRoutes.js
│   │   ├── adminRoutes.js
│   │   └── userRoutes.js
│   │
│   ├── middlewares/
│   │   ├── authMiddleware.js
│   │   ├── errorHandler.js
│   │   └── s3Upload.js           # Handles file upload to AWS S3
│   │
│   ├── services/
│   │   ├── nlpService.js         # Calls NLP Cloud Run microservice
│   │   ├── ocrService.js         # Calls OCR Cloud Run microservice
│   │   ├── emailService.js       # Sends alerts if violations
│   │   └── auditService.js       # Business logic for detection
│   │
│   ├── app.js                    # Express app
│   └── server.js                 # Entry point
│
├── package.json
└── .env
```
