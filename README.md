# 🔐 AI-Driven Privacy Auditor  
**MERN + AWS + NLP + OCR**

A cloud-powered platform that automatically detects and prevents **sensitive data leaks** (PII) such as  
📱 phone numbers, 🪪 IDs, 📍 locations, 📧 emails, and 🖼️ text hidden inside images.

Users upload text or files → AI inspects content → Flags violations → Admin gets alerts.

---

# 🧩 1. Problem Statement

With the increasing use of social platforms, people unintentionally upload sensitive information like:

- Phone numbers  
- Aadhar, PAN, Passport IDs  
- Addresses & geolocations  
- Vehicle numbers  
- Photos of documents  

This leads to:
- Privacy breaches  
- Identity theft  
- Fraud  
- Data misuse  
- Non-compliance with privacy laws (GDPR / India DPDP Act)

**There is no automated system that warns users *before* they accidentally leak private information.**

---

# 🎯 2. Our Solution

We built an **AI-powered privacy auditor** that:

### 🧠 1. Uses NLP to scan text for sensitive info  
Detects:
- Phone numbers  
- Emails  
- Addresses  
- IDs (Aadhar/PAN)  
- GPS-like text  

### 📷 2. Uses OCR to extract text from images  
Handles:
- Photos of ID cards  
- Screenshots  
- Documents  
- Photos with embedded text  

### 🛡️ 3. Automatically flags violations  
- Categorizes severity  
- Logs the violations  
- Alerts admins  
- Prevents posting when high-risk PII is detected  

### ☁️ 4. Runs fully on AWS  
- AWS S3 for file uploads  
- AWS Lambda microservices for NLP & OCR  
- API Gateway for routing  
- IAM for security  
- CloudWatch for monitoring  
- MongoDB Atlas for data storage  

---

# 🏗️ 3. System Architecture


---

# 🚀 4. Features

### 🟢 User Features
- Upload text or image files  
- Immediate AI scan for PII  
- Get warnings before posting  
- View your flagged uploads  

### 🔴 Admin Features
- Dashboard with real-time violations  
- View flagged users  
- Audit logs  
- Violation severity stats  
- Export reports  

### 🤖 AI Features
- NLP NER-based PII detection  
- OCR extraction from images  
- Regex backup matching patterns  
- Confidence scoring  
- Hybrid model = better accuracy  

### ☁️ Cloud Features
- S3 → Lambda triggers  
- API Gateway REST APIs  
- IAM role-based access control  
- CloudWatch monitoring  
- Scalable stateless microservices  

---

# 🧬 5. Tech Stack

### **Frontend**
- React 18  
- Vite  
- Context API  
- Axios  

### **Backend**
- Node.js + Express  
- MongoDB Atlas (Mongoose)  
- JWT Auth  

### **AI Microservices**
- FastAPI  
- spaCy / Regex (NLP)  
- Tesseract OCR  
- Python 3.10  
- Dockerized Lambdas  

### **Cloud**
- AWS Lambda  
- S3  
- API Gateway  
- IAM  
- CloudWatch  
- Terraform (optional)  

---

# 📁 6. Folder Structure (High-Level)

```
ai-privacy-auditor/
│
├── backend/ # Express + MongoDB API
├── frontend/ # React UI (User + Admin)
├── ai-services/ # NLP + OCR microservices
├── infrastructure/ # AWS infra (Lambda, S3, IAM, Terraform)
└── scripts/ # Helper scripts

```


---

# 🔍 7. AI Microservices

### **NLP Microservice**
- Extracts text entities  
- Detects PII using:
  - spaCy NER  
  - Regex rules  
- Returns structured JSON violations  

### **OCR Microservice**
- Reads text from:
  - ID card photos  
  - Screenshots  
  - Documents  
- Applies PII regex scanning afterward  

---

# 🔄 8. Workflow

### **Text Upload Flow**
1. User enters text  
2. Text sent to backend  
3. Backend calls NLP Lambda  
4. NLP returns violations  
5. Stored in MongoDB  
6. Respond to user  

### **Image Upload Flow**
1. User uploads image  
2. Stored in S3  
3. S3 triggers OCR Lambda  
4. OCR extracts text  
5. NLP detects PII  
6. Violations stored  
7. Notify admin  

---

# 🔐 9. Security

- JWT-based authentication  
- Admin role-based authorization  
- Signed S3 URLs  
- IAM restricted Lambda execution roles  
- HTTPS enforced  
- Sanitized inputs  
- Rate limiting on API Gateway  

---

# 🧪 10. Testing

Includes:
- Unit tests for NLP extraction  
- Unit tests for OCR extraction  
- Integration tests for API Gateway → Lambda  
- Load tests for bulk uploads  

---

# ⚙️ 11. Deployment

### **Backend**

```
npm install
npm run build
npm run start

```


### **Frontend**
```
npm install
npm run dev
npm run build

```


### **AI Services**

```
docker build -t nlp .
docker build -t ocr .
```



### **AWS**
- Upload Lambda zip  
- Deploy API Gateway  
- Attach IAM roles  
- Set up S3 triggers  

---

# 📈 12. Future Enhancements

- Add AWS Textract for better OCR  
- Automatic PII redaction  
- Integrate with WhatsApp/Telegram bots  
- Add fraud pattern detection  
- Add analytics dashboard with charts  

---



