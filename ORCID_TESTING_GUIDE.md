# ORCID Integration Testing Guide

## Overview

This guide explains how to test the ORCID integration in ResearchAtlas. ORCID (Open Researcher and Contributor ID) is a unique identifier for researchers that helps connect research outputs across different platforms.

## What ORCID Integration Does

The ORCID integration allows you to:
- Fetch researcher profile information from ORCID
- Retrieve publication/work data associated with a researcher
- Update citation records with ORCID information
- Track fetch operations in the audit log
- Maintain historical data when records are updated

## Prerequisites

### 1. Backend Server Running

The ORCID integration requires the backend server to be running because:
- API calls are made from the backend (not frontend)
- API credentials are stored securely in backend environment variables
- Data is processed and validated server-side
- Results are stored in MongoDB

**Start the backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. MongoDB Running

Ensure MongoDB is running and accessible:
```bash
# Check if MongoDB is running
mongosh

# Or start MongoDB
mongod --dbpath /path/to/data
```

### 3. Demo Data Loaded

The system should have the 17 faculty demo records loaded. Check the backend logs for:
```
✅ Successfully seeded 17 faculty citation records
```

## ORCID API Configuration

### Option 1: Public API (No Credentials Required)

ORCID provides a free public API that doesn't require authentication for basic read operations. This is sufficient for testing.

**No configuration needed** - the system will use the public API automatically.

### Option 2: Member API (Requires Credentials)

If you have institutional access to ORCID's member API, you can configure credentials for enhanced features.

**Add to `backend/.env`:**
```env
ORCID_CLIENT_ID=your-client-id
ORCID_CLIENT_SECRET=your-client-secret
```

**How to get credentials:**
1. Register at https://orcid.org/develop
2. Create a new application
3. Get your Client ID and Client Secret
4. Add them to your `.env` file

## Testing Steps

### Step 1: Access Citation Management

1. Login as admin (use demo mode or real backend)
2. Navigate to **Admin Dashboard** → **Citation Management**
3. You should see the table with 17 faculty members

### Step 2: Add ORCID ID to a Faculty Member

Before testing ORCID fetch, you need to add an ORCID ID to at least one faculty member.

**Using the UI:**
1. Click **Edit** on any faculty row (e.g., "Dr. Mangala Madankar")
2. In the edit modal, find the **ORCID ID** field
3. Enter a valid ORCID ID (see test IDs below)
4. Click **Save Changes**

**Test ORCID IDs:**
```
0000-0002-1825-0097  # Josiah Carberry (test ORCID)
0000-0001-5109-3700  # Real researcher
0000-0002-4510-0385  # Real researcher
0000-0003-0001-5109  # Real researcher
```

**Using the API directly:**
```bash
# Get admin token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@raisoni.net", "password": "Admin@123"}'

# Update a faculty record with ORCID ID
curl -X PUT http://localhost:8000/api/citations/{record_id} \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "orcid": {
      "id": "0000-0002-1825-0097",
      "url": "https://orcid.org/0000-0002-1825-0097"
    }
  }'
```

### Step 3: Test Individual ORCID Fetch

1. In the Citation Management table, find the faculty member with the ORCID ID
2. Click the **Fetch** button in the Actions column
3. Wait for the fetch to complete (1-2 seconds)
4. A modal will appear showing the fetch result

**Expected Result:**
```
Status: SUCCESS
Message: ORCID data fetched successfully
Faculty: Dr. [Name]
ORCID: 0000-0002-1825-0097
Works Found: [number]
Updated Records: 1
Skipped: 0
Errors: 0
```

**What happens:**
- Backend calls ORCID API with the ORCID ID
- Retrieves researcher profile (name, biography, affiliations)
- Retrieves works/publications list
- Updates the citation record in MongoDB
- Creates a history snapshot if data changed
- Logs the fetch operation

### Step 4: Test Bulk ORCID Fetch

1. Add ORCID IDs to multiple faculty members (repeat Step 2)
2. Click **Fetch All Data** button at the top
3. Wait for the bulk operation to complete
4. Check the success message

**Expected Result:**
```
Fetch complete. Found [total] works, updated [count] records.
```

**What happens:**
- System iterates through all faculty with ORCID IDs
- Fetches ORCID data for each one
- Updates records individually
- Shows summary of total works found and records updated

### Step 5: Verify Data Updates

After fetching ORCID data:

1. **Check the table:**
   - ORCID ID column should show the ID
   - ORCID URL column should show the link (clickable)

2. **Check history:**
   - Click **History** button for the faculty member
   - You should see a new entry with:
     - Source: ORCID
     - Change Source: api
     - Changed fields: orcid.id, orcid.url

3. **Check fetch logs:**
   - Use the API to view fetch logs:
   ```bash
   curl http://localhost:8000/api/citations/logs/fetch \
     -H "Authorization: Bearer {token}"
   ```

## What ORCID Returns

### ✅ Data Provided by ORCID

1. **Researcher Identity:**
   - ORCID ID
   - Full name
   - Biography/bio
   - Credit name

2. **Affiliations:**
   - Employment history
   - Education history
   - Invited positions
   - Distinctions

3. **Works/Publications:**
   - Title
   - Type (journal article, book, etc.)
   - Publication date
   - Journal name
   - DOI (if available)
   - External identifiers

4. **External Identifiers:**
   - DOI links
   - Other researcher IDs
   - URL to ORCID profile

### ❌ Data NOT Provided by ORCID

ORCID does **NOT** provide citation metrics:
- ❌ Citation counts
- ❌ h-index
- ❌ i10-index
- ❌ Impact factors

These metrics must come from other sources:
- Scopus API
- Web of Science API
- Google Scholar (scraping)
- OpenAlex API

## Testing Scenarios

### Scenario 1: Valid ORCID ID

**Test ID:** `0000-0002-1825-0097`

**Expected:**
- ✅ Fetch succeeds
- ✅ Profile data retrieved
- ✅ Works list retrieved
- ✅ Record updated
- ✅ History created

### Scenario 2: Invalid ORCID ID

**Test ID:** `0000-0000-0000-0000`

**Expected:**
- ❌ Fetch fails
- ✅ Error message shown
- ✅ No record update
- ✅ Error logged

### Scenario 3: ORCID ID Without Works

**Test ID:** Any valid ORCID with no publications

**Expected:**
- ✅ Fetch succeeds
- ✅ Profile data retrieved
- ✅ Works count: 0
- ✅ Record updated (ORCID info only)
- ✅ History created

### Scenario 4: Network Error

**Setup:** Stop backend server temporarily

**Expected:**
- ❌ Fetch fails
- ✅ Network error message
- ✅ No record update
- ✅ Error handled gracefully

### Scenario 5: Rate Limiting

**Setup:** Make multiple rapid fetch requests

**Expected:**
- ⚠️ Some requests may be rate-limited
- ✅ System handles 429 responses
- ✅ Retry logic (if implemented)
- ✅ Error message shown

## API Endpoints for Testing

### 1. Fetch ORCID Data for Single Faculty

```bash
POST /api/citations/{record_id}/fetch/orcid
Authorization: Bearer {token}

Response:
{
  "success": true,
  "message": "ORCID data fetched successfully",
  "faculty_id": "faculty_001",
  "source": "ORCID",
  "records_found": 45,
  "records_updated": 1,
  "history_created": 1,
  "data": {
    "orcid_id": "0000-0002-1825-0097",
    "orcid_url": "https://orcid.org/0000-0002-1825-0097",
    "name": "Josiah Carberry",
    "biography": "...",
    "affiliations": [...],
    "works_count": 45,
    "works": [...]
  }
}
```

### 2. Get Fetch Logs

```bash
GET /api/citations/logs/fetch?faculty_id={faculty_id}&limit=50
Authorization: Bearer {token}

Response:
[
  {
    "id": "log_id",
    "faculty_id": "faculty_001",
    "faculty_name": "Dr. Mangala Madankar",
    "source": "ORCID",
    "status": "success",
    "started_at": "2026-03-25T10:00:00Z",
    "completed_at": "2026-03-25T10:00:05Z",
    "records_found": 45,
    "records_updated": 1,
    "error_message": null,
    "triggered_by": "admin@raisoni.net"
  }
]
```

### 3. Get Citation History

```bash
GET /api/citations/{record_id}/history
Authorization: Bearer {token}

Response:
{
  "history": [
    {
      "id": "history_id",
      "citation_record_id": "record_id",
      "faculty_id": "faculty_001",
      "faculty_name": "Dr. Mangala Madankar",
      "snapshot": {
        "orcid": {
          "id": "",
          "url": ""
        }
      },
      "changed_fields": ["orcid.id", "orcid.url"],
      "change_source": "api",
      "source_platform": "ORCID",
      "created_at": "2026-03-25T10:00:05Z",
      "created_by": "admin@raisoni.net"
    }
  ],
  "total": 1
}
```

## Troubleshooting

### Issue 1: "ORCID ID not configured"

**Cause:** Faculty record doesn't have an ORCID ID

**Solution:**
1. Click **Edit** on the faculty row
2. Add ORCID ID in the format: `0000-0000-0000-0000`
3. Save changes
4. Try fetch again

### Issue 2: "Invalid ORCID ID format"

**Cause:** ORCID ID doesn't match the required format

**Solution:**
- Use format: `0000-0000-0000-0000`
- Must be 16 digits with dashes
- Last character can be digit or 'X'

### Issue 3: "Failed to fetch data from ORCID API"

**Cause:** Network error or ORCID API issue

**Solution:**
1. Check if backend server is running
2. Check internet connection
3. Check ORCID API status: https://status.orcid.org/
4. Check backend logs for detailed error

### Issue 4: "ORCID record not found"

**Cause:** ORCID ID doesn't exist in ORCID database

**Solution:**
1. Verify ORCID ID is correct
2. Try a different ORCID ID
3. Check ORCID website: https://orcid.org/

### Issue 5: Fetch succeeds but no data updated

**Cause:** ORCID data matches existing data

**Solution:**
- This is normal behavior
- System only creates history when data changes
- Check fetch logs to confirm operation succeeded

## Demo Mode Testing

If you're using demo mode (no backend), the ORCID fetch will return mock data:

**Expected Behavior:**
- ✅ Fetch button works
- ✅ Simulated delay (1 second)
- ✅ Mock result shown
- ✅ Message: "ORCID data fetched successfully (Demo Mode)"
- ❌ No actual API call
- ❌ No database updates
- ❌ No history created

**To test real ORCID integration:**
1. Start backend server
2. Login with real credentials (not demo mode)
3. Use real ORCID IDs
4. Check MongoDB for actual updates

## Best Practices

### 1. Use Valid ORCID IDs

Always use real, valid ORCID IDs for testing:
- ✅ `0000-0002-1825-0097` (Josiah Carberry - test ORCID)
- ✅ `0000-0001-5109-3700` (Real researcher)
- ❌ `0000-0000-0000-0000` (Invalid)

### 2. Test Incrementally

1. Start with one faculty member
2. Verify fetch works
3. Check data updates
4. Verify history
5. Then test bulk operations

### 3. Monitor Logs

Check backend logs for:
- API call details
- Response data
- Errors
- Database operations

### 4. Verify Data Integrity

After each fetch:
1. Check citation record updated correctly
2. Check history snapshot created
3. Check fetch log created
4. Verify no data loss

### 5. Handle Errors Gracefully

Test error scenarios:
- Invalid ORCID IDs
- Network failures
- API rate limits
- Missing data

## Next Steps After ORCID Testing

Once ORCID integration is verified, you can:

1. **Add More Faculty ORCID IDs**
   - Populate ORCID IDs for all 17 faculty members
   - Test bulk fetch operations

2. **Implement Additional APIs**
   - Scopus API integration
   - Web of Science API integration
   - Google Scholar integration
   - OpenAlex integration

3. **Enhance Features**
   - Automatic periodic fetching
   - Conflict resolution
   - Data validation
   - Advanced reporting

## Support

If you encounter issues:

1. **Check Backend Logs:**
   ```bash
   # Logs are printed to console when running uvicorn
   ```

2. **Check MongoDB:**
   ```bash
   mongosh
   use researchatlas
   db.citation_records.find()
   db.citation_history.find()
   db.citation_fetch_logs.find()
   ```

3. **Check API Documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

4. **Review Code:**
   - Backend: `backend/app/services/orcid_service.py`
   - Backend: `backend/app/routes/citations.py`
   - Frontend: `src/pages/admin/CitationManagement.jsx`

## Summary

ORCID integration testing involves:
1. ✅ Setting up backend and MongoDB
2. ✅ Adding ORCID IDs to faculty records
3. ✅ Testing individual fetch operations
4. ✅ Testing bulk fetch operations
5. ✅ Verifying data updates
6. ✅ Checking history and logs
7. ✅ Testing error scenarios

The integration is working correctly when:
- ORCID API calls succeed
- Data is retrieved and stored
- History snapshots are created
- Fetch logs are recorded
- Error handling works properly

**Status:** Ready for testing! 🚀
