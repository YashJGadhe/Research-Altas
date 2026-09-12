"""
ResearchAtlas - Authentication Schemas

Pydantic models for authentication request/response validation.
"""

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import re


class RegisterRequest(BaseModel):
    """Schema for user registration request."""
    full_name: str
    email: str
    password: str
    confirm_password: str
    role: str
    department: str

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v):
        v = v.strip()
        if not v or len(v) < 2:
            raise ValueError("Full name must be at least 2 characters")
        if len(v) > 100:
            raise ValueError("Full name must not exceed 100 characters")
        return v

    @field_validator("email")
    @classmethod
    def validate_and_normalize_email(cls, v):
        v = v.strip().lower()
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_pattern, v):
            raise ValueError("Invalid email format")
        return v

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'\d', v):
            raise ValueError("Password must contain at least one number")
        if not re.search(r'[@$!%*?&]', v):
            raise ValueError("Password must contain at least one special character (@$!%*?&)")
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        valid_roles = ["admin", "faculty", "student"]
        if v not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        return v

    @field_validator("department")
    @classmethod
    def validate_department(cls, v):
        valid_departments = ["CSE"]
        if v not in valid_departments:
            raise ValueError(f"Invalid department. Must be one of: {', '.join(valid_departments)}")
        return v


class LoginRequest(BaseModel):
    """Schema for login request."""
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v):
        return v.strip().lower()


class TokenResponse(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    token_type: str = "bearer"
    user: dict


class MessageResponse(BaseModel):
    """Schema for simple message responses."""
    message: str
    success: bool = True
