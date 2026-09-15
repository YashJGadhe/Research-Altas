# Backend Quick Start Guide

## ✅ All Syntax Errors Fixed

The backend is now ready to run. All Python syntax errors have been resolved.

## 🚀 Start Backend

### Windows PowerShell
```powershell
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Expected Output
```
INFO:     Will watch for changes in these directories: ['...\\backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
🚀 Starting ResearchAtlas v1.0.0
📊 Environment: DEBUG
✅ Connected to MongoDB: researchatlas
✅ Database indexes created
✅ Successfully seeded 17 faculty citation records
✅ Database initialization complete
✅ ResearchAtlas started successfully
INFO:     Application startup complete.
```

## 🧪 Quick Tests

### Test 1: Health Check
```powershell
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "app": "ResearchAtlas",
  "version": "1.0.0"
}
```

### Test 2: API Documentation
Open browser: http://localhost:8000/docs

You should see Swagger UI with all API endpoints listed.

### Test 3: Login
```powershell
curl -X POST http://localhost:8000/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{
    "email": "admin@test.com",
    "password": "Admin@123"
  }'
```

**Expected Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "...",
    "full_name": "Dr. Rajesh Kumar",
    "email": "admin@test.com",
    "role": "admin",
    "department": "CSE",
    "orcid_id": "0000-0002-1825-0097",
    "scopus_id": "55805511000",
    "wos_id": "A-2345-6789"
  }
}
```

### Test 4: Get Citations
```powershell
$token = "YOUR_TOKEN_FROM_ABOVE"
curl http://localhost:8000/api/citations/ `
  -H "Authorization: Bearer $token"
```

**Expected Response:**
```json
{
  "records": [
    {
      "id": "...",
      "faculty_id": "faculty_001",
      "faculty_name": "Dr. Mangala Madankar",
      "web_of_science": {
        "papers": 14,
        "citations": 39,
        "h_index": 4
      },
      ...
    },
    ...
  ],
  "total": 17
}
```

## 🎯 Frontend Integration

### Start Frontend
```powershell
cd ..
npm run dev
```

### Access Application
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Login via Frontend
1. Open http://localhost:3000
2. Click "👑 Login as Admin (Demo)"
3. You'll be redirected to admin dashboard

## 📊 Test All Features

### Citation Management
1. Navigate to "Citation Management"
2. See 17 faculty members with citation data
3. Click "Edit" to modify data
4. Click "History" to view changes
5. Click "Download Excel" to export
6. Click "Fetch" to test ORCID integration

### Research Papers
1. Navigate to "Research Papers"
2. Select a faculty member
3. Select "ORCID" platform
4. Click "Fetch Research Papers"
5. View publications table
6. Try search and filters

## 🔍 Troubleshooting

### Issue: Backend won't start
**Solution:** Check if MongoDB is running
```powershell
mongod
```

### Issue: Port 8000 already in use
**Solution:** Use a different port
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Issue: Import errors
**Solution:** Reinstall dependencies
```powershell
pip install -r requirements.txt
```

### Issue: MongoDB connection failed
**Solution:** Check MongoDB is running
```powershell
mongosh
```

## ✅ Success Indicators

You'll know everything is working when:
- ✅ Backend starts with "Application startup complete"
- ✅ http://localhost:8000/docs shows API documentation
- ✅ http://localhost:8000/health returns healthy status
- ✅ Frontend can login successfully
- ✅ All admin pages load correctly
- ✅ Citation Management shows 17 faculty
- ✅ Research Papers can fetch data

## 📚 Documentation

- **BACKEND_SYNTAX_ERRORS_FIXED.md** - Complete fix documentation
- **ORCID_CONFIG_FIX.md** - ORCID configuration guide
- **PHASE_6_COMPLETE.md** - Citation Management guide
- **PHASE_7_COMPLETE.md** - Research Papers guide

---

**Status: ✅ ALL ERRORS FIXED - BACKEND READY TO RUN**

Start the backend now and test all features! 🚀
