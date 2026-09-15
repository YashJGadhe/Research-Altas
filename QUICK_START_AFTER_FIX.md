# Quick Start - Backend After ORCID Fix

## ✅ Fix Applied

The ORCID configuration error has been fixed. The Settings class now accepts `ORCID_CLIENT_ID` and `ORCID_CLIENT_SECRET` fields.

## 🚀 Start Backend

### Step 1: Activate Virtual Environment

```bash
cd backend
source venv/bin/activate
```

**On Windows PowerShell:**
```powershell
cd backend
.\venv\Scripts\activate
```

### Step 2: Start the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Verify Startup

You should see:

```
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

```bash
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

You should see Swagger UI with all API endpoints.

### Test 3: Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
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
    ...
  }
}
```

### Test 4: Get Citations

```bash
TOKEN="your_token_from_above"
curl http://localhost:8000/api/citations/ \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response:**
```json
{
  "records": [
    {
      "id": "...",
      "faculty_id": "faculty_001",
      "faculty_name": "Dr. Mangala Madankar",
      "web_of_science": {...},
      "scopus": {...},
      "google_scholar": {...},
      ...
    },
    ...
  ],
  "total": 17
}
```

## 🎯 Frontend Integration

### Start Frontend

In a new terminal:

```bash
npm run dev
```

### Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Login via Frontend

1. Open http://localhost:3000
2. Click "👑 Login as Admin (Demo)"
3. You'll be redirected to admin dashboard

## 🔍 ORCID Configuration

### Current Status

Your `.env` file has ORCID credentials:
```env
ORCID_CLIENT_ID=APP-LG6L9FY9IXCZIU1N
ORCID_CLIENT_SECRET=2e1a0273-278a-4c8e-968b-0e56816af914
```

### Test ORCID Integration

1. Login as admin
2. Navigate to **Citation Management**
3. Select a faculty member (e.g., Dr. Shruti Thakur)
4. Click **Edit**
5. Add ORCID ID: `0000-0002-0619-8500`
6. Save changes
7. Click **Fetch** button
8. Wait for ORCID data to be retrieved

**Expected Result:**
- Fetch status shows "Success"
- ORCID profile data is retrieved
- Publication data is fetched

### If ORCID Credentials Are Invalid

If you get ORCID API errors (401, 403):

1. Go to https://orcid.org/develop
2. Verify your credentials
3. Update `.env` file with correct credentials
4. Restart backend

### Demo Mode (No ORCID)

If you want to test without ORCID:

1. Remove ORCID credentials from `.env`:
   ```env
   ORCID_CLIENT_ID=
   ORCID_CLIENT_SECRET=
   ```

2. Restart backend

3. Application will use mock data for testing

## 📊 Verify All Features

### Citation Management
- ✅ View 17 faculty members
- ✅ Edit citation data
- ✅ View history
- ✅ Download Excel
- ✅ Fetch ORCID data (if credentials valid)

### Research Papers
- ✅ Select faculty member
- ✅ Fetch publications from ORCID
- ✅ View publications table
- ✅ Search and filter
- ✅ Sort by year

### Admin Dashboard
- ✅ View admin profile
- ✅ Navigate to all modules
- ✅ Sidebar navigation
- ✅ Logout functionality

## 🐛 Troubleshooting

### Issue: Port 8000 already in use

**Solution:**
```bash
# Find process using port 8000
# On Windows PowerShell:
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <process_id> /F

# Or use a different port
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Issue: MongoDB not running

**Solution:**
```bash
# Start MongoDB
mongod

# Or check if it's running
mongosh
```

### Issue: Import errors

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: ORCID API errors

**Solution:**
- Check credentials in `.env`
- Verify credentials at https://orcid.org/develop
- Test with demo mode (empty credentials)

## ✅ Success Indicators

You'll know everything is working when:

1. ✅ Backend starts with "Application startup complete"
2. ✅ http://localhost:8000/docs shows API documentation
3. ✅ http://localhost:8000/health returns healthy status
4. ✅ Frontend can login successfully
5. ✅ All admin pages load correctly
6. ✅ Citation Management shows 17 faculty
7. ✅ Research Papers can fetch data (if ORCID credentials valid)

## 📚 Documentation

- **ORCID_CONFIG_FIX.md** - Detailed fix documentation
- **QUICK_START_BACKEND.md** - Backend quick start guide
- **PHASE_6_COMPLETE.md** - Citation Management guide
- **PHASE_7_COMPLETE.md** - Research Papers guide

---

**Status: ✅ ORCID CONFIGURATION FIXED - BACKEND READY TO RUN**

Start the backend now and test all features! 🚀
