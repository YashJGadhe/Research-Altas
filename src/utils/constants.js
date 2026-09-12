/**
 * ResearchAtlas - System Constants
 * Central configuration for roles, departments, and system-wide constants.
 */

export const ROLES = Object.freeze({
  ADMIN: 'admin',
  FACULTY: 'faculty',
  STUDENT: 'student',
});

export const ROLE_LABELS = Object.freeze({
  [ROLES.ADMIN]: 'Administrator',
  [ROLES.FACULTY]: 'Faculty',
  [ROLES.STUDENT]: 'Student',
});

export const VALID_ROLES = Object.freeze(Object.values(ROLES));

export const DEPARTMENTS = Object.freeze({
  CSE: 'CSE',
});

export const DEPARTMENT_LABELS = Object.freeze({
  [DEPARTMENTS.CSE]: 'Computer Science & Engineering',
});

export const VALID_DEPARTMENTS = Object.freeze(Object.values(DEPARTMENTS));

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const ROUTES = Object.freeze({
  LOGIN: '/login',
  REGISTER: '/register',
  UNAUTHORIZED: '/unauthorized',
  ADMIN_DASHBOARD: '/admin-dashboard',
  FACULTY_DASHBOARD: '/faculty-dashboard',
  STUDENT_DASHBOARD: '/student-dashboard',
});

export const ROLE_DASHBOARD_MAP = Object.freeze({
  [ROLES.ADMIN]: ROUTES.ADMIN_DASHBOARD,
  [ROLES.FACULTY]: ROUTES.FACULTY_DASHBOARD,
  [ROLES.STUDENT]: ROUTES.STUDENT_DASHBOARD,
});

export const PASSWORD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

export const PASSWORD_REQUIREMENTS = 'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character (@$!%*?&).';

export const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
