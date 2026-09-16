/**
 * ResearchAtlas - Registration Page
 * 
 * Handles new user registration with:
 * - Tab-based role selection (Admin, Faculty, Student)
 * - Email domain validation per role
 * - Mandatory ORCID, Scopus, and WOS ID fields
 * - Full client and server-side validation
 */

import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { register as registerApi } from '../../api/authApi';
import {
  ROUTES,
  ROLES,
  ROLE_LABELS,
  VALID_ROLES,
  DEPARTMENTS,
  DEPARTMENT_LABELS,
  VALID_DEPARTMENTS,
  ROLE_EMAIL_DOMAINS,
  EMAIL_REGEX,
  PASSWORD_REGEX,
  PASSWORD_REQUIREMENTS,
  ORCID_REGEX,
  SCOPUS_REGEX,
  WOS_REGEX,
} from '../../utils/constants';

const RegisterPage = () => {
  const [selectedRole, setSelectedRole] = useState(ROLES.STUDENT);
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    password: '',
    confirm_password: '',
    role: ROLES.STUDENT,
    department: '',
    orcid_id: '',
    scopus_id: '',
    wos_id: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Update role in formData when tab changes
  useEffect(() => {
    setFormData(prev => ({ ...prev, role: selectedRole, email: '' }));
    setError('');
  }, [selectedRole]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError('');
    setSuccess('');
  };

  const handleRoleTabClick = (role) => {
    setSelectedRole(role);
  };

  const validateForm = () => {
    // Full name validation
    if (!formData.full_name.trim()) {
      setError('Full name is required.');
      return false;
    }

    // Email validation
    if (!formData.email.trim()) {
      setError('Email is required.');
      return false;
    }

    if (!EMAIL_REGEX.test(formData.email)) {
      setError('Please enter a valid email address.');
      return false;
    }

    // Email domain validation based on role
    const allowedDomain = ROLE_EMAIL_DOMAINS[selectedRole];
    if (!formData.email.endsWith(`@${allowedDomain}`)) {
      if (selectedRole === ROLES.STUDENT) {
        setError(`Students must register with a @${allowedDomain} email address.`);
      } else {
        setError(`${ROLE_LABELS[selectedRole]} must register with a @${allowedDomain} email address.`);
      }
      return false;
    }

    // Department validation
    if (!VALID_DEPARTMENTS.includes(formData.department)) {
      setError('Please select a valid department.');
      return false;
    }

    // ORCID ID validation
    if (!formData.orcid_id.trim()) {
      setError('ORCID ID is required.');
      return false;
    }
    if (!ORCID_REGEX.test(formData.orcid_id.trim())) {
      setError('Invalid ORCID ID format. Use format: 0000-0000-0000-0000');
      return false;
    }

    // Scopus ID validation
    if (!formData.scopus_id.trim()) {
      setError('Scopus ID is required.');
      return false;
    }
    if (!SCOPUS_REGEX.test(formData.scopus_id.trim())) {
      setError('Invalid Scopus ID. Must be 5-15 digits.');
      return false;
    }

    // WOS ID validation
    if (!formData.wos_id.trim()) {
      setError('Web of Science ID is required.');
      return false;
    }
    if (!WOS_REGEX.test(formData.wos_id.trim())) {
      setError('Invalid Web of Science ID format. Use format: A-0000-0000');
      return false;
    }

    // Password validation
    if (!formData.password) {
      setError('Password is required.');
      return false;
    }

    if (!PASSWORD_REGEX.test(formData.password)) {
      setError(PASSWORD_REQUIREMENTS);
      return false;
    }

    // Password confirmation
    if (formData.password !== formData.confirm_password) {
      setError('Passwords do not match.');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!validateForm()) return;

    setLoading(true);

    try {
      await registerApi(formData);
      setSuccess('Registration successful! Redirecting to login...');
      setTimeout(() => {
        navigate(ROUTES.LOGIN);
      }, 2000);
    } catch (err) {
      console.error('Registration error:', err);
      console.error('Error response:', err.response);
      
      if (err.response?.data?.detail) {
        const detail = err.response.data.detail;
        if (typeof detail === 'string') {
          setError(detail);
        } else if (Array.isArray(detail)) {
          const messages = detail.map(d => {
            if (typeof d === 'string') return d;
            if (d.msg) return d.msg;
            if (d.message) return d.message;
            return JSON.stringify(d);
          });
          setError(messages.join('. '));
        } else {
          setError('Registration failed. Please check your input and try again.');
        }
      } else if (err.response?.status === 409) {
        setError('An account with this email or ID already exists.');
      } else if (err.response?.status === 422) {
        setError('Invalid input. Please check all fields and try again.');
      } else if (err.response?.status === 403) {
        setError(err.response.data?.detail || 'Registration not allowed. Please check your email domain.');
      } else if (err.response?.status === 500) {
        setError('Server error. Please try again later or contact support.');
      } else if (err.code === 'ERR_NETWORK' || !err.response) {
        setError('Cannot connect to server. Please check if the backend is running.');
      } else {
        setError('Registration failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  // Get the email domain hint for the selected role
  const getEmailDomainHint = () => {
    return `@${ROLE_EMAIL_DOMAINS[selectedRole]}`;
  };

  // Role tab configuration
  const roleTabs = [
    { role: ROLES.STUDENT, label: 'Student', icon: '🎓', color: 'amber' },
    { role: ROLES.FACULTY, label: 'Faculty', icon: '👨‍🏫', color: 'emerald' },
    { role: ROLES.ADMIN, label: 'Admin', icon: '🛡️', color: 'purple' },
  ];

  const getTabStyles = (tab) => {
    const isSelected = selectedRole === tab.role;
    const base = 'flex-1 py-3 px-4 rounded-t-xl font-medium text-sm transition-all duration-200 flex items-center justify-center gap-2 border-b-2';
    
    if (isSelected) {
      return `${base} bg-white text-${tab.color}-700 border-${tab.color}-500 shadow-sm`;
    }
    return `${base} bg-gray-100 text-gray-500 border-transparent hover:bg-gray-200 hover:text-gray-700`;
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 px-4 py-8">
      <div className="w-full max-w-lg">
        {/* Header */}
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-2xl shadow-lg mb-4">
            <span className="text-3xl">🌐</span>
          </div>
          <h1 className="text-3xl font-bold text-gray-900">ResearchAtlas</h1>
          <p className="text-gray-500 mt-2">Create your research account</p>
        </div>

        {/* Registration Card */}
        <div className="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden">
          {/* Role Selection Tabs */}
          <div className="flex bg-gray-50 border-b border-gray-200">
            {roleTabs.map((tab) => (
              <button
                key={tab.role}
                type="button"
                onClick={() => handleRoleTabClick(tab.role)}
                className={getTabStyles(tab)}
              >
                <span className="text-lg">{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            ))}
          </div>

          {/* Email Domain Notice */}
          <div className="px-8 pt-4">
            <div className={`p-3 rounded-lg border text-sm ${
              selectedRole === ROLES.STUDENT ? 'bg-amber-50 border-amber-200 text-amber-800' :
              selectedRole === ROLES.FACULTY ? 'bg-emerald-50 border-emerald-200 text-emerald-800' :
              'bg-purple-50 border-purple-200 text-purple-800'
            }`}>
              <span className="font-medium">Note:</span>{' '}
              {ROLE_LABELS[selectedRole]} must register with a <strong>{getEmailDomainHint()}</strong> email address.
            </div>
          </div>

          {/* Form */}
          <div className="p-8 pt-6">
            {error && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                {error}
              </div>
            )}

            {success && (
              <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm">
                {success}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Full Name */}
              <div>
                <label htmlFor="full_name" className="block text-sm font-medium text-gray-700 mb-1.5">
                  Full Name
                </label>
                <input
                  type="text"
                  id="full_name"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleChange}
                  className="input-field"
                  placeholder="Dr. John Doe"
                  required
                />
              </div>

              {/* Email */}
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1.5">
                  Email Address <span className="text-gray-400 text-xs">({getEmailDomainHint()})</span>
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="input-field"
                  placeholder={`yourname${getEmailDomainHint()}`}
                  autoComplete="email"
                  required
                />
              </div>

              {/* Department */}
              <div>
                <label htmlFor="department" className="block text-sm font-medium text-gray-700 mb-1.5">
                  Department
                </label>
                <select
                  id="department"
                  name="department"
                  value={formData.department}
                  onChange={handleChange}
                  className="input-field"
                  required
                >
                  <option value="">Select department</option>
                  {VALID_DEPARTMENTS.map((dept) => (
                    <option key={dept} value={dept}>
                      {DEPARTMENT_LABELS[dept]}
                    </option>
                  ))}
                </select>
              </div>

              {/* Research IDs Section */}
              <div className="border-t border-gray-200 pt-4 mt-4">
                <h3 className="text-sm font-semibold text-gray-800 mb-3 flex items-center gap-2">
                  <span>🔬</span> Research Identifiers <span className="text-red-500">*</span>
                </h3>
                <p className="text-xs text-gray-500 mb-3">
                  All research identifiers are mandatory for registration.
                </p>

                {/* ORCID ID */}
                <div className="mb-3">
                  <label htmlFor="orcid_id" className="block text-sm font-medium text-gray-700 mb-1.5">
                    ORCID ID
                  </label>
                  <input
                    type="text"
                    id="orcid_id"
                    name="orcid_id"
                    value={formData.orcid_id}
                    onChange={handleChange}
                    className="input-field"
                    placeholder="0000-0000-0000-0000"
                    required
                  />
                  <p className="text-xs text-gray-400 mt-1">Format: 0000-0000-0000-0000</p>
                </div>

                {/* Scopus ID */}
                <div className="mb-3">
                  <label htmlFor="scopus_id" className="block text-sm font-medium text-gray-700 mb-1.5">
                    Scopus Author ID
                  </label>
                  <input
                    type="text"
                    id="scopus_id"
                    name="scopus_id"
                    value={formData.scopus_id}
                    onChange={handleChange}
                    className="input-field"
                    placeholder="55555555555"
                    required
                  />
                  <p className="text-xs text-gray-400 mt-1">Numeric ID (5-15 digits)</p>
                </div>

                {/* Web of Science ID */}
                <div className="mb-3">
                  <label htmlFor="wos_id" className="block text-sm font-medium text-gray-700 mb-1.5">
                    Web of Science (WoS) Researcher ID
                  </label>
                  <input
                    type="text"
                    id="wos_id"
                    name="wos_id"
                    value={formData.wos_id}
                    onChange={handleChange}
                    className="input-field"
                    placeholder="A-0000-0000"
                    required
                  />
                  <p className="text-xs text-gray-400 mt-1">Format: A-0000-0000</p>
                </div>
              </div>

              {/* Password Section */}
              <div className="border-t border-gray-200 pt-4 mt-4">
                <h3 className="text-sm font-semibold text-gray-800 mb-3 flex items-center gap-2">
                  <span>🔒</span> Security
                </h3>

                {/* Password */}
                <div className="mb-3">
                  <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1.5">
                    Password
                  </label>
                  <input
                    type="password"
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    className="input-field"
                    placeholder="••••••••"
                    autoComplete="new-password"
                    required
                  />
                </div>

                {/* Confirm Password */}
                <div className="mb-3">
                  <label htmlFor="confirm_password" className="block text-sm font-medium text-gray-700 mb-1.5">
                    Confirm Password
                  </label>
                  <input
                    type="password"
                    id="confirm_password"
                    name="confirm_password"
                    value={formData.confirm_password}
                    onChange={handleChange}
                    className="input-field"
                    placeholder="••••••••"
                    autoComplete="new-password"
                    required
                  />
                </div>

                <p className="text-xs text-gray-500">{PASSWORD_REQUIREMENTS}</p>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className={`btn-primary w-full py-3 text-base mt-4 ${
                  selectedRole === ROLES.STUDENT ? 'bg-amber-600 hover:bg-amber-700' :
                  selectedRole === ROLES.FACULTY ? 'bg-emerald-600 hover:bg-emerald-700' :
                  'bg-purple-600 hover:bg-purple-700'
                }`}
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                    </svg>
                    Creating account...
                  </span>
                ) : (
                  `Register as ${ROLE_LABELS[selectedRole]}`
                )}
              </button>
            </form>

            <div className="mt-6 text-center">
              <p className="text-gray-600 text-sm">
                Already have an account?{' '}
                <Link to={ROUTES.LOGIN} className="text-blue-600 hover:text-blue-700 font-medium">
                  Sign in
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
