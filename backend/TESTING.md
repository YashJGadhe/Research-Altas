# Testing Guide - Unified Researcher/Publication System

## Prerequisites

1. MongoDB running on localhost:27017
2. Backend server running on localhost:8000
3. API keys configured in `.env` file

## Quick Test Commands

### 1. Test ORCID Only

```bash
curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{
    "orcid": "0000-0002-1825-0097"
  }' | jq .
```

**Expected:**
- ✅ Status: success
- ✅ Publications fetched
- ✅ Citation count: null (ORCID doesn't provide)
- ✅ Data saved to MongoDB

### 2. Test Scopus Only

```bash
curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{
    "scopus_author_id": "57487968600"
  }' | jq .
```

**Expected:**
- ✅ Status: success (if API key valid)
- ✅ Publications fetched
- ✅ Citation count: provided
- ✅ Data saved to MongoDB

### 3. Test Google Scholar Only

```bash
curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{
    "google_scholar_author_id": "JicYPdAAAAAJ"
  }' | jq .
```

**Expected:**
- ✅ Status: success
- ✅ Publications fetched
- ✅ Citation count: provided
- ⚠️ May be rate-limited

### 4. Test Web of Science Only

```bash
curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{
    "wos_researcher_id": "A-1234-5678"
  }' | jq .
```

**Expected:**
- ✅ Status: success (if API key valid)
- ✅ Publications fetched
- ✅ Citation count: provided

### 5. Test All Platforms Together

```bash
curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{
    "orcid": "0000-0002-1825-0097",
    "scopus_author_id": "57487968600",
    "google_scholar_author_id": "JicYPdAAAAAJ",
    "wos_researcher_id": "A-1234-5678"
  }' | jq .
```

**Expected:**
- ✅ All platforms fetch in parallel
- ✅ Combined publications in unified format
- ✅ Platform-specific citation counts preserved
- ✅ All data saved to MongoDB

### 6. Test GET Endpoint

```bash
curl "http://localhost:8000/api/researchers/search?orcid=0000-0002-1825-0097&scopus_author_id=57487968600" | jq .
```

## Verify MongoDB Data

### Check Researchers Collection

```bash
mongosh
use researchatlas_new
db.researchers.find().pretty()
```

### Check Publications Collection

```bash
mongosh
use researchatlas_new
db.publications.find({researcher_key: "orcid:0000-0002-1825-0097"}).pretty()
```

### Check Sync Logs

```bash
mongosh
use researchatlas_new
db.sync_logs.find().sort({synced_at: -1}).limit(5).pretty()
```

### Count Publications by Platform

```bash
mongosh
use researchatlas_new
db.publications.aggregate([
  {$match: {researcher_key: "orcid:0000-0002-1825-0097"}},
  {$group: {_id: "$platform", count: {$sum: 1}}}
])
```

## Test Error Handling

### 1. Test Missing Identifiers

```bash
curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{}' | jq .
```

**Expected:** 400 error - "At least one researcher identifier must be provided"

### 2. Test Invalid ORCID

```bash
curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{
    "orcid": "invalid-orcid-id"
  }' | jq .
```

**Expected:** Platform failure with error message

### 3. Test Partial Failure

```bash
curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{
    "orcid": "0000-0002-1825-0097",
    "scopus_author_id": "invalid-id"
  }' | jq .
```

**Expected:**
- ✅ ORCID: success
- ❌ Scopus: failed with error
- ✅ Other platforms continue

## Verify Unified Format

Check that all publications have the same structure:

```bash
curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{
    "orcid": "0000-0002-1825-0097",
    "scopus_author_id": "57487968600"
  }' | jq '.publications[0]'
```

**Expected fields:**
- source
- paper_name
- year
- date
- author_name
- work_type
- doi
- url
- citation_count
- publication_name
- scopus_id
- wos_id
- issn
- eissn
- isbn
- volume
- issue
- pages
- publisher

## Test Duplicate Handling

### 1. Fetch Same Researcher Twice

```bash
# First fetch
curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{"orcid": "0000-0002-1825-0097"}' | jq .

# Second fetch (same researcher)
curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{"orcid": "0000-0002-1825-0097"}' | jq .
```

**Expected:**
- ✅ No duplicate publications in MongoDB
- ✅ Existing records updated
- ✅ Same total count

### 2. Check for Duplicates in MongoDB

```bash
mongosh
use researchatlas_new

# Check for duplicate DOIs within same platform
db.publications.aggregate([
  {$match: {doi: {$ne: null}}},
  {$group: {
    _id: {researcher_key: "$researcher_key", platform: "$platform", doi: "$doi"},
    count: {$sum: 1}
  }},
  {$match: {count: {$gt: 1}}}
])
```

**Expected:** No results (no duplicates)

## Test Citation Counts

### Verify Platform-Specific Citations

```bash
mongosh
use researchatlas_new

# Check ORCID (should be null)
db.publications.findOne({platform: "ORCID"}, {citation_count: 1, paper_name: 1})

# Check Scopus (should have value)
db.publications.findOne({platform: "Scopus"}, {citation_count: 1, paper_name: 1})

# Check Google Scholar (should have value)
db.publications.findOne({platform: "Google Scholar"}, {citation_count: 1, paper_name: 1})
```

## Test Re-fetch Behavior

### 1. Initial Fetch

```bash
curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{"orcid": "0000-0002-1825-0097"}' | jq '.total_publications'
```

### 2. Re-fetch After Some Time

```bash
curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{"orcid": "0000-0002-1825-0097"}' | jq '.total_publications'
```

**Expected:**
- ✅ Same or higher count (if new publications added)
- ✅ No duplicates
- ✅ Updated timestamp in researcher record

## Performance Test

### Test Parallel Fetching

```bash
time curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{
    "orcid": "0000-0002-1825-0097",
    "scopus_author_id": "57487968600",
    "google_scholar_author_id": "JicYPdAAAAAJ",
    "wos_researcher_id": "A-1234-5678"
  }' > /dev/null
```

**Expected:** Should complete in ~5-10 seconds (parallel fetching)

## Frontend Integration Test

### Test Response Structure

```bash
curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{"orcid": "0000-0002-1825-0097"}' | jq '{
    researcher_ids: .researcher_ids,
    sources: .sources,
    columns: .columns,
    total_publications: .total_publications,
    mongodb: .mongodb,
    first_publication: .publications[0]
  }'
```

**Expected:** Complete response structure for frontend

## Troubleshooting

### Issue: MongoDB Connection Failed
```bash
# Check MongoDB is running
mongosh

# Check connection string
cat .env | grep MONGODB_URL
```

### Issue: Scopus API Returns 401
```bash
# Verify API key
curl -H "X-ELS-APIKey: YOUR_KEY" \
  "https://api.elsevier.com/content/search/scopus?query=AU-ID(57487968600)"
```

### Issue: Google Scholar Blocked
- Wait a few minutes and retry
- Check if IP is blocked
- Consider using proxy

### Issue: Web of Science Returns 403
- Verify institutional API access
- Check API key validity
- Contact Clarivate support

## Success Criteria

✅ All 4 platforms can fetch publications
✅ Unified format returned for all platforms
✅ Citation counts are platform-specific
✅ No duplicate publications within same platform
✅ Data saved to MongoDB correctly
✅ Error handling works gracefully
✅ Parallel fetching improves performance
✅ Frontend can consume the response

---

**Testing Status:** Ready for comprehensive testing
