# Registration Error Fix - Troubleshooting Guide

## Issues Fixed

### 1. **CORS/Proxy Configuration**
- **Problem**: Frontend was trying to connect directly to `http://localhost:8000` which caused CORS errors
- **Solution**: Added proxy configuration in `vite.config.js` to forward `/api` requests to the backend
- **Changed**: `API_BASE_URL` from `http://localhost:8000` to empty string (relative URL)

### 2. **Error Handling Improvements**
- **Backend**: Added detailed error logging and better error messages
- **Frontend**: Enhanced error display to show specific validation errors from the backend
- **Added**: Console logging for debugging registration errors

## How to Test Registration

### Prerequisites
1. **Start MongoDB**:
   ```bash
   mongod
   ```

2. **Start Backend** (in a new terminal):
   ```bash
   cd backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Start Frontend** (in another terminal):
   ```bash
   npm run dev
   ```

### Registration Steps

1. Open browser to `http://localhost:3000`
2. Click "Register here" or navigate to `/register`
3. Select role tab (Student, Faculty, or Admin)
4. Fill in the form:

#### For Student Registration:
- **Full Name**: Any name (e.g., "John Student")
- **Email**: Must end with `@ghrce.raisoni.net` (e.g., `john@ghrce.raisoni.net`)
- **Department**: Select "CSE"
- **ORCID ID**: Format `0000-0000-0000-0000` (e.g., `1234-5678-9012-3456`)
- **Scopus ID**: 5-15 digits (e.g., `55555555555`)
- **WoS ID**: Format `A-0000-0000` (e.g., `A-1234-5678`)
- **Password**: Minimum 8 characters with uppercase, lowercase, number, and special character (e.g., `Student@123`)
- **Confirm Password**: Must match password

#### For Faculty Registration:
- **Email**: Must end with `@raisoni.net` (e.g., `prof@raisoni.net`)
- All other fields same as student

#### For Admin Registration:
- **Email**: Must end with `@raisoni.net` (e.g., `admin@raisoni.net`)
- All other fields same as student

### Expected Behavior

✅ **Success**: Green message "Registration successful! Redirecting to login..."
✅ **Redirect**: Automatically redirected to login page after 2 seconds
✅ **Login**: Can now login with registered credentials

### Common Errors and Solutions

#### ❌ "Cannot connect to server"
- **Cause**: Backend not running or MongoDB not started
- **Solution**: 
  1. Start MongoDB: `mongod`
  2. Start backend: `uvicorn app.main:app --reload --port 8000`
  3. Check backend is running at `http://localhost:8000/docs`

#### ❌ "Students must register with a @ghrce.raisoni.net email address"
- **Cause**: Wrong email domain for selected role
- **Solution**: Use correct email domain:
  - Student: `@ghrce.raisoni.net`
  - Faculty: `@raisoni.net`
  - Admin: `@raisoni.net`

#### ❌ "An account with this email already exists"
- **Cause**: Email already registered
- **Solution**: Use a different email or login with existing credentials

#### ❌ "Invalid ORCID ID format"
- **Cause**: ORCID ID doesn't match required format
- **Solution**: Use format `0000-0000-0000-0000` (16 digits with dashes)

#### ❌ "Invalid Scopus ID"
- **Cause**: Scopus ID is not 5-15 digits
- **Solution**: Enter only numeric digits (e.g., `55555555555`)

#### ❌ "Invalid Web of Science ID format"
- **Cause**: WoS ID doesn't match required format
- **Solution**: Use format `A-0000-0000` or alphanumeric 5-20 characters

#### ❌ "Password must be at least 8 characters..."
- **Cause**: Password doesn't meet strength requirements
- **Solution**: Include uppercase, lowercase, number, and special character (@$!%*?&)

## Debugging Tips

### Check Browser Console
1. Open Developer Tools (F12)
2. Go to Console tab
3. Look for error messages when registration fails
4. Check Network tab for API request/response details

### Check Backend Logs
1. Look at the terminal where backend is running
2. You should see detailed error messages like:
   ```
   Registration error: <specific error>
   ```

### Test API Directly
Test the registration endpoint directly with curl:

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test Student",
    "email": "test@ghrce.raisoni.net",
    "password": "Student@123",
    "confirm_password": "Student@123",
    "role": "student",
    "department": "CSE",
    "orcid_id": "1234-5678-9012-3456",
    "scopus_id": "55555555555",
    "wos_id": "A-1234-5678"
  }'
```

Expected response:
```json
{
  "message": "Registration successful. You can now login.",
  "success": true
}
```

## Files Modified

1. **vite.config.js**: Added proxy configuration for `/api` routes
2. **src/utils/constants.js**: Changed `API_BASE_URL` to empty string for relative URLs
3. **src/pages/auth/RegisterPage.jsx**: Enhanced error handling and display
4. **backend/app/routes/auth.py**: Added detailed error logging and messages

## Next Steps

After successful registration:
1. Login with your credentials
2. You should be redirected to the appropriate dashboard based on your role
3. Your profile information including ORCID, Scopus, and WoS IDs will be displayed

## Support

If you continue to experience issues:
1. Check that MongoDB is running
2. Check that backend is running on port 8000
3. Check browser console for JavaScript errors
4. Check backend terminal for Python errors
5. Try the curl command above to test the API directly
