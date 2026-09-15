/**
 * ResearchAtlas - Mock API for Preview/Demo Mode
 * 
 * Provides mock data when backend is not available.
 * Used for preview demonstrations and testing.
 */

// Mock admin user data
export const MOCK_ADMIN = {
  id: 'demo-admin-001',
  full_name: 'Dr. Rajesh Kumar',
  email: 'admin@test.com',
  role: 'admin',
  department: 'CSE',
  orcid_id: '0000-0002-1825-0097',
  scopus_id: '55805511000',
  wos_id: 'A-2345-6789',
  is_active: true,
  created_at: '2026-01-15T10:00:00+00:00',
  updated_at: '2026-03-24T10:00:00+00:00',
};

// Mock faculty data
export const MOCK_FACULTY = [
  {
    id: 'faculty-001',
    full_name: 'Dr. Priya Sharma',
    email: 'priya.sharma@raisoni.net',
    role: 'faculty',
    department: 'CSE',
    orcid_id: '0000-0001-2345-6789',
    scopus_id: '55805511001',
    wos_id: 'A-1234-5678',
    is_active: true,
    created_at: '2026-01-20T10:00:00+00:00',
    updated_at: '2026-03-20T10:00:00+00:00',
  },
  {
    id: 'faculty-002',
    full_name: 'Dr. Amit Patel',
    email: 'amit.patel@raisoni.net',
    role: 'faculty',
    department: 'CSE',
    orcid_id: '0000-0002-3456-7890',
    scopus_id: '55805511002',
    wos_id: 'B-2345-6789',
    is_active: true,
    created_at: '2026-02-01T10:00:00+00:00',
    updated_at: '2026-03-21T10:00:00+00:00',
  },
  {
    id: 'faculty-003',
    full_name: 'Dr. Sneha Reddy',
    email: 'sneha.reddy@raisoni.net',
    role: 'faculty',
    department: 'CSE',
    orcid_id: '0000-0003-4567-8901',
    scopus_id: '55805511003',
    wos_id: 'C-3456-7890',
    is_active: true,
    created_at: '2026-02-10T10:00:00+00:00',
    updated_at: '2026-03-22T10:00:00+00:00',
  },
];

// Mock student data
export const MOCK_STUDENT = {
  id: 'student-001',
  full_name: 'Rahul Verma',
  email: 'rahul.verma@ghrce.raisoni.net',
  role: 'student',
  department: 'CSE',
  orcid_id: '0000-0004-5678-9012',
  scopus_id: '55805511004',
  wos_id: 'D-4567-8901',
  is_active: true,
  created_at: '2026-03-01T10:00:00+00:00',
  updated_at: '2026-03-24T10:00:00+00:00',
};

/**
 * Mock login function
 * Simulates backend login with test credentials
 */
export const mockLogin = async (email, password) => {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 800));

  // Test credentials
  const validCredentials = [
    { email: 'admin@test.com', password: 'Admin@123', user: MOCK_ADMIN },
    { email: 'faculty@test.com', password: 'Faculty@123', user: MOCK_FACULTY[0] },
    { email: 'student@test.com', password: 'Student@123', user: MOCK_STUDENT },
  ];

  const match = validCredentials.find(
    cred => cred.email === email.toLowerCase().trim() && cred.password === password
  );

  if (!match) {
    throw {
      response: {
        status: 401,
        data: { detail: 'Invalid email or password' }
      }
    };
  }

  // Generate mock JWT token
  const mockToken = 'mock_jwt_token_' + Date.now() + '_' + Math.random().toString(36).substring(7);

  return {
    access_token: mockToken,
    token_type: 'bearer',
    user: match.user,
  };
};

/**
 * Mock register function
 */
export const mockRegister = async (userData) => {
  await new Promise(resolve => setTimeout(resolve, 800));
  return {
    message: 'Registration successful (Demo Mode). You can now login.',
    success: true,
  };
};

/**
 * Mock get current user
 */
export const mockGetCurrentUser = async () => {
  await new Promise(resolve => setTimeout(resolve, 300));
  const storedUser = localStorage.getItem('user');
  if (storedUser) {
    return JSON.parse(storedUser);
  }
  throw { response: { status: 401, data: { detail: 'Not authenticated' } } };
};

/**
 * Check if we're in demo mode (backend not available)
 */
export const isDemoMode = () => {
  return import.meta.env.VITE_DEMO_MODE === 'true' || localStorage.getItem('demoMode') === 'true';
};

/**
 * Enable demo mode
 */
export const enableDemoMode = () => {
  localStorage.setItem('demoMode', 'true');
};

/**
 * Disable demo mode
 */
export const disableDemoMode = () => {
  localStorage.removeItem('demoMode');
};
