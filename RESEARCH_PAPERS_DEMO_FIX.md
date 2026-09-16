# Research Papers - Demo Mode Fix

## Issue
The Research Papers page was not working in demo mode because it was trying to make API calls to the backend, which doesn't exist in the preview environment.

## Solution
Implemented complete demo mode support for the Research Papers page by:

1. **Created Mock Data** (`src/api/mockResearchPapers.js`)
   - Added mock research papers for all 17 faculty members
   - Each faculty has 1-3 sample publications with realistic data
   - Includes all required fields: title, authors, venue, year, DOI, work type, etc.

2. **Updated ResearchPapers.jsx** to support demo mode:
   - `loadFacultyList()` - Uses mock faculty data from mock papers
   - `loadPublications()` - Returns mock papers with filtering and sorting
   - `loadStatistics()` - Calculates statistics from mock data
   - `loadWorkTypes()` - Extracts unique work types from mock data
   - `handleFetchPublications()` - Simulates API call with 1.5s delay
   - `hasOrcidId()` - Returns true in demo mode to enable fetch button

## Demo Mode Features

### Faculty Selection
- All 17 faculty members available in dropdown
- Each has mock ORCID ID (0000-0000-0000-0000)
- Fetch button is enabled for all faculty

### Fetch Publications
- Clicking "Fetch Research Papers" simulates API call
- Shows loading state for 1.5 seconds
- Displays success message with "(Demo Mode)" indicator
- Shows fetch status: fetched count, duplicates removed, unique count

### Publications Table
- Displays mock publications for selected faculty
- Supports all filters:
  - Search (title, authors, venue, DOI)
  - Work type filter
  - Year sorting (newest/oldest first)
- Shows all columns: Sr. No., Title, Authors, Publication, Year, Work Type, DOI, Source, View

### Statistics
- Total publications count
- Publications by source (all ORCID)
- Publications by work type
- Year range (min/max)
- Last fetched timestamp

## Mock Data Structure

Each faculty member has mock publications with:
```javascript
{
  id: 'pub_001_1',
  faculty_id: 'faculty_001',
  faculty_name: 'Dr. Mangala Madankar',
  source: 'ORCID',
  source_work_id: '123456789',
  title: 'Machine Learning Approaches for Predictive Analytics in Healthcare',
  authors: ['Dr. Mangala Madankar', 'Dr. John Smith', 'Prof. Jane Doe'],
  publication_venue: 'International Journal of Healthcare Informatics',
  publication_date: '2024-03-15',
  year: 2024,
  doi: '10.1234/ijhi.2024.001',
  url: 'https://doi.org/10.1234/ijhi.2024.001',
  work_type_raw: 'journal-article',
  work_type: 'Journal Article',
  is_duplicate: false
}
```

## Testing in Demo Mode

1. Login as demo admin (admin@test.com / Admin@123)
2. Navigate to Research Papers page
3. Select any faculty member from dropdown
4. Select "ORCID" platform
5. Click "Fetch Research Papers"
6. Wait for 1.5 second simulated delay
7. View publications table with mock data
8. Try filtering and searching
9. Try sorting by year

## Production Mode

When backend is available:
- All functions automatically use real API calls
- No code changes needed
- Demo mode detection is automatic via `isDemoMode()`

## Files Modified

1. `src/api/mockResearchPapers.js` (NEW)
   - Mock research papers for all 17 faculty
   - Mock fetch result template
   - Mock statistics template

2. `src/pages/admin/ResearchPapers.jsx` (MODIFIED)
   - Added demo mode imports
   - Updated all data loading functions
   - Added demo mode checks
   - Maintained all existing functionality

## Compatibility

- ✅ Works in demo mode (preview environment)
- ✅ Works in production mode (with backend)
- ✅ No breaking changes
- ✅ All existing features preserved
- ✅ Seamless switching between modes

## Future Enhancements

When backend is ready:
- Real ORCID API integration
- Actual publication fetching
- Real duplicate detection
- Persistent storage in MongoDB
- Publication history tracking
