```
frontend/
│
├── public/
│   ├── index.html
│   ├── favicon.ico
│   ├── manifest.json
│   └── robots.txt
│
├── src/
│   ├── App.jsx
│   ├── main.jsx
│   ├── index.css
│   │
│   ├── assets/
│   │   ├── logo.svg
│   │   ├── empty-state.png
│   │   └── banner.jpg
│   │
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── Sidebar.jsx
│   │   ├── FileUpload.jsx
│   │   ├── FileCard.jsx
│   │   ├── ViolationItem.jsx
│   │   ├── StatsCard.jsx
│   │   ├── Table.jsx
│   │   └── Loader.jsx
│   │
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── UserDashboard.jsx
│   │   ├── AdminDashboard.jsx
│   │   ├── AuditReports.jsx
│   │   └── NotFound.jsx
│   │
│   ├── context/
│   │   ├── AuthContext.jsx
│   │   └── AlertContext.jsx
│   │
│   ├── services/
│   │   ├── api.js                  # Axios config
│   │   ├── authService.js          # Login/register/logout
│   │   ├── uploadService.js        # Upload files/text
│   │   ├── auditService.js         # Get flagged results
│   │   └── reportService.js        # Admin analytics
│   │
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── useAlert.js
│   │   └── useFetch.js
│   │
│   ├── utils/
│   │   ├── constants.js
│   │   └── formatDate.js
│   │
│   ├── styles/
│   │   ├── global.css
│   │   ├── dashboard.css
│   │   ├── form.css
│   │   └── navbar.css
│   │
│   └── router/
│       ├── AppRouter.jsx
│       └── ProtectedRoute.jsx
│
├── package.json
├── vite.config.js
└── README.md

```
