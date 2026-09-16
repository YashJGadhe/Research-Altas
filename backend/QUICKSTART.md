# Quick Start Guide

Get the unified researcher/publication backend running in 5 minutes.

## Prerequisites

- Python 3.8+
- MongoDB running on localhost:27017
- API keys (at least Scopus recommended)

## Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Step 2: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=researchatlas_new

# Required for Scopus
SCOPUS_API_KEY=your_scopus_api_key_here

# Optional for Web of Science
WOS_API_KEY=your_wos_api_key_here

# Optional for ORCID (public API works without these)
ORCID_CLIENT_ID=
ORCID_CLIENT_SECRET=

CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

**Where to get API keys:**
- **Scopus**: https://dev.elsevier.com/
- **Web of Science**: Contact Clarivate (institutional access required)
- **ORCID**: Not required (public API works)
- **Google Scholar**: No API key needed

## Step 3: Start MongoDB

```bash
# Option 1: Local MongoDB
mongod

# Option 2: Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

## Step 4: Run Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
Connected to MongoDB: researchatlas_new
Database indexes created successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 5: Test the API

### Test ORCID (No API key required)

```bash
curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{"orcid": "0000-0002-1825-0097"}' | jq .
```

Expected: ✅ Publications fetched, citation_count: null

### Test Scopus (API key required)

```bash
curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{"scopus_author_id": "57487968600"}' | jq .
```

Expected: ✅ Publications fetched with citation counts

### Test Multiple Platforms

```bash
curl -X POST http://localhost:8000/api/researchers/search \
  -H "Content-Type: application/json" \
  -d '{
    "orcid": "0000-0002-1825-0097",
    "scopus_author_id": "57487968600"
  }' | jq .
```

Expected: ✅ Publications from both platforms in unified format

## Step 6: Verify MongoDB Data

```bash
mongosh
use researchatlas_new

# Check researchers
db.researchers.find().count()

# Check publications
db.publications.find().count()

# Check publications by platform
db.publications.aggregate([
  {$group: {_id: "$platform", count: {$sum: 1}}}
])
```

## Step 7: View API Documentation

Open browser: http://localhost:8000/docs

You'll see interactive Swagger UI with all endpoints.

## Common Issues

### Issue: MongoDB Connection Failed
```bash
# Check if MongoDB is running
mongosh

# If not running, start it
mongod
```

### Issue: Scopus API Returns 401
```bash
# Verify your API key in .env
cat .env | grep SCOPUS_API_KEY

# Test API key directly
curl -H "X-ELS-APIKey: YOUR_KEY" \
  "https://api.elsevier.com/content/search/scopus?query=AU-ID(57487968600)"
```

### Issue: Google Scholar Blocked
- Wait a few minutes and retry
- Google Scholar may rate-limit requests
- Consider using only ORCID and Scopus

### Issue: Port 8000 Already in Use
```bash
# Use different port
uvicorn app.main:app --reload --port 8001
```

## Frontend Integration

Update your frontend to call the new API:

```javascript
// Example: Fetch researcher publications
const response = await fetch('http://localhost:8000/api/researchers/search', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    orcid: '0000-0002-1825-0097',
    scopus_author_id: '57487968600'
  })
});

const data = await response.json();

// Display publications in table
console.log(data.publications);
console.log(data.total_publications);
console.log(data.sources);
```

## Next Steps

1. ✅ Backend is running
2. ✅ Test each platform individually
3. ✅ Test multiple platforms together
4. ✅ Verify MongoDB data
5. ✅ Integrate with frontend
6. ✅ Read `TESTING.md` for comprehensive tests
7. ✅ Read `README.md` for full documentation

## Success Indicators

✅ Backend starts without errors
✅ MongoDB connection successful
✅ ORCID search returns publications
✅ Scopus search returns publications (if API key valid)
✅ Publications saved to MongoDB
✅ Unified format returned
✅ No duplicate publications
✅ API docs accessible at /docs

## Need Help?

- **Full Documentation**: See `README.md`
- **Testing Guide**: See `TESTING.md`
- **Implementation Details**: See `IMPLEMENTATION_SUMMARY.md`
- **API Documentation**: Visit http://localhost:8000/docs

---

**You're all set! 🚀**
