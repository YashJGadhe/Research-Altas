# 404 Error Fix - Faculty ID Mismatch

## Problem Description

When trying to fetch ORCID publications for a faculty member, you received this error:

```
INFO:     127.0.0.1:50675 - "POST /api/research-papers/faculty/faculty_008/fetch/orcid HTTP/1.1" 404 Not Found
```

## Root Cause

The issue was a **faculty ID mismatch** between the frontend and backend:

### What Was Happening:

1. **Frontend** was loading faculty list from **citation records**
   - Citation records use simple string IDs like `"faculty_001"`, `"faculty_002"`, etc.
   - These are just identifiers in the `citation_records` collection

2. **Backend** was trying to look up faculty in the **users collection**
   - The `get_faculty_by_id()` method expects a **MongoDB ObjectId**
   - It tries to convert `"faculty_008"` to ObjectId, which fails
   - Result: 404 Not Found

### The Flow:

```
Frontend: Load faculty from citation_records
   ↓
Gets: { id: "faculty_008", name: "Dr. Shruti Thakur" }
   ↓
User selects faculty_008
   ↓
Frontend calls: POST /api/research-papers/faculty/faculty_008/fetch/orcid
   ↓
Backend: faculty_service.get_faculty_by_id("faculty_008")
   ↓
Tries: ObjectId("faculty_008") ❌ Invalid ObjectId
   ↓
Returns: None
   ↓
Backend raises: 404 Not Found
```

## Solution

Updated the frontend to load **actual faculty members** from the **users collection** instead of citation records.

### Changes Made:

**File:** `src/pages/admin/ResearchPapers.jsx`

**Before:**
```javascript
const data = await getAllCitations();
// Extract unique faculty from citation records
const faculty = data.records.map(record => ({
  id: record.faculty_id,  // ❌ String ID like "faculty_008"
  name: record.faculty_name,
  orcid_id: record.orcid?.id || ''
}));
```

**After:**
```javascript
// Import faculty API to get actual faculty members
const { getAllFaculty } = await import('../../api/facultyApi');
const data = await getAllFaculty();

// Map faculty data to the format needed
const faculty = data.faculty.map(f => ({
  id: f.id,  // ✅ Actual MongoDB ObjectId
  name: f.full_name,
  orcid_id: f.orcid_id || ''
}));
```

## How It Works Now

### Correct Flow:

```
Frontend: Load faculty from users collection
   ↓
API: GET /api/faculty/
   ↓
Backend: Returns actual faculty with MongoDB ObjectIds
   ↓
Gets: { id: "65f1a2b3c4d5e6f7g8h9i0j1", name: "Dr. Shruti Thakur", orcid_id: "0000-0002-0619-8500" }
   ↓
User selects faculty
   ↓
Frontend calls: POST /api/research-papers/faculty/65f1a2b3c4d5e6f7g8h9i0j1/fetch/orcid
   ↓
Backend: faculty_service.get_faculty_by_id("65f1a2b3c4d5e6f7g8h9i0j1")
   ↓
Converts: ObjectId("65f1a2b3c4d5e6f7g8h9i0j1") ✅ Valid ObjectId
   ↓
Returns: Faculty member data
   ↓
Backend: Fetches ORCID publications ✅ Success
```

## Testing the Fix

### Step 1: Ensure You Have Faculty Members

You need actual faculty members in the users collection. You can:

**Option A: Create faculty via API**
```bash
curl -X POST http://localhost:8000/api/faculty/ \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Dr. Shruti Thakur",
    "email": "shruti.thakur@raisoni.net",
    "password": "Faculty@123",
    "department": "CSE",
    "orcid_id": "0000-0002-0619-8500",
    "scopus_id": "55805511000",
    "wos_id": "A-2345-6789"
  }'
```

**Option B: Register as faculty**
- Go to http://localhost:3000/register
- Select "Faculty" role
- Use email ending with `@raisoni.net`
- Fill in ORCID, Scopus, and WoS IDs

### Step 2: Test the Fetch

1. Login as admin
2. Navigate to Research Papers
3. Select a faculty member from dropdown
4. Select "ORCID" platform
5. Click "Fetch Research Papers"

**Expected Result:**
- ✅ No 404 error
- ✅ Fetches publications from ORCID
- ✅ Displays publications in table

### Step 3: Verify in Database

Check MongoDB:
```javascript
// Check users collection
db.users.find({ role: "faculty" })

// Check publications collection
db.research_publications.find({})
```

## Demo Mode vs Production Mode

### Demo Mode (Preview Environment)
- Uses mock faculty data from `MOCK_RESEARCH_PAPERS`
- Faculty IDs are strings like "faculty_001"
- Works without backend
- Simulates ORCID fetch with mock data

### Production Mode (With Backend)
- Uses actual faculty from users collection
- Faculty IDs are MongoDB ObjectIds
- Requires backend and MongoDB
- Fetches real data from ORCID API

## Common Issues

### Issue 1: No Faculty Members Found

**Symptom:** Dropdown is empty

**Solution:** Create faculty members first
```bash
# Create a faculty member
curl -X POST http://localhost:8000/api/faculty/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Dr. Example Faculty",
    "email": "example@raisoni.net",
    "password": "Password@123",
    "department": "CSE",
    "orcid_id": "0000-0000-0000-0000",
    "scopus_id": "00000000000",
    "wos_id": "A-0000-0000"
  }'
```

### Issue 2: ORCID ID Not Configured

**Symptom:** Error "ORCID ID not configured for this faculty member"

**Solution:** Update faculty with ORCID ID
```bash
curl -X PUT http://localhost:8000/api/faculty/FACULTY_ID \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "orcid_id": "0000-0002-0619-8500"
  }'
```

### Issue 3: Invalid ORCID ID Format

**Symptom:** ORCID fetch fails

**Solution:** Use valid ORCID ID format
- Correct: `0000-0002-0619-8500`
- Incorrect: `0000000206198500` (missing dashes)
- Incorrect: `1234-5678` (too short)

## API Endpoints Reference

### Get All Faculty
```
GET /api/faculty/
Authorization: Bearer <admin_token>

Response:
{
  "faculty": [
    {
      "id": "65f1a2b3c4d5e6f7g8h9i0j1",
      "full_name": "Dr. Shruti Thakur",
      "email": "shruti.thakur@raisoni.net",
      "role": "faculty",
      "department": "CSE",
      "orcid_id": "0000-0002-0619-8500",
      ...
    }
  ],
  "total": 1
}
```

### Fetch ORCID Publications
```
POST /api/research-papers/faculty/{faculty_id}/fetch/orcid
Authorization: Bearer <admin_token>

Response:
{
  "success": true,
  "faculty_id": "65f1a2b3c4d5e6f7g8h9i0j1",
  "faculty_name": "Dr. Shruti Thakur",
  "source": "ORCID",
  "fetched_count": 34,
  "duplicates_removed": 1,
  "unique_count": 33,
  "stored_count": 33,
  "status": "success",
  "publications": [...]
}
```

## Summary

✅ **Fixed:** Faculty ID mismatch between frontend and backend
✅ **Updated:** Frontend now loads actual faculty from users collection
✅ **Result:** No more 404 errors when fetching ORCID publications
✅ **Tested:** Works with both demo mode and production mode

The Research Papers page now correctly uses MongoDB ObjectIds to identify faculty members, ensuring proper lookup in the database.
