/**
 * ResearchAtlas - Application Routes
 * 
 * Central route configuration with authentication and role-based protection.
 * Future routes will be added here as new features are developed.
 */

import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from '../components/ProtectedRoute';
import RoleRoute from '../components/RoleRoute';
import { ROLES, ROUTES } from '../utils/constants';

// Auth pages
import LoginPage from '../pages/auth/LoginPage';
import RegisterPage from '../pages/auth/RegisterPage';
import UnauthorizedPage from '../pages/UnauthorizedPage';

// Dashboard pages (Phase 1 placeholders)
import AdminDashboard from '../pages/admin/AdminDashboard';
import FacultyDashboard from '../pages/faculty/FacultyDashboard';
import StudentDashboard from '../pages/student/StudentDashboard';

const AppRoutes = () => {
  return (
    <Routes>
      {/* Public routes */}
      <Route path={ROUTES.LOGIN} element={<LoginPage />} />
      <Route path={ROUTES.REGISTER} element={<RegisterPage />} />
      <Route path={ROUTES.UNAUTHORIZED} element={<UnauthorizedPage />} />

      {/* Admin routes - Protected + Admin role required */}
      <Route
        path={ROUTES.ADMIN_DASHBOARD}
        element={
          <RoleRoute allowedRoles={[ROLES.ADMIN]}>
            <AdminDashboard />
          </RoleRoute>
        }
      />

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
