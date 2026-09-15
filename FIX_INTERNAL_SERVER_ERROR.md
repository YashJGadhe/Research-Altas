# 🔧 Internal Server Error - Complete Fix Guide

## ✅ What Was Fixed

I've completely rebuilt all backend files to fix the "Internal Server Error" when logging in as admin. Here are the key fixes:

### 1. **Enhanced Error Handling**
- Added detailed error logging throughout the codebase
- All errors now print to console with full traceback
- Specific error messages instead of generic "Internal Server Error"

### 2. **Database Connection Improvements**
- Added connection timeout settings (5 seconds)
- Added ping test to verify MongoDB connection
- Better error messages if MongoDB is not running

### 3. **Authentication Flow Fixes**
- Fixed response format to match frontend expectations
- Added validation to ensure all required fields are present
- Better handling of missing password_hash field

### 4. **User Model Robustness**
- Safe handling of missing fields (no more KeyError)
- Proper datetime conversion with fallbacks
- Default values for all optional fields

### 5. **JWT Token Handling**
- Better error handling in token creation/verification
- Clear error messages if JWT secret is missing

### 6. **Database Migration**
- Automatic migration of existing users
- Adds missing research ID fields to Phase 1 users
- Updates existing admin with research IDs

## 🚀 How to Run (Step-by-Step)

### Step 1: Start MongoDB
```bash
# Open a new terminal
mongod
```

**Expected output:**
```
{"t":{"$date":"..."},"s":"I",  "c":"NETWORK",  "id":23016, ...}
```

If you see an error like "address already in use", MongoDB is already running.

### Step 2: Navigate to Backend
```bash
cd backend
```

### Step 3: Activate Virtual Environment
```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

**Expected output:**
```
(venv) $
```

If you see an error, create the virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed fastapi-0.115.0 uvicorn-0.30.6 ...
```

### Step 5: Start Backend
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
🚀 Starting ResearchAtlas v1.0.0
📊 Environment: DEBUG
✅ Connected to MongoDB: researchatlas
✅ Database indexes created
✅ No users need migration
ℹ️  Default admin already exists: admin@raisoni.net
✅ Default admin already has all required fields
✅ Database initialization complete
✅ ResearchAtlas started successfully
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 6: Start Frontend (New Terminal)
```bash
# Open another terminal
npm run dev
```

**Expected output:**
```
  VITE v6.4.3  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

### Step 7: Login
1. Open browser: http://localhost:3000/login
2. Enter credentials:
   - **Email:** `admin@raisoni.net`
   - **Password:** `Admin@123`
3. Click "Sign In"

**Expected result:** Redirect to `/admin-dashboard`

## 🐛 Troubleshooting Common Errors

### Error: "Internal Server Error" (500)

**Check the backend terminal for error logs.** You should see something like:
```
[ERROR] Login failed: <specific error message>
Traceback (most recent call last):
  ...
```

**Common causes:**

1. **MongoDB not running**
   ```
   ❌ Failed to connect to MongoDB: Connection refused
   ```
   **Fix:** Start MongoDB with `mongod`

2. **Missing .env file**
   ```
   ⚠️  Using default JWT_SECRET_KEY
   ```
   **Fix:** Copy `.env.example` to `.env`

3. **Admin account missing research IDs**
   ```
   ✅ Updated default admin with research ID fields
   ```
   **Fix:** This is automatic - the migration runs on startup

4. **Password hash missing**
   ```
   [ERROR] Login failed: Invalid email or password
   ```
   **Fix:** Delete and recreate admin:
   ```bash
   # In MongoDB shell
   use researchatlas
   db.users.deleteOne({email: "admin@raisoni.net"})
   ```
   Then restart backend.

### Error: "Cannot connect to server"

**Check:**
1. Backend is running on port 8000
2. Frontend proxy is configured in `vite.config.js`
3. CORS is configured in backend

**Fix:** Check backend terminal for startup messages

### Error: "Invalid email or password"

**Check:**
1. Email is exactly `admin@raisoni.net` (case-insensitive)
2. Password is exactly `Admin@123`
3. Admin account exists in database

**Fix:** Verify in MongoDB:
```bash
mongosh
use researchatlas
db.users.find({email: "admin@raisoni.net"})
```

### Error: "Account is deactivated"

**Fix:** Reactivate admin:
```bash
mongosh
use researchatlas
db.users.updateOne(
  {email: "admin@raisoni.net"},
  {$set: {is_active: true}}
)
```

## 📊 Backend Logs to Watch For

When you start the backend, you should see:

```
🚀 Starting ResearchAtlas v1.0.0
📊 Environment: DEBUG
✅ Connected to MongoDB: researchatlas
✅ Database indexes created
✅ No users need migration  (or "✅ Migrated X existing users")
ℹ️  Default admin already exists: admin@raisoni.net
✅ Default admin already has all required fields
✅ Database initialization complete
✅ ResearchAtlas started successfully
INFO:     Uvicorn running on http://0.0.0.0:8000
```

When you login successfully, you should see:
```
INFO:     127.0.0.1:12345 - "POST /api/auth/login HTTP/1.1" 200 OK
```

When you login fails, you should see:
```
[ERROR] Login failed: <specific error>
INFO:     127.0.0.1:12345 - "POST /api/auth/login HTTP/1.1" 401 Unauthorized
```

## 🔍 Diagnostic Script

Run the diagnostic script to check your setup:
```bash
cd backend
chmod +x diagnose.sh
./diagnose.sh
```

This will check:
- MongoDB is running
- Virtual environment exists
- .env file exists
- Dependencies are installed
- Backend structure is complete

## 📝 Files Modified

All backend files have been rebuilt with better error handling:

| File | Key Changes |
|------|-------------|
| `app/main.py` | Better startup/shutdown error handling |
| `app/core/config.py` | Added default values for all settings |
| `app/core/security.py` | Better JWT error handling |
| `app/core/dependencies.py` | Better authentication error handling |
| `app/database/database.py` | Connection timeout and ping test |
| `app/database/init_db.py` | Better migration and error handling |
| `app/models/user.py` | Safe field access, no KeyError |
| `app/services/auth_service.py` | Better response format validation |
| `app/services/user_service.py` | Better error handling |
| `app/routes/auth.py` | Removed response_model, better validation |
| `app/schemas/auth.py` | No changes (already correct) |
| `.env` | Created with development settings |
| `diagnose.sh` | New diagnostic script |

## ✅ Verification Checklist

After starting the backend, verify:

- [ ] MongoDB is running (`mongod`)
- [ ] Backend starts without errors
- [ ] You see "✅ Connected to MongoDB"
- [ ] You see "✅ Database initialization complete"
- [ ] You see "✅ ResearchAtlas started successfully"
- [ ] Uvicorn is running on port 8000
- [ ] Frontend is running on port 3000
- [ ] You can access http://localhost:8000/docs (Swagger UI)
- [ ] You can login with admin@raisoni.net / Admin@123
- [ ] You are redirected to /admin-dashboard
- [ ] Admin dashboard shows your profile information

## 🎯 Next Steps

Once login works:
1. ✅ Access admin dashboard
2. ✅ Navigate through all admin pages
3. ✅ Test sidebar collapse/expand
4. ✅ Test logout functionality
5. ✅ Test role-based access control
6. ✅ Continue to Phase 3 (Faculty Management)

## 📞 If You Still Have Issues

1. **Check backend terminal** - Look for `[ERROR]` messages
2. **Check browser console** - Press F12, look for errors
3. **Check network tab** - See the actual API response
4. **Test API directly** - Use curl or Postman:
   ```bash
   curl -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@raisoni.net", "password": "Admin@123"}'
   ```
5. **Check MongoDB** - Verify admin account exists:
   ```bash
   mongosh
   use researchatlas
   db.users.find({email: "admin@raisoni.net"})
   ```

## 💡 Pro Tips

1. **Always check backend terminal first** - It has the most detailed error information
2. **Use the diagnostic script** - `./diagnose.sh` checks common issues
3. **Restart everything** - Sometimes a fresh start fixes issues:
   ```bash
   # Stop backend (Ctrl+C)
   # Stop MongoDB (Ctrl+C)
   # Start MongoDB
   mongod
   # Start backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
4. **Clear browser cache** - Sometimes old tokens cause issues
5. **Check .env file** - Make sure it has all required values

The backend is now fully rebuilt with comprehensive error handling. All internal server errors should be resolved!
