# ResearchAtlas Backend - Unified Researcher/Publication System

## Overview

Complete backend implementation for fetching researcher publications from 4 platforms:
- **ORCID** - Public API (no key required for basic access)
- **Scopus** - Uses Search API with AU-ID query
- **Google Scholar** - Uses scholarly library (web scraping)
- **Web of Science** - Uses Clarivate API (requires institutional access)

All platforms return data in a **unified normalized format** that can be displayed in the same frontend table.

## Architecture

```
backend/
├── app/
│   ├── core/
│   │   └── config.py              # Configuration settings
│   ├── database/
│   │   ├── mongodb.py             # MongoDB connection
│   │   └── indexes.py             # Database indexes
│   ├── models/
│   │   └── publication.py         # Unified publication model
│   ├── sources/
│   │   ├── orcid/
│   │   │   └── service.py         # ORCID API service
│   │   ├── scopus/
│   │   │   └── service.py         # Scopus API service
│   │   ├── google_scholar/
│   │   │   └── service.py         # Google Scholar service
│   │   └── wos/
│   │       └── service.py         # Web of Science service
│   ├── services/
│   │   └── researcher_service.py  # Unified service coordinator
│   ├── routes/
│   │   └── researchers.py         # API endpoints
│   └── main.py                    # FastAPI application
├── requirements.txt
└── .env.example
```

## Unified Publication Format

All platforms normalize their data into this common structure:

```json
{
  "source": "ORCID|Scopus|Google Scholar|Web of Science",
  "paper_name": "Publication Title",
  "year": 2024,
  "date": "2024-05-12",
  "author_name": "Author Name",
  "work_type": "journal-article",
  "doi": "10.xxxx/xxxxx",
  "url": "https://...",
  "citation_count": 42,
  "publication_name": "Journal Name",
  "scopus_id": "1-s2.0-xxx",
  "wos_id": "WOS:xxx",
  "issn": "xxxx-xxxx",
  "eissn": "xxxx-xxxx",
  "isbn": null,
  "volume": "10",
  "issue": "2",
  "pages": "10-20",
  "publisher": "Publisher Name"
}
```

**Note:** Fields not provided by a platform will be `null`.

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

**Required API Keys:**
- `SCOPUS_API_KEY` - Get from https://dev.elsevier.com/
- `WOS_API_KEY` - Get from Clarivate (institutional access required)
- `ORCID_CLIENT_ID` and `ORCID_CLIENT_SECRET` - Optional (for member API)

**Google Scholar** doesn't require an API key (uses web scraping).

### 3. Start MongoDB

```bash
# If using local MongoDB
mongod

# Or use Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### 4. Run Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API documentation will be available at: http://localhost:8000/docs

## API Endpoints

### Search Researcher

**POST** `/api/researchers/search`

**Request Body:**
```json
{
  "orcid": "0000-0002-1825-0097",
  "scopus_author_id": "57487968600",
  "google_scholar_author_id": "JicYPdAAAAAJ",
  "wos_researcher_id": "A-1234-5678"
}
```

**Response:**
```json
{
  "researcher_ids": {
    "orcid": "0000-0002-1825-0097",
    "scopus_author_id": "57487968600",
    "google_scholar_author_id": "JicYPdAAAAAJ",
    "wos_researcher_id": "A-1234-5678"
  },
  "sources": {
    "ORCID": {
      "status": "success",
      "publications_count": 45,
      "error": null
    },
    "Scopus": {
      "status": "success",
      "publications_count": 38,
      "error": null
    },
    "Google Scholar": {
      "status": "success",
      "publications_count": 52,
      "error": null
    },
    "Web of Science": {
      "status": "success",
      "publications_count": 30,
      "error": null
    }
  },
  "publications": [
    {
      "source": "ORCID",
      "paper_name": "Research Paper Title",
      "year": 2024,
      "date": "2024-05-12",
      "author_name": "Author Name",
      "work_type": "journal-article",
      "doi": "10.xxxx/xxxxx",
      "url": "https://...",
      "citation_count": null,
      "publication_name": "Journal Name",
      "scopus_id": null,
      "wos_id": null,
      "issn": "xxxx-xxxx",
      "eissn": null,
      "isbn": null,
      "volume": "10",
      "issue": "2",
      "pages": "10-20",
      "publisher": "Publisher"
    }
  ],
  "columns": [
    "source", "paper_name", "year", "date", "author_name", "work_type",
    "doi", "url", "citation_count", "publication_name", "scopus_id",
    "wos_id", "issn", "eissn", "isbn", "volume", "issue", "pages", "publisher"
  ],
  "total_publications": 165,
  "mongodb": {
    "saved": true,
    "researcher_key": "orcid:0000-0002-1825-0097|scopus:57487968600",
    "publications_saved": 165,
    "error": null
  }
}
```

**GET** `/api/researchers/search` - Same endpoint using query parameters

```
GET /api/researchers/search?orcid=0000-0002-1825-0097&scopus_author_id=57487968600
```

## Platform-Specific Notes

### ORCID
- **API:** Public API (no key required)
- **Citation Count:** NOT provided (always `null`)
- **Data Quality:** High (curated by researchers)
- **Rate Limit:** Generous for public API

### Scopus
- **API:** Search API with AU-ID query
- **Citation Count:** ✅ Provided
- **Data Quality:** High (curated by Elsevier)
- **Rate Limit:** Depends on API key tier
- **Note:** Uses Search API, not Author Retrieval (which returns 401)

### Google Scholar
- **API:** Web scraping via scholarly library
- **Citation Count:** ✅ Provided
- **Data Quality:** Variable (automated extraction)
- **Rate Limit:** Aggressive (may be blocked)
- **Note:** No official API, may be unstable

### Web of Science
- **API:** Clarivate Starter API
- **Citation Count:** ✅ Provided
- **Data Quality:** High (curated by Clarivate)
- **Rate Limit:** Depends on institutional access
- **Note:** Requires institutional API access

## MongoDB Collections

### 1. `researchers`
Stores researcher metadata and sync status.

```json
{
  "researcher_key": "orcid:0000-0002-1825-0097|scopus:57487968600",
  "identifiers": {
    "orcid": "0000-0002-1825-0097",
    "scopus_author_id": "57487968600",
    "google_scholar_author_id": "JicYPdAAAAAJ",
    "wos_researcher_id": "A-1234-5678"
  },
  "profile_urls": {
    "orcid": "https://orcid.org/0000-0002-1825-0097",
    "scopus": "https://www.scopus.com/authid/detail.uri?authorId=57487968600",
    "google_scholar": "https://scholar.google.com/citations?user=JicYPdAAAAAJ",
    "wos": "https://www.webofscience.com/wos/author/record/A-1234-5678"
  },
  "platforms": {
    "ORCID": {"status": "success", "publications_count": 45, "error": null},
    "Scopus": {"status": "success", "publications_count": 38, "error": null}
  },
  "last_synced_at": "2024-01-15T10:30:00Z",
  "sync_status": "success",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### 2. `publications`
Stores individual publications with platform-specific data.

```json
{
  "researcher_key": "orcid:0000-0002-1825-0097",
  "platform": "ORCID",
  "source_record_id": "doi:10.xxxx/xxxxx",
  "title": "Research Paper Title",
  "authors": "Author Name",
  "publication_year": 2024,
  "publication_date": "2024-05-12",
  "work_type": "journal-article",
  "doi": "10.xxxx/xxxxx",
  "url": "https://...",
  "citation_count": null,
  "issn": "xxxx-xxxx",
  "eissn": null,
  "isbn": null,
  "volume": "10",
  "issue": "2",
  "pages": "10-20",
  "publisher": "Publisher Name",
  "publication_name": "Journal Name",
  "scopus_id": null,
  "wos_id": null,
  "platform_data": {},
  "raw_data": {...},
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### 3. `sync_logs`
Tracks sync operations for auditing.

```json
{
  "researcher_key": "orcid:0000-0002-1825-0097",
  "synced_at": "2024-01-15T10:30:00Z",
  "platforms": {
    "ORCID": {"status": "success", "publications_count": 45, "error": null}
  },
  "total_publications": 165,
  "publications_saved": 165
}
```

## Duplicate Handling

### Within Same Platform
- Uses `source_record_id` for deduplication
- Priority: DOI > platform-specific ID > title+year
- Upsert operation prevents duplicates

### Across Platforms
- Each platform maintains separate records
- Citation counts remain platform-specific
- DOI can be used for cross-platform matching later
- No automatic merging (preserves data integrity)

## Testing

### Test with Real Data

```bash
# Test ORCID
curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{
    "orcid": "0000-0002-1825-0097"
  }'

# Test Scopus
curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{
    "scopus_author_id": "57487968600"
  }'

# Test Multiple Platforms
curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{
    "orcid": "0000-0002-1825-0097",
    "scopus_author_id": "57487968600",
    "google_scholar_author_id": "JicYPdAAAAAJ"
  }'
```

### Expected Results

**ORCID:**
- ✅ Should fetch publications
- ✅ Citation count will be `null`
- ✅ High data quality

**Scopus:**
- ✅ Should fetch publications (if API key valid)
- ✅ Citation count will be provided
- ✅ Uses Search API (not Author Retrieval)

**Google Scholar:**
- ✅ Should fetch publications
- ✅ Citation count will be provided
- ⚠️ May be rate-limited or blocked

**Web of Science:**
- ✅ Should fetch publications (if API key valid)
- ✅ Citation count will be provided
- ⚠️ Requires institutional access

## Error Handling

The system handles errors gracefully:

1. **Platform Failure:** If one platform fails, others continue
2. **Partial Success:** Returns data from successful platforms
3. **Error Messages:** Clear error messages for each platform
4. **MongoDB Persistence:** Saves whatever data was successfully fetched

Example response with partial failure:

```json
{
  "sources": {
    "ORCID": {"status": "success", "publications_count": 45, "error": null},
    "Scopus": {"status": "failed", "publications_count": 0, "error": "Invalid API key"},
    "Google Scholar": {"status": "success", "publications_count": 52, "error": null}
  },
  "total_publications": 97
}
```

## Frontend Integration

The backend returns data in a format compatible with the existing frontend table:

1. **Columns:** Standardized column names
2. **Publications:** Array of normalized publication objects
3. **Sources:** Status of each platform fetch
4. **Total Count:** Total publications across all platforms

The frontend can:
- Display all publications in a single table
- Filter by source platform
- Sort by year, citations, etc.
- Show platform-specific citation counts
- Handle null values gracefully

## Performance Considerations

1. **Parallel Fetching:** All platforms fetch in parallel using `asyncio.gather()`
2. **Pagination:** Scopus and WoS handle pagination automatically
3. **Rate Limiting:** Google Scholar may be rate-limited
4. **Caching:** Consider adding Redis caching for frequently accessed researchers
5. **Timeout:** 30-second timeout per platform request

## Security Notes

1. **API Keys:** Stored in `.env` file, never committed to git
2. **CORS:** Configured to allow frontend origins
3. **Input Validation:** Pydantic models validate all inputs
4. **Error Messages:** Don't expose sensitive information

## Future Enhancements

1. **Cross-Platform Deduplication:** Match publications across platforms using DOI
2. **Citation Merging:** Combine citation counts from multiple platforms
3. **Author Disambiguation:** Handle name variations
4. **Full-Text Search:** Add Elasticsearch for publication search
5. **Batch Processing:** Fetch multiple researchers at once
6. **Scheduled Sync:** Automatic periodic updates
7. **Analytics Dashboard:** Publication trends, collaboration networks

## Troubleshooting

### MongoDB Connection Issues
```bash
# Check if MongoDB is running
mongosh

# Check connection string in .env
MONGODB_URL=mongodb://localhost:27017
```

### Scopus API Issues
```bash
# Verify API key
curl -H "X-ELS-APIKey: YOUR_KEY" \
  "https://api.elsevier.com/content/search/scopus?query=AU-ID(57487968600)"
```

### Google Scholar Blocking
- Reduce request frequency
- Use proxy/VPN if blocked
- Consider alternative data source

### Web of Science Access
- Verify institutional API access
- Check API key validity
- Contact Clarivate support

## Support

For issues or questions:
1. Check API documentation at http://localhost:8000/docs
2. Review error messages in response
3. Check MongoDB logs
4. Verify API keys in .env file

---

**Status:** ✅ Complete and Ready for Testing
