# 🌐 ResearchAtlas

**Automated Research & Development Information Management System**

Phase 1: Authentication & Authorization Foundation

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Setup Instructions](#setup-instructions)
5. [Environment Variables](#environment-variables)
6. [Running the Application](#running-the-application)
7. [API Endpoints](#api-endpoints)
8. [Role-Permission Matrix](#role-permission-matrix)
9. [Testing Procedure](#testing-procedure)
10. [Security Checklist](#security-checklist)
11. [Future Module Integration](#future-module-integration)

---

## 🎯 Project Overview

ResearchAtlas is a comprehensive system for managing research and development information. Phase 1 establishes the complete authentication and authorization foundation that all future modules will build upon.

### What's Implemented in Phase 1:
- ✅ Complete user registration with validation
- ✅ JWT-based authentication
- ✅ Role-Based Access Control (RBAC)
- ✅ Admin, Faculty, and Student roles
- ✅ User management APIs (Admin only)
- ✅ Faculty management APIs (Admin only)
- ✅ Protected frontend routes
- ✅ MongoDB database with proper indexing
- ✅ Secure password hashing (bcrypt)
- ✅ Default admin initialization
- ✅ Full API documentation (Swagger/OpenAPI)

---

## 🛠 Tech Stack

### Frontend
| Technology | Purpose |
|-----------|---------|
| React.js 18 | UI Framework |
| Vite | Build Tool |
| React Router DOM 6 | Client-side Routing |
| Axios | HTTP Client |
| Tailwind CSS 4 | Styling |

### Backend
| Technology | Purpose |
|-----------|---------|
| Python 3.10+ | Runtime |
| FastAPI | Web Framework |
| Uvicorn | ASGI Server |
| Pydantic v2 | Validation |
| Motor | Async MongoDB Driver |
| python-jose | JWT Handling |
| passlib/bcrypt | Password Hashing |

### Database
| Technology | Purpose |
|-----------|---------|
| MongoDB | Primary Database |

---

## 📁 Project Structure

```
ResearchAtlas/
├── frontend/                          # (This is the project root)
│   ├── src/
│   │   ├── api/
│   │   │   ├── apiClient.js          # Centralized Axios instance
│   │   │   ├── authApi.js            # Authentication API calls
│   │   │   ├── userApi.js            # User management API calls
│   │   │   └── facultyApi.js         # Faculty management API calls
│   │   ├── components/
│   │   │   ├── ProtectedRoute.jsx    # Auth-required route wrapper
│   │   │   └── RoleRoute.jsx         # Role-specific route wrapper
│   │   ├── context/
│   │   │   └── AuthContext.jsx       # Global auth state provider
│   │   ├── hooks/
│   │   │   └── useAuth.js            # Auth state hook
│   │   ├── pages/
│   │   │   ├── auth/
│   │   │   │   ├── LoginPage.jsx     # Login page
│   │   │   │   └── RegisterPage.jsx  # Registration page
│   │   │   ├── admin/
│   │   │   │   └── AdminDashboard.jsx    # Admin placeholder
│   │   │   ├── faculty/
│   │   │   │   └── FacultyDashboard.jsx  # Faculty placeholder
│   │   │   ├── student/
│   │   │   │   └── StudentDashboard.jsx  # Student placeholder
│   │   │   └── UnauthorizedPage.jsx  # 403 page
│   │   ├── routes/
│   │   │   └── AppRoutes.jsx         # Central route configuration
│   │   ├── utils/
│   │   │   └── constants.js          # Roles, departments, config
│   │   ├── App.tsx                   # Root component
│   │   ├── main.tsx                  # Entry point
│   │   └── index.css                 # Global styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tsconfig.json
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py             # App configuration (env vars)
│   │   │   ├── security.py           # JWT & password hashing
│   │   │   └── dependencies.py       # FastAPI auth dependencies
│   │   ├── database/
│   │   │   ├── database.py           # MongoDB connection
│   │   │   └── init_db.py            # DB initialization & admin setup
│   │   ├── models/
│   │   │   └── user.py               # User document model
│   │   ├── schemas/
│   │   │   ├── auth.py               # Auth request/response schemas
│   │   │   └── user.py               # User management schemas
│   │   ├── routes/
│   │   │   ├── auth.py               # Auth endpoints
│   │   │   ├── user.py               # User management endpoints
│   │   │   └── faculty.py            # Faculty management endpoints
│   │   ├── services/
│   │   │   ├── auth_service.py       # Auth business logic
│   │   │   ├── user_service.py       # User management logic
│   │   │   └── faculty_service.py    # Faculty management logic
│   │   └── main.py                   # FastAPI application entry
│   ├── requirements.txt
│   └── .env.example
│
└── README.md
```

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB 6.0+ (running locally or accessible remotely)
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ResearchAtlas
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env

# Edit .env with your actual values
# IMPORTANT: Change JWT_SECRET_KEY to a strong random value
```

### 3. Frontend Setup

```bash
# Navigate to project root (frontend)
cd ..  # (if you're in backend/)

# Install dependencies
npm install

# The frontend is ready to build
```

### 4. MongoDB Setup

```bash
# If MongoDB is running locally on default port:
# mongodb://localhost:27017

# Verify connection:
mongosh
# Then: use researchatlas; db.stats()
```

---

## 🔐 Environment Variables

### Backend (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `MONGODB_URL` | MongoDB connection string | `mongodb://localhost:27017` |
| `DATABASE_NAME` | Database name | `researchatlas` |
| `JWT_SECRET_KEY` | JWT signing secret (CHANGE THIS!) | `your-random-secret-here` |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration | `60` |
| `DEFAULT_ADMIN_EMAIL` | Initial admin email | `admin@researchatlas.com` |
| `DEFAULT_ADMIN_PASSWORD` | Initial admin password | `Admin@123` |
| `CORS_ORIGINS` | Allowed frontend origins | `http://localhost:5173` |

### Frontend (.env or .env.local)

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API URL | `http://localhost:8000` |

---

## 🚀 Running the Application

### Start MongoDB
```bash
# Ensure MongoDB is running
mongod --dbpath /path/to/data
```

### Start Backend
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will:
1. Connect to MongoDB
2. Create required indexes
3. Initialize the default admin account (if configured)
4. Start serving on http://localhost:8000

API Documentation: http://localhost:8000/docs

### Start Frontend (Development)
```bash
npm run dev
```

Frontend runs on: http://localhost:5173

### Build Frontend (Production)
```bash
npm run build
```

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | Login & get JWT | No |
| GET | `/api/auth/me` | Get current user | Yes (Any role) |

### User Management (Admin Only)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/users/` | List all users | Admin |
| GET | `/api/users/{user_id}` | Get user by ID | Admin |
| PUT | `/api/users/{user_id}` | Update user | Admin |
| DELETE | `/api/users/{user_id}` | Delete user | Admin |

### Faculty Management (Admin Only)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/faculty/` | List all faculty | Admin |
| GET | `/api/faculty/{faculty_id}` | Get faculty by ID | Admin |
| POST | `/api/faculty/` | Create faculty | Admin |
| PUT | `/api/faculty/{faculty_id}` | Update faculty | Admin |
| PATCH | `/api/faculty/{faculty_id}/status` | Toggle active status | Admin |
| DELETE | `/api/faculty/{faculty_id}` | Delete faculty | Admin |

### System

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | API info | No |
| GET | `/health` | Health check | No |
| GET | `/docs` | Swagger UI | No |
| GET | `/redoc` | ReDoc UI | No |

---

## 🔑 Role-Permission Matrix

| Permission | Admin | Faculty | Student |
|-----------|-------|---------|---------|
| Register | ✅ | ✅ | ✅ |
| Login | ✅ | ✅ | ✅ |
| View own profile | ✅ | ✅ | ✅ |
| View all users | ✅ | ❌ | ❌ |
| Manage users | ✅ | ❌ | ❌ |
| View all faculty | ✅ | ❌ | ❌ |
| Create faculty | ✅ | ❌ | ❌ |
| Edit faculty | ✅ | ❌ | ❌ |
| Activate/Deactivate faculty | ✅ | ❌ | ❌ |
| Delete faculty | ✅ | ❌ | ❌ |
| Access Admin Dashboard | ✅ | ❌ | ❌ |
| Access Faculty Dashboard | ❌ | ✅ | ❌ |
| Access Student Dashboard | ❌ | ❌ | ✅ |
| View own publications | — | ✅ (future) | ❌ |
| Search public research | — | — | ✅ (future) |

---

## 🧪 Testing Procedure

### 1. Admin Testing

```bash
# Register as admin (or use default admin from .env)
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test Admin",
    "email": "admin@test.com",
    "password": "Admin@123",
    "confirm_password": "Admin@123",
    "role": "admin",
    "department": "CSE"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "Admin@123"
  }'
# Save the access_token from response

# Get current user
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer <token>"

# List all users
curl http://localhost:8000/api/users/ \
  -H "Authorization: Bearer <token>"

# Create a faculty member
curl -X POST http://localhost:8000/api/faculty/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "full_name": "Dr. Faculty",
    "email": "faculty@test.com",
    "password": "Faculty@123",
    "department": "CSE"
  }'
```

### 2. Faculty Testing

```bash
# Login as faculty
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "faculty@test.com",
    "password": "Faculty@123"
  }'

# Get own profile
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer <faculty_token>"

# Try accessing admin endpoints (should return 403)
curl http://localhost:8000/api/users/ \
  -H "Authorization: Bearer <faculty_token>"
# Expected: 403 Forbidden
```

### 3. Student Testing

```bash
# Register as student
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test Student",
    "email": "student@test.com",
    "password": "Student@123",
    "confirm_password": "Student@123",
    "role": "student",
    "department": "CSE"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@test.com",
    "password": "Student@123"
  }'

# Try accessing admin endpoints (should return 403)
curl http://localhost:8000/api/users/ \
  -H "Authorization: Bearer <student_token>"
# Expected: 403 Forbidden

# Try accessing faculty endpoints (should return 403)
curl http://localhost:8000/api/faculty/ \
  -H "Authorization: Bearer <student_token>"
# Expected: 403 Forbidden
```

### 4. Unauthenticated Testing

```bash
# Try accessing protected endpoints without token
curl http://localhost:8000/api/auth/me
# Expected: 403 or 401

curl http://localhost:8000/api/users/
# Expected: 403 or 401
```

### 5. Frontend Testing

1. Open http://localhost:5173
2. Try accessing /admin-dashboard directly → Redirected to /login
3. Register a new account → Success message → Redirected to /login
4. Login with credentials → Redirected to correct dashboard based on role
5. Try navigating to another role's dashboard → Redirected to /unauthorized
6. Click Logout → Redirected to /login, can't access protected pages

---

## 🔒 Security Checklist

- [x] Passwords hashed with bcrypt (never stored in plain text)
- [x] JWT tokens with expiration
- [x] JWT secret from environment variables (never hardcoded)
- [x] Backend authorization on all protected endpoints
- [x] Role-Based Access Control (RBAC) enforced server-side
- [x] Input validation on all endpoints (Pydantic schemas)
- [x] Email normalization (lowercase, trimmed)
- [x] Password strength validation
- [x] Duplicate email prevention
- [x] No password_hash in API responses
- [x] CORS properly configured
- [x] No sensitive data in frontend code
- [x] No .env files committed to Git
- [x] Proper HTTP status codes (400, 401, 403, 404, 409, 422, 500)
- [x] Global exception handler (no stack traces exposed)
- [x] Protection against IDOR (ownership validation)
- [x] Protection against role escalation (backend enforcement)
- [x] Invalid/expired JWT handling
- [x] Account deactivation support
- [x] Self-deletion/deactivation prevention for admins

---

## 🔮 Future Module Integration

This Phase 1 architecture is designed to be the permanent foundation for all future modules.

### How Future Modules Connect:

#### 1. Admin Dashboard
- Uses existing `require_admin` dependency
- Calls existing user/faculty management APIs
- Adds new admin-specific endpoints using the same auth pattern

#### 2. Faculty Dashboard
- Uses existing `require_faculty` dependency
- Faculty profile references user via `user_id` (string of ObjectId)
- All faculty data scoped to authenticated user's ID

#### 3. Student Dashboard
- Uses existing `require_student` dependency
- Read-only access to public research data
- Search APIs use existing auth middleware

#### 4. Publications Module
- New collection: `publications`
- References faculty via `faculty_id` (user's ObjectId string)
- Protected with `require_faculty` for write, public for read

#### 5. Notifications Module
- New collection: `notifications`
- References users via `user_id`
- Each user only sees their own notifications

#### 6. Research Profiles
- New collection: `faculty_profiles`
- One-to-one with user: `faculty_profiles.user_id` → `users._id`
- Managed by faculty owner + admin

### Adding a New Protected Endpoint:

```python
from app.core.dependencies import require_admin, require_faculty, get_current_user

# Admin-only endpoint
@router.get("/admin-data")
async def admin_data(current_user: dict = Depends(require_admin)):
    # current_user is guaranteed to be an active admin
    ...

# Faculty-only endpoint (returns only own data)
@router.get("/my-publications")
async def my_publications(current_user: dict = Depends(require_faculty)):
    user_id = str(current_user["_id"])
    # Query publications where faculty_id == user_id
    ...

# Any authenticated user
@router.get("/profile")
async def profile(current_user: dict = Depends(get_current_user)):
    ...
```

### Adding a New Frontend Page:

```jsx
// Protected page (any authenticated user)
<Route path="/profile" element={
  <ProtectedRoute><ProfilePage /></ProtectedRoute>
} />

// Role-specific page
<Route path="/admin/reports" element={
  <RoleRoute allowedRoles={[ROLES.ADMIN]}>
    <ReportsPage />
  </RoleRoute>
} />
```

---

## 📄 License

© 2026 ResearchAtlas. All rights reserved.
