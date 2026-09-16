/**
 * ResearchAtlas - System Constants
 * Central configuration for roles, departments, email domains, and system-wide constants.
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

/**
 * Email domain restrictions per role
 * Admin and Faculty must use @raisoni.net
 * Students must use @ghrce.raisoni.net
 */
export const ROLE_EMAIL_DOMAINS = Object.freeze({
  [ROLES.ADMIN]: 'raisoni.net',
  [ROLES.FACULTY]: 'raisoni.net',
  [ROLES.STUDENT]: 'ghrce.raisoni.net',
});

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export const ROUTES = Object.freeze({
  LOGIN: '/login',
  REGISTER: '/register',
  UNAUTHORIZED: '/unauthorized',
  
  // Admin routes
  ADMIN_DASHBOARD: '/admin-dashboard',
  ADMIN_FACULTY: '/admin/faculty',
  ADMIN_CITATIONS: '/admin/citations',
  ADMIN_RESEARCH_PAPERS: '/admin/research-papers',
  ADMIN_NOTIFICATIONS: '/admin/notifications',
  ADMIN_ANALYTICS: '/admin/analytics',
  ADMIN_REPORTS: '/admin/reports',
  ADMIN_MANAGE_FACULTY: '/admin/manage-faculty',
  
  // Faculty routes
  FACULTY_DASHBOARD: '/faculty-dashboard',
  
  // Student routes
  STUDENT_DASHBOARD: '/student-dashboard',
});

/**
 * All admin routes for centralized access
 */
export const ADMIN_ROUTES = Object.freeze([
  ROUTES.ADMIN_DASHBOARD,
  ROUTES.ADMIN_FACULTY,
  ROUTES.ADMIN_CITATIONS,
  ROUTES.ADMIN_RESEARCH_PAPERS,
  ROUTES.ADMIN_NOTIFICATIONS,
  ROUTES.ADMIN_ANALYTICS,
  ROUTES.ADMIN_REPORTS,
  ROUTES.ADMIN_MANAGE_FACULTY,
]);

export const ROLE_DASHBOARD_MAP = Object.freeze({
  [ROLES.ADMIN]: ROUTES.ADMIN_DASHBOARD,
  [ROLES.FACULTY]: ROUTES.FACULTY_DASHBOARD,
  [ROLES.STUDENT]: ROUTES.STUDENT_DASHBOARD,
});

export const PASSWORD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

export const PASSWORD_REQUIREMENTS = 'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character (@$!%*?&).';

export const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export const ORCID_REGEX = /^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$|^\d{16}$/;
export const SCOPUS_REGEX = /^\d{5,15}$/;
export const WOS_REGEX = /^[A-Z]-\d{4}-\d{4}$|^[A-Za-z0-9\-]{5,20}$/;
