# Phase 6 - Citation Management Implementation Guide

## Overview

Phase 6 implements a comprehensive citation management system with:
- Complete citation tracking for 17 CSE faculty members
- Manual editing with validation
- ORCID API integration (first phase of API integrations)
- Historical data tracking with snapshots
- Previous values display
- Fetch logs for auditing

## Architecture

### Backend Components

#### 1. Models (`backend/app/models/citation.py`)
- **CitationRecord**: Main citation data model
- **CitationHistory**: Historical snapshots of changes
- **CitationFetchLog**: Audit logs for API fetches

#### 2. Schemas (`backend/app/schemas/citation.py`)
- Pydantic schemas for request/response validation
- Ensures data integrity and proper formatting

#### 3. Services
- **CitationService** (`backend/app/services/citation_service.py`): Business logic for citations
- **OrcidService** (`backend/app/services/orcid_service.py`): ORCID API integration

#### 4. Routes (`backend/app/routes/citations.py`)
Admin-only endpoints:
- `GET /api/citations/` - Get all citation records
- `GET /api/citations/{record_id}` - Get specific record
- `GET /api/citations/faculty/{faculty_id}` - Get by faculty ID
- `PUT /api/citations/{record_id}` - Update record (creates history)
- `GET /api/citations/{record_id}/history` - Get history
- `POST /api/citations/{record_id}/fetch/orcid` - Fetch ORCID data
- `GET /api/citations/logs/fetch` - Get fetch logs

### Frontend Components

#### CitationManagement Page (`src/pages/admin/CitationManagement.jsx`)
Features:
- Responsive table with sticky headers and columns
- Color-coded sections (WoS: blue, Scopus: green, Google Scholar: purple)
- Edit modal with validation
- History modal showing all changes
- Fetch result modal
- Bulk fetch functionality
- Individual faculty fetch

#### Citation API Client (`src/api/citationApi.js`)
- All API calls for citation management
- Error handling
- Type safety

## Database Collections

### 1. `citation_records`
Stores current citation data for each faculty member.

**Structure:**
```json
{
  "_id": "ObjectId",
  "faculty_id": "faculty_001",
  "faculty_name": "Dr. Mangala Madankar",
  "web_of_science": {
    "papers": 14,
    "citations": 39,
    "h_index": 4,
    "profile_url": ""
  },
  "scopus": {
    "papers": 46,
    "citations": 285,
    "h_index": 10,
    "profile_url": ""
  },
  "google_scholar": {
    "papers": 80,
    "citations": 541,
    "h_index": 13,
    "i10_index": 15,
    "profile_url": ""
  },
  "publons_url": "",
  "scopus_url": "",
  "google_scholar_url": "",
  "researchgate_url": "",
  "orcid": {
    "id": "",
    "url": ""
  },
  "openalex": {
    "id": "",
    "url": ""
  },
  "source_status": {
    "web_of_science": "not_configured",
    "scopus": "not_configured",
    "google_scholar": "not_configured",
    "orcid": "not_configured",
    "openalex": "not_configured"
  },
  "last_fetched_at": null,
  "created_at": "2026-03-25T10:00:00Z",
  "updated_at": "2026-03-25T10:00:00Z",
  "updated_by": null
}
```

### 2. `citation_history`
Stores snapshots of previous data whenever changes occur.

**Structure:**
```json
{
  "_id": "ObjectId",
  "citation_record_id": "ObjectId",
  "faculty_id": "faculty_001",
  "faculty_name": "Dr. Mangala Madankar",
  "snapshot": {
    "web_of_science": {
      "papers": 14,
      "citations": 39,
      "h_index": 4
    }
  },
  "changed_fields": ["web_of_science.citations"],
  "change_source": "manual",
  "source_platform": "MANUAL",
  "created_at": "2026-03-25T11:00:00Z",
  "created_by": "admin@raisoni.net"
}
```

### 3. `citation_fetch_logs`
Audit logs for API fetch operations.

**Structure:**
```json
{
  "_id": "ObjectId",
  "faculty_id": "faculty_001",
  "faculty_name": "Dr. Mangala Madankar",
  "source": "ORCID",
  "status": "success",
  "started_at": "2026-03-25T11:00:00Z",
  "completed_at": "2026-03-25T11:00:05Z",
  "records_found": 45,
  "records_updated": 1,
  "error_message": null,
  "triggered_by": "admin@raisoni.net"
}
```

## Demo Data

17 CSE faculty members with realistic citation data:

1. Dr. Mangala Madankar
2. Dr. Apeksha Sakhare
3. Dr. Girish Talmale
4. Prof. Prashant K. Khobragade
5. Dr. Atiya Khan
6. Prof. Neha Purohit
7. Dr. Prasad Lokulwar
8. Dr. Shruti Thakur
9. Dr. Sarika Khandelwal
10. Prof. Ashish Soni
11. Prof. Anuradha Joshi
12. Prof. Imran Ahmad
13. Prof. Mrunali Dhone
14. Dr. Aditya Turankar
15. Prof. Sonali Bhardwaj
16. Prof. Wani Bisen
17. Dr. Sonia Bajaj

## ORCID Integration

### Setup

1. **No API Key Required for Public Access**
   - ORCID Public API is free and doesn't require authentication
   - For member API access, register at: https://orcid.org/develop

2. **Configuration** (Optional - for member API)
   Add to `backend/.env`:
   ```
   ORCID_CLIENT_ID=your-client-id
   ORCID_CLIENT_SECRET=your-client-secret
   ```

### How It Works

1. **Fetch ORCID Data**
   - User clicks "Fetch" button for a faculty member
   - Backend calls ORCID API with the faculty's ORCID ID
   - Retrieves: name, biography, affiliations, works/publications
   - Updates citation record with ORCID information
   - Creates history snapshot if data changed
   - Logs the fetch operation

2. **What ORCID Provides**
   - ✅ Researcher identity (name, ORCID ID)
   - ✅ Biography
   - ✅ Affiliations (employment, education)
   - ✅ Works/publications list
   - ✅ DOI identifiers
   - ❌ Citation counts (not provided by ORCID)
   - ❌ h-index (not provided by ORCID)
   - ❌ i10-index (not provided by ORCID)

3. **What ORCID Does NOT Provide**
   - Citation metrics (must come from Scopus, WoS, Google Scholar)
   - h-index calculations
   - i10-index calculations

### Testing ORCID Integration

1. **Add ORCID ID to a Faculty Member**
   - Click "Edit" on a faculty row
   - Enter ORCID ID (format: 0000-0000-0000-0000)
   - Save changes

2. **Fetch ORCID Data**
   - Click "Fetch" button for that faculty member
   - Wait for fetch to complete
   - View result modal showing:
     - Status (SUCCESS/FAILED)
     - Records found (works count)
     - Records updated
     - Retrieved data (name, ORCID ID, works count)

3. **Verify History**
   - Click "History" button
   - See the ORCID fetch entry
   - Shows changed fields and timestamp

### Example ORCID IDs for Testing

You can use these real ORCID IDs for testing:
- `0000-0002-1825-0097` (Josiah Carberry - test ORCID)
- `0000-0001-5109-3700` (Real researcher)
- `0000-0002-4510-0385` (Real researcher)

## Historical Data Tracking

### How It Works

1. **Before Every Update**
   - System compares new data with current data
   - Identifies changed fields
   - Creates snapshot of old data
   - Stores snapshot in `citation_history`

2. **What Gets Tracked**
   - All metric changes (papers, citations, h-index, i10-index)
   - URL changes (profile links)
   - ORCID/OpenAlex ID changes
   - Change source (manual/api)
   - Source platform (ORCID, SCOPUS, WOS, etc.)
   - Who made the change
   - When the change was made

3. **Viewing History**
   - Click "History" button on any faculty row
   - See chronological list of all changes
   - Each entry shows:
     - Timestamp
     - Change source (manual/api)
     - Source platform
     - Changed fields
     - Who made the change

### Example History Entry

```json
{
  "faculty_name": "Dr. Mangala Madankar",
  "snapshot": {
    "google_scholar": {
      "citations": 541
    }
  },
  "changed_fields": ["google_scholar.citations"],
  "change_source": "api",
  "source_platform": "ORCID",
  "created_at": "2026-03-25T11:00:00Z",
  "created_by": "admin@raisoni.net"
}
```

## API Endpoints

### Get All Citations
```http
GET /api/citations/
Authorization: Bearer <admin_token>

Response:
{
  "records": [...],
  "total": 17
}
```

### Get Citation by ID
```http
GET /api/citations/{record_id}
Authorization: Bearer <admin_token>

Response:
{
  "id": "...",
  "faculty_id": "faculty_001",
  "faculty_name": "Dr. Mangala Madankar",
  "web_of_science": {...},
  "scopus": {...},
  "google_scholar": {...},
  ...
}
```

### Update Citation (Manual)
```http
PUT /api/citations/{record_id}
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "web_of_science": {
    "papers": 15,
    "citations": 42,
    "h_index": 4
  }
}

Response:
{
  "id": "...",
  "faculty_name": "Dr. Mangala Madankar",
  "web_of_science": {
    "papers": 15,
    "citations": 42,
    "h_index": 4
  },
  ...
}
```

### Get Citation History
```http
GET /api/citations/{record_id}/history
Authorization: Bearer <admin_token>

Response:
{
  "history": [
    {
      "id": "...",
      "faculty_name": "Dr. Mangala Madankar",
      "snapshot": {...},
      "changed_fields": ["web_of_science.citations"],
      "change_source": "manual",
      "source_platform": "MANUAL",
      "created_at": "2026-03-25T11:00:00Z",
      "created_by": "admin@raisoni.net"
    }
  ],
  "total": 1
}
```

### Fetch ORCID Data
```http
POST /api/citations/{record_id}/fetch/orcid
Authorization: Bearer <admin_token>

Response:
{
  "success": true,
  "message": "ORCID data fetched successfully",
  "faculty_id": "faculty_001",
  "source": "ORCID",
  "records_found": 45,
  "records_updated": 1,
  "history_created": 0,
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

### Get Fetch Logs
```http
GET /api/citations/logs/fetch?faculty_id=faculty_001&limit=50
Authorization: Bearer <admin_token>

Response:
[
  {
    "id": "...",
    "faculty_id": "faculty_001",
    "faculty_name": "Dr. Mangala Madankar",
    "source": "ORCID",
    "status": "success",
    "started_at": "2026-03-25T11:00:00Z",
    "completed_at": "2026-03-25T11:00:05Z",
    "records_found": 45,
    "records_updated": 1,
    "error_message": null,
    "triggered_by": "admin@raisoni.net"
  }
]
```

## Security

### Authorization
- All endpoints require Admin role
- Backend enforces authorization (not just frontend)
- Uses existing `require_admin` dependency

### Data Validation
- All numeric fields must be >= 0
- URLs must be valid format
- ORCID IDs must match format: 0000-0000-0000-0000
- Pydantic schemas enforce validation

### No Sensitive Data Exposure
- API keys stored only in backend .env
- Never exposed to frontend
- Never logged or returned in responses

## Testing

### 1. Test Demo Data Seeding
```bash
# Start backend
cd backend
uvicorn app.main:app --reload

# Check logs for:
# "📊 Seeding demo citation data for 17 CSE faculty members..."
# "✅ Successfully seeded 17 faculty citation records"
```

### 2. Test Citation List
```bash
# Login as admin and get token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@raisoni.net", "password": "Admin@123"}'

# Get all citations
curl http://localhost:8000/api/citations/ \
  -H "Authorization: Bearer <token>"
```

### 3. Test Manual Update
```bash
# Update a citation record
curl -X PUT http://localhost:8000/api/citations/<record_id> \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "web_of_science": {
      "papers": 15,
      "citations": 42,
      "h_index": 4
    }
  }'
```

### 4. Test History
```bash
# Get history for a record
curl http://localhost:8000/api/citations/<record_id>/history \
  -H "Authorization: Bearer <token>"
```

### 5. Test ORCID Fetch
```bash
# First, add ORCID ID to a faculty member via edit
# Then fetch ORCID data
curl -X POST http://localhost:8000/api/citations/<record_id>/fetch/orcid \
  -H "Authorization: Bearer <token>"
```

### 6. Test Frontend
1. Login as admin
2. Navigate to /admin/citations
3. Verify table shows all 17 faculty members
4. Click "Edit" and modify some data
5. Click "History" and verify change is recorded
6. Add ORCID ID to a faculty member
7. Click "Fetch" and verify ORCID data is retrieved
8. Verify fetch result modal shows correct information

## Future Enhancements

### Phase 6B - Scopus Integration
- Add ScopusService
- Implement Scopus API calls
- Fetch citation metrics from Scopus
- Update citation records

### Phase 6C - Web of Science Integration
- Add WOSService
- Implement WoS API calls
- Fetch citation metrics from WoS
- Update citation records

### Phase 6D - Google Scholar Integration
- Add GoogleScholarService
- Implement scraping or API calls
- Fetch citation metrics
- Update citation records

### Phase 6E - OpenAlex Integration
- Add OpenAlexService
- Implement OpenAlex API calls
- Fetch additional metadata
- Update citation records

## Files Created/Modified

### Backend Files Created
1. `backend/app/models/citation.py` - Citation models
2. `backend/app/schemas/citation.py` - Citation schemas
3. `backend/app/services/citation_service.py` - Citation service
4. `backend/app/services/orcid_service.py` - ORCID service
5. `backend/app/routes/citations.py` - Citation routes

### Backend Files Modified
1. `backend/app/main.py` - Added citations router
2. `backend/app/database/init_db.py` - Added demo data seeding
3. `backend/requirements.txt` - Added httpx dependency
4. `backend/.env.example` - Added API credential placeholders

### Frontend Files Created
1. `src/api/citationApi.js` - Citation API client
2. `src/pages/admin/CitationManagement.jsx` - Full implementation

## Environment Variables

Add to `backend/.env` (optional for ORCID member API):
```
ORCID_CLIENT_ID=
ORCID_CLIENT_SECRET=
SCOPUS_API_KEY=
WOS_API_KEY=
OPENALEX_EMAIL=
```

## Dependencies

### Backend
- `httpx==0.27.0` - Async HTTP client for API calls

### Frontend
- No new dependencies (uses existing axios)

## Summary

Phase 6 successfully implements:
✅ Complete citation management system
✅ 17 faculty members with demo data
✅ Manual editing with validation
✅ ORCID API integration
✅ Historical data tracking
✅ Previous values display
✅ Fetch logs for auditing
✅ Responsive table UI
✅ Modal-based editing
✅ History viewing
✅ Fetch result display
✅ Bulk fetch functionality
✅ Proper error handling
✅ Admin-only access
✅ Backend authorization
✅ Data validation
✅ No sensitive data exposure

The system is ready for Phase 6B (Scopus integration) and future API integrations.
