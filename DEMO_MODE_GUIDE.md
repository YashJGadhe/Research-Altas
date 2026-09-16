# 🎮 ResearchAtlas - Demo Mode Guide

## ✅ Demo Mode is Now Active!

The preview environment now includes a **complete demo mode** that allows you to explore the full ResearchAtlas admin panel without needing a backend server.

## 🚀 Quick Start

### Option 1: One-Click Admin Login (Recommended)
1. Open the preview
2. Click the **"👑 Login as Admin (Demo)"** button
3. You'll be instantly logged in and redirected to the admin dashboard

### Option 2: Manual Login
1. Open the preview
2. Use these credentials:
   - **Email:** `admin@test.com`
   - **Password:** `Admin@123`
3. Click "Sign In"

## 🎭 Available Demo Accounts

### 👑 Admin Account
- **Email:** `admin@test.com`
- **Password:** `Admin@123`
- **Name:** Dr. Rajesh Kumar
- **Access:** Full admin panel with sidebar navigation

### 👨‍🏫 Faculty Account
- **Email:** `faculty@test.com`
- **Password:** `Faculty@123`
- **Name:** Dr. Priya Sharma
- **Access:** Faculty dashboard

### 🎓 Student Account
- **Email:** `student@test.com`
- **Password:** `Student@123`
- **Name:** Rahul Verma
- **Access:** Student dashboard

## 🎯 What You Can Explore

### Admin Dashboard Features
- ✅ **Professional Sidebar Navigation** - Collapsible with tooltips
- ✅ **8 Admin Module Pages** - All accessible via sidebar
- ✅ **Admin Profile Display** - Shows name, email, role, department
- ✅ **Research IDs** - ORCID, Scopus, WoS IDs displayed
- ✅ **Quick Access Cards** - Visual navigation to key modules
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile
- ✅ **Demo Mode Badge** - Purple badge in header indicates demo mode

### Admin Module Pages
1. **Dashboard** - Overview with profile and quick access
2. **View Faculty** - Faculty listing (placeholder)
3. **Citation Management** - Citation tracking (placeholder)
4. **Research Papers** - Publication management (placeholder)
5. **Notifications** - System notifications (placeholder)
6. **Analytics** - Research analytics (placeholder)
7. **Reports** - Report generation (placeholder)
8. **Manage Faculty** - Faculty CRUD operations (placeholder)

## 🔧 How Demo Mode Works

### Architecture
```
User clicks "Login as Admin (Demo)"
    ↓
Frontend calls mockLogin() function
    ↓
Mock API returns test admin data
    ↓
AuthContext stores user data in localStorage
    ↓
Sets demoMode flag in localStorage
    ↓
Redirects to /admin-dashboard
    ↓
AdminLayout renders with sidebar
    ↓
All admin pages accessible
```

### Key Features
- **No Backend Required** - Works entirely in the browser
- **Persistent Session** - Stays logged in until you logout
- **Automatic Fallback** - If backend is unavailable, uses demo mode
- **Real UI/UX** - Full admin interface with all features
- **Role-Based Access** - Test different user roles

## 📊 Demo Data

### Admin User Profile
```json
{
  "id": "demo-admin-001",
  "full_name": "Dr. Rajesh Kumar",
  "email": "admin@test.com",
  "role": "admin",
  "department": "CSE",
  "orcid_id": "0000-0002-1825-0097",
  "scopus_id": "55805511000",
  "wos_id": "A-2345-6789",
  "is_active": true
}
```

### Sample Faculty Members
- Dr. Priya Sharma (priya.sharma@raisoni.net)
- Dr. Amit Patel (amit.patel@raisoni.net)
- Dr. Sneha Reddy (sneha.reddy@raisoni.net)

## 🎨 UI Features

### Sidebar
- **Expanded:** Shows icons + labels
- **Collapsed:** Shows icons only with tooltips
- **Active State:** Blue highlight on current page
- **Responsive:** Mobile drawer on small screens

### Header
- **Page Title:** Shows current page name
- **Demo Badge:** Purple "🎮 Demo" badge
- **User Info:** Name and role display
- **Logout Button:** Clears session and returns to login

### Dashboard
- **Profile Card:** Shows admin details with research IDs
- **Quick Access:** 4 cards for key modules
- **Phase Notice:** Information about current development phase

## 🔄 Switching Between Accounts

1. Click **Logout** in the header
2. You'll be redirected to login page
3. Click a different demo account button
4. Or enter credentials manually

## 🛠️ Technical Details

### Files Created/Modified
- `src/api/mockApi.js` - Mock API with test data
- `src/api/authApi.js` - Updated to use mock in demo mode
- `src/context/AuthContext.jsx` - Skips verification in demo mode
- `src/pages/auth/LoginPage.jsx` - Added demo login buttons
- `src/components/admin/AdminHeader.jsx` - Added demo badge
- `src/pages/admin/AdminDashboard.jsx` - Added demo notice

### Demo Mode Detection
```javascript
// Check if demo mode is active
const isDemo = localStorage.getItem('demoMode') === 'true';

// Enable demo mode
localStorage.setItem('demoMode', 'true');

// Disable demo mode (on logout, but keeps for next login)
localStorage.removeItem('demoMode');
```

### Mock API Functions
- `mockLogin(email, password)` - Simulates login
- `mockRegister(userData)` - Simulates registration
- `mockGetCurrentUser()` - Returns stored user data
- `isDemoMode()` - Checks if demo mode is active

## 🎯 Testing Scenarios

### Test 1: Admin Login
1. Click "Login as Admin (Demo)"
2. Verify redirect to `/admin-dashboard`
3. Verify sidebar is visible
4. Verify admin profile shows correctly
5. Verify demo badge appears in header

### Test 2: Sidebar Navigation
1. Click each menu item in sidebar
2. Verify page changes
3. Verify active state highlights
4. Test collapse/expand functionality
5. Verify tooltips appear when collapsed

### Test 3: Role-Based Access
1. Logout from admin
2. Login as faculty
3. Verify redirect to `/faculty-dashboard`
4. Try accessing `/admin-dashboard`
5. Verify redirect to `/unauthorized`

### Test 4: Responsive Design
1. Resize browser to mobile width
2. Verify sidebar becomes drawer
3. Click hamburger menu
4. Verify drawer opens
5. Click menu item
6. Verify drawer closes

### Test 5: Logout
1. Click logout button
2. Verify redirect to `/login`
3. Try accessing `/admin-dashboard`
4. Verify redirect to `/login`

## 💡 Tips

### For Presentations
- Use the one-click admin login for quick demos
- Show the sidebar collapse/expand feature
- Navigate through all admin pages
- Demonstrate responsive design on mobile

### For Development
- Demo mode automatically activates when backend is unavailable
- You can manually enable it: `localStorage.setItem('demoMode', 'true')`
- All mock data is in `src/api/mockApi.js`
- Easy to customize test data

### For Testing
- Test all three roles (admin, faculty, student)
- Verify role-based access control
- Test sidebar persistence across page changes
- Test logout and re-login flow

## 🚀 Next Steps

### With Backend
When you connect to the real backend:
1. Backend automatically takes over
2. Demo mode deactivates
3. Real authentication works
4. Real data from MongoDB

### Without Backend
Continue using demo mode:
1. All UI features work
2. Navigation works
3. Role-based access works
4. Perfect for presentations

## 📝 Summary

✅ **Demo mode is fully functional**
✅ **One-click admin login available**
✅ **All admin pages accessible**
✅ **Professional UI/UX preserved**
✅ **No backend required**
✅ **Perfect for preview and presentations**

---

**Status: ✅ READY FOR DEMO**

Click "👑 Login as Admin (Demo)" to explore the full admin panel!
