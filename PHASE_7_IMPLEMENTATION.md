# Phase 7 - Research Papers Implementation Guide

## Overview

Phase 7 implements the Research Papers of Faculty module with ORCID publication management, duplicate detection, filtering, and sorting capabilities.

## Architecture

### Backend Components

#### 1. Publication Model (`backend/app/models/publication.py`)
- **Publication**: Main publication data model
- **PublicationHistory**: Tracks changes to publication metadata

**Key Fields:**
- `faculty_id`: Reference to faculty member
- `source`: Data source (ORCID, Scopus, WoS, etc.)
- `source_work_id`: Unique identifier from source
- `title`: Publication title
- `authors`: List of authors
- `publication_venue`: Journal/conference name
- `publication_date`: Publication date
- `year`: Publication year
- `doi`: Digital Object Identifier
- `url`: Publication URL
- `work_type_raw`: Raw work type from source
- `work_type`: Normalized work type for display
- `is_duplicate`: Duplicate flag
- `duplicate_of`: Reference to original publication
- `duplicate_reason`: Reason for duplicate detection

#### 2. Research Paper Service (`backend/app/services/research_paper_service.py`)
- Fetches publications from ORCID
- Normalizes ORCID work data
- Detects and removes duplicates
- Stores publications in MongoDB
- Provides filtering and search functionality

**Key Methods:**
- `fetch_orcid_publications()`: Fetch and store publications
- `_normalize_orcid_works()`: Convert ORCID data to publication format
- `_detect_and_remove_duplicates()`: Duplicate detection logic
- `get_faculty_publications()`: Get publications with filters
- `get_publication_statistics()`: Get publication statistics

#### 3. Research Papers Routes (`backend/app/routes/research_papers.py`)
Admin-only endpoints:
- `POST /api/research-papers/faculty/{faculty_id}/fetch/orcid`: Fetch ORCID publications
- `GET /api/research-papers/faculty/{faculty_id}`: Get publications with filters
- `GET /api/research-papers/faculty/{faculty_id}/statistics`: Get statistics
- `GET /api/research-papers/faculty/{faculty_id}/work-types`: Get available work types
- `GET /api/research-papers/faculty/{faculty_id}/years`: Get available years

### Frontend Components

#### 1. Research Papers API Client (`src/api/researchPaperApi.js`)
- `fetchOrcidPublications()`: Fetch from ORCID
- `getFacultyPublications()`: Get publications with filters
- `getPublicationStatistics()`: Get statistics
- `getFacultyWorkTypes()`: Get work types
- `getFacultyPublicationYears()`: Get years

#### 2. Research Papers Page (`src/pages/admin/ResearchPapers.jsx`)
Complete UI with:
- Faculty selection dropdown
- Platform selection dropdown (ORCID active, others disabled)
- Fetch button with loading state
- Search functionality
- Work type filter
- Year sorting
- Publication table with all required columns
- Fetch status summary
- Error and success messages

## Duplicate Detection Strategy

### Priority Order:
1. **DOI** (if available) - Most reliable identifier
2. **ORCID Work ID** (source_work_id) - Source-specific identifier
3. **Normalized title + year** - Fallback when DOI/ID not available

### Normalization:
- Lowercase text
- Trim whitespace
- Normalize punctuation
- Collapse repeated whitespace
- Normalize DOI case
- Remove URL prefixes from DOIs

### Example:
```
Record A: DOI: 10.20944/preprints202205.0248.v1
Record B: https://doi.org/10.20944/preprints202205.0248.v1
Result: Same publication (DOI match after normalization)
```

## Data Flow

### Fetch Flow:
```
1. Admin selects faculty member
2. Admin selects ORCID platform
3. Admin clicks "Fetch Research Papers"
4. Frontend calls POST /api/research-papers/faculty/{id}/fetch/orcid
5. Backend fetches ORCID data using existing OrcidService
6. Backend normalizes works to publication format
7. Backend detects and removes duplicates
8. Backend stores unique publications in MongoDB (upsert)
9. Backend returns fetch summary
10. Frontend displays results and statistics
```

### Display Flow:
```
1. Admin selects faculty member
2. Frontend calls GET /api/research-papers/faculty/{id}
3. Backend queries MongoDB for non-duplicate publications
4. Backend applies filters (search, work type, year)
5. Backend sorts results
6. Frontend displays publication table
```

## ORCID Data Mapping

### ORCID Work → Publication:
| ORCID Field | Publication Field | Notes |
|-------------|-------------------|-------|
| put-code | source_work_id | Unique ORCID work ID |
| title.title | title | Publication title |
| contributors | authors | List of authors |
| journal-title.value | publication_venue | Journal/conference name |
| publication-date | publication_date | Full date if available |
| publication-date.year | year | Publication year |
| external-ids (doi) | doi | DOI identifier |
| url | url | Publication URL |
| type | work_type_raw, work_type | Work type (raw + normalized) |

### Work Type Normalization:
| ORCID Type | Display Type |
|------------|--------------|
| journal-article | Journal Article |
| conference-paper | Conference Paper |
| book | Book |
| book-chapter | Book Chapter |
| edited-book | Edited Book |
| preprint | Preprint |
| patent | Patent |
| thesis | Thesis |
| report | Report |
| dataset | Dataset |
| other | Other |

## API Examples

### Fetch ORCID Publications

**Request:**
```bash
POST /api/research-papers/faculty/{faculty_id}/fetch/orcid
Authorization: Bearer {admin_token}
```

**Response:**
```json
{
  "success": true,
  "faculty_id": "faculty_008",
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

### Get Publications with Filters

**Request:**
```bash
GET /api/research-papers/faculty/{faculty_id}?search=blockchain&work_type=Conference Paper&sort_by=year_desc
Authorization: Bearer {admin_token}
```

**Response:**
```json
{
  "faculty_id": "faculty_008",
  "faculty_name": "Dr. Shruti Thakur",
  "publications": [
    {
      "id": "pub_id",
      "faculty_id": "faculty_008",
      "faculty_name": "Dr. Shruti Thakur",
      "source": "ORCID",
      "source_work_id": "222527444",
      "title": "Blockchain-Based Solutions for Enhancing Data Security",
      "authors": ["Author 1", "Author 2"],
      "publication_venue": "International Conference",
      "publication_date": "2026",
      "year": 2026,
      "doi": "10.1109/icsscna68616.2026.11546964",
      "url": "https://doi.org/10.1109/icsscna68616.2026.11546964",
      "work_type_raw": "conference-paper",
      "work_type": "Conference Paper",
      "is_duplicate": false,
      "fetched_at": "2026-03-25T10:00:00Z",
      "created_at": "2026-03-25T10:00:00Z",
      "updated_at": "2026-03-25T10:00:00Z"
    }
  ],
  "total": 5
}
```

### Get Publication Statistics

**Request:**
```bash
GET /api/research-papers/faculty/{faculty_id}/statistics
Authorization: Bearer {admin_token}
```

**Response:**
```json
{
  "faculty_id": "faculty_008",
  "faculty_name": "Dr. Shruti Thakur",
  "statistics": {
    "total_publications": 33,
    "by_source": {
      "ORCID": 33
    },
    "by_work_type": {
      "Conference Paper": 15,
      "Journal Article": 12,
      "Book Chapter": 4,
      "Preprint": 2
    },
    "year_range": {
      "min": 2020,
      "max": 2026
    },
    "last_fetched": "2026-03-25T10:00:00Z"
  }
}
```

## UI Features

### Faculty Selection
- Dropdown with all 17 CSE faculty members
- Shows faculty name
- Validates ORCID ID availability

### Platform Selection
- ORCID: Active and functional
- Scopus: Disabled (Coming Soon)
- Web of Science: Disabled (Coming Soon)
- Google Scholar: Disabled (Coming Soon)
- OpenAlex: Disabled (Coming Soon)

### Fetch Button
- Disabled until faculty selected
- Disabled if ORCID ID not configured
- Shows loading spinner during fetch
- Displays success/error messages

### Filters
- **Search**: Searches title, authors, venue, DOI
- **Work Type**: Filters by publication type
- **Sort**: Newest first or oldest first

### Publication Table
Columns:
1. **Sr. No.**: Sequential number
2. **Title**: Full publication title (with tooltip for long titles)
3. **Authors**: Author list (shows first 2 + "et al." if more)
4. **Publication**: Journal/conference name
5. **Year**: Publication year
6. **Work Type**: Normalized work type (badge)
7. **DOI**: Clickable DOI link
8. **Source**: Data source (badge)
9. **View**: Link to publication URL

### Fetch Status Summary
Shows after fetch:
- Faculty name
- Platform
- Fetch status
- Last fetched date
- Fetched count
- Duplicates removed
- Unique publications

## Database Collections

### research_publications
Stores all publication records.

**Indexes:**
- `faculty_id`: For faculty-specific queries
- `source`: For source-specific queries
- `source_work_id`: For duplicate detection
- `doi`: For duplicate detection
- `year`: For sorting
- `work_type`: For filtering
- Compound: `(faculty_id, source, source_work_id)` for upsert
- Compound: `(faculty_id, source, doi)` for upsert

### research_publication_history
Tracks changes to publication metadata.

**Fields:**
- `publication_id`: Reference to publication
- `faculty_id`: Faculty member ID
- `source`: Data source
- `old_data`: Previous publication data
- `new_data`: Updated publication data
- `changed_fields`: List of changed fields
- `changed_at`: Timestamp of change
- `changed_by`: User who made change

## Testing Scenarios

### Test 1: Fetch ORCID Publications
1. Login as admin
2. Navigate to Research Papers
3. Select "Dr. Shruti Thakur"
4. Select "ORCID" platform
5. Click "Fetch Research Papers"
6. Verify fetch status shows:
   - Fetched: 34
   - Duplicates Removed: 1
   - Unique Publications: 33
7. Verify table displays 33 publications

### Test 2: Duplicate Detection
1. Fetch publications twice
2. Verify no duplicate records created
3. Verify counts remain same
4. Check MongoDB for unique records

### Test 3: Search Functionality
1. Fetch publications for a faculty
2. Search for "blockchain"
3. Verify only matching publications shown
4. Clear search
5. Verify all publications shown

### Test 4: Work Type Filter
1. Fetch publications
2. Filter by "Conference Paper"
3. Verify only conference papers shown
4. Clear filter
5. Verify all publications shown

### Test 5: Year Sorting
1. Fetch publications
2. Sort by "Newest First"
3. Verify 2026 publications at top
4. Sort by "Oldest First"
5. Verify oldest publications at top

### Test 6: Re-fetch Behavior
1. Fetch publications (first time)
2. Note counts
3. Fetch again (second time)
4. Verify same counts
5. Verify no duplicate MongoDB records

## Security

### Backend Authorization
- All endpoints require Admin role
- Uses existing `require_admin` dependency
- Faculty-specific data enforced by `faculty_id`

### API Keys
- ORCID credentials stored in backend `.env`
- Never exposed to frontend
- Never logged or returned in responses

### Data Validation
- Faculty ID validated before operations
- ORCID ID format validated
- Publication data validated before storage

## Error Handling

### Backend Errors
- Faculty not found: 404
- ORCID ID not configured: 400
- ORCID API failure: 500 with error message
- Database error: 500 with error message

### Frontend Errors
- Network errors: User-friendly message
- API errors: Display error detail
- Validation errors: Inline validation messages

## Future Enhancements

### Phase 7B: Scopus Integration
- Add Scopus API service
- Fetch publications from Scopus
- Map Scopus data to publication model
- Handle Scopus-specific metadata

### Phase 7C: Web of Science Integration
- Add WoS API service
- Fetch publications from WoS
- Map WoS data to publication model
- Handle WoS-specific metadata

### Phase 7D: Google Scholar Integration
- Add Google Scholar scraping/API
- Fetch publications from Google Scholar
- Map Google Scholar data to publication model
- Handle Google Scholar-specific metadata

### Phase 7E: OpenAlex Integration
- Add OpenAlex API service
- Fetch publications from OpenAlex
- Map OpenAlex data to publication model
- Handle OpenAlex-specific metadata

### Phase 7F: Advanced Features
- Publication citation counts (from Scopus/WoS)
- Publication impact metrics
- Co-author network analysis
- Publication trend analysis
- Export to Excel/PDF

## Files Created

### Backend (3 files)
1. `backend/app/models/publication.py` - Publication models
2. `backend/app/services/research_paper_service.py` - Publication service
3. `backend/app/routes/research_papers.py` - Publication routes

### Backend Modified (1 file)
1. `backend/app/main.py` - Added research papers router

### Frontend (2 files)
1. `src/api/researchPaperApi.js` - Publication API client
2. `src/pages/admin/ResearchPapers.jsx` - Publication page

### Documentation (1 file)
1. `PHASE_7_IMPLEMENTATION.md` - This file

## Dependencies

### Backend
- Uses existing `httpx` for ORCID API calls
- Uses existing `pymongo` for MongoDB operations
- No new dependencies required

### Frontend
- Uses existing React and Tailwind CSS
- No new dependencies required

## Summary

Phase 7 successfully implements:
✅ Research Papers page with faculty selection
✅ ORCID publication fetching
✅ Duplicate detection and removal
✅ Publication storage in MongoDB
✅ Search functionality
✅ Work type filtering
✅ Year sorting
✅ Professional publication table
✅ Fetch status summary
✅ Error handling
✅ Admin-only access
✅ Backend authorization
✅ Data validation
✅ No fake data
✅ Re-fetch without duplicates

The system is ready for Phase 7B (Scopus integration) and future platform integrations.
