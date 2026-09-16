/**
 * ResearchAtlas - Application Routes
 * 
 * Central route configuration with authentication and role-based protection.
 * Phase 2: Admin module with layout, sidebar, and all admin pages.
 */

import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from '../components/ProtectedRoute';
import RoleRoute from '../components/RoleRoute';
import AdminLayout from '../components/admin/AdminLayout';
import { ROLES, ROUTES } from '../utils/constants';

// Auth pages
import LoginPage from '../pages/auth/LoginPage';
import RegisterPage from '../pages/auth/RegisterPage';
import UnauthorizedPage from '../pages/UnauthorizedPage';

// Admin pages
import AdminDashboard from '../pages/admin/AdminDashboard';
import ViewFaculty from '../pages/admin/ViewFaculty';
import CitationManagement from '../pages/admin/CitationManagement';
import ResearchPapers from '../pages/admin/ResearchPapers';
import Notifications from '../pages/admin/Notifications';
import Analytics from '../pages/admin/Analytics';
import Reports from '../pages/admin/Reports';
import ManageFaculty from '../pages/admin/ManageFaculty';

// Faculty pages
import FacultyDashboard from '../pages/faculty/FacultyDashboard';

// Student pages
import StudentDashboard from '../pages/student/StudentDashboard';

const AppRoutes = () => {
  return (
    <Routes>
      {/* Public routes */}
      <Route path={ROUTES.LOGIN} element={<LoginPage />} />
      <Route path={ROUTES.REGISTER} element={<RegisterPage />} />
      <Route path={ROUTES.UNAUTHORIZED} element={<UnauthorizedPage />} />

      {/* Admin routes - Protected + Admin role required + Admin Layout */}
      <Route
        element={
          <RoleRoute allowedRoles={[ROLES.ADMIN]}>
            <AdminLayout />
          </RoleRoute>
        }
      >
        <Route path={ROUTES.ADMIN_DASHBOARD} element={<AdminDashboard />} />
        <Route path={ROUTES.ADMIN_FACULTY} element={<ViewFaculty />} />
        <Route path={ROUTES.ADMIN_CITATIONS} element={<CitationManagement />} />
        <Route path={ROUTES.ADMIN_RESEARCH_PAPERS} element={<ResearchPapers />} />
        <Route path={ROUTES.ADMIN_NOTIFICATIONS} element={<Notifications />} />
        <Route path={ROUTES.ADMIN_ANALYTICS} element={<Analytics />} />
        <Route path={ROUTES.ADMIN_REPORTS} element={<Reports />} />
        <Route path={ROUTES.ADMIN_MANAGE_FACULTY} element={<ManageFaculty />} />
      </Route>

      {/* Faculty routes - Protected + Faculty role required */}
      <Route
        path={ROUTES.FACULTY_DASHBOARD}
        element={
          <RoleRoute allowedRoles={[ROLES.FACULTY]}>
            <FacultyDashboard />
          </RoleRoute>
        }
      />

      {/* Student routes - Protected + Student role required */}
      <Route
        path={ROUTES.STUDENT_DASHBOARD}
        element={
          <RoleRoute allowedRoles={[ROLES.STUDENT]}>
            <StudentDashboard />
          </RoleRoute>
        }
      />

      {/* Catch-all redirect */}
      <Route path="*" element={<Navigate to={ROUTES.LOGIN} replace />} />
    </Routes>
  );
};

export default AppRoutes;
