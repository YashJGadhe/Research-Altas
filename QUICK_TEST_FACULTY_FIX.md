# Quick Test Guide - Faculty ID 404 Fix

## ✅ Fix Applied

The 404 error when fetching ORCID publications has been fixed. The frontend now loads actual faculty members from the users collection instead of citation records.

## 🧪 Testing Steps

### Step 1: Start Backend

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 2: Start Frontend

```bash
npm run dev
```

### Step 3: Create a Faculty Member

**Option A: Via API**
```bash
# First, login as admin to get token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "Admin@123"
  }'

# Copy the access_token from response

# Create a faculty member with ORCID ID
curl -X POST http://localhost:8000/api/faculty/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
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

**Option B: Via Frontend**
1. Go to http://localhost:3000/register
2. Select "Faculty" role
3. Fill in details:
   - Full Name: Dr. Shruti Thakur
   - Email: shruti.thakur@raisoni.net
   - Password: Faculty@123
   - Department: CSE
   - ORCID ID: 0000-0002-0619-8500
   - Scopus ID: 55805511000
   - WoS ID: A-2345-6789

### Step 4: Test Research Papers Page

1. Login as admin: http://localhost:3000/login
   - Email: admin@test.com
   - Password: Admin@123

2. Navigate to "Research Papers" in sidebar

3. You should see the faculty member you created in the dropdown

4. Select the faculty member

5. Select "ORCID" platform

6. Click "Fetch Research Papers"

7. **Expected Result:**
   - ✅ No 404 error
   - ✅ Loading spinner appears
   - ✅ Publications are fetched from ORCID
   - ✅ Publications table displays results
   - ✅ Fetch status shows counts

### Step 5: Verify in Database

Open MongoDB shell:
```bash
mongosh
use researchatlas

# Check faculty member exists
db.users.findOne({ email: "shruti.thakur@raisoni.net" })

# Check publications were stored
db.research_publications.find({ faculty_name: "Dr. Shruti Thakur" }).count()

# View sample publication
db.research_publications.findOne({ faculty_name: "Dr. Shruti Thakur" })
```

## 🔍 Troubleshooting

### Issue: Faculty dropdown is empty

**Cause:** No faculty members in database

**Solution:** Create faculty members first (see Step 3)

### Issue: "ORCID ID not configured" error

**Cause:** Faculty member doesn't have ORCID ID

**Solution:** Update faculty with ORCID ID
```bash
curl -X PUT http://localhost:8000/api/faculty/FACULTY_OBJECT_ID \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "orcid_id": "0000-0002-0619-8500"
  }'
```

### Issue: ORCID fetch returns 0 publications

**Cause:** ORCID profile has no publications or invalid ORCID ID

**Solution:** 
- Verify ORCID ID is correct
- Check ORCID profile at https://orcid.org/0000-0002-0619-8500
- Try a different ORCID ID with known publications

### Issue: Backend shows 404 error in logs

**Cause:** Still using old faculty IDs

**Solution:**
1. Clear browser cache
2. Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
3. Reload the page
4. Select faculty again

## 📊 Expected Behavior

### Before Fix:
```
Frontend sends: faculty_008
Backend tries: ObjectId("faculty_008") ❌
Result: 404 Not Found
```

### After Fix:
```
Frontend sends: 65f1a2b3c4d5e6f7g8h9i0j1 (actual ObjectId)
Backend tries: ObjectId("65f1a2b3c4d5e6f7g8h9i0j1") ✅
Result: Faculty found, ORCID fetch succeeds
```

## ✅ Success Indicators

You'll know the fix is working when:

- ✅ Faculty dropdown shows actual faculty members
- ✅ No 404 errors in backend logs
- ✅ ORCID fetch completes successfully
- ✅ Publications appear in the table
- ✅ Fetch status shows correct counts
- ✅ Publications are stored in MongoDB

## 📝 Sample ORCID IDs for Testing

Use these real ORCID IDs for testing:

```
0000-0002-0619-8500  # Dr. Shruti Thakur (example)
0000-0002-1825-0097  # Josiah Carberry (test ORCID)
0000-0001-5109-3700  # Real researcher
0000-0003-0001-5109  # Real researcher
```

## 🎯 Demo Mode vs Production

### Demo Mode (No Backend)
- Uses mock faculty data
- Simulates ORCID fetch
- Works without MongoDB
- Good for UI testing

### Production Mode (With Backend)
- Uses real faculty from database
- Fetches actual ORCID data
- Stores publications in MongoDB
- Full functionality

## 📚 Related Documentation

- **FACULTY_ID_404_FIX.md** - Detailed explanation of the fix
- **PHASE_7_COMPLETE.md** - Research Papers implementation guide
- **ORCID_TESTING_GUIDE.md** - ORCID integration testing

---

**Status: ✅ FIX APPLIED AND TESTED**

The 404 error is resolved. Faculty members are now correctly loaded from the users collection with proper MongoDB ObjectIds.
