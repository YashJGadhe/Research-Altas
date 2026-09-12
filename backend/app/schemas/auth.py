"""
ResearchAtlas - Authentication Schemas

Pydantic models for authentication request/response validation.
Includes email domain validation per role and mandatory research IDs.
"""

from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
import re

from app.core.config import settings


class RegisterRequest(BaseModel):
    """Schema for user registration request."""
    full_name: str
    email: str
    password: str
    confirm_password: str
    role: str
    department: str
    orcid_id: str
    scopus_id: str
    wos_id: str

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

    @model_validator(mode='after')
    def validate_email_domain_by_role(self):
        """Validate email domain matches the selected role."""
        role = self.role
        email = self.email
        
        # Get allowed domain for role
        allowed_domain = settings.role_email_domains.get(role)
        
        if not allowed_domain:
            raise ValueError(f"Invalid role: {role}")
        
        # Check if email ends with the allowed domain
        if not email.endswith(f"@{allowed_domain}"):
            if role == "student":
                raise ValueError(f"Students must register with a @{settings.STUDENT_EMAIL_DOMAIN} email address")
            else:
                raise ValueError(f"{role.capitalize()} must register with a @{allowed_domain} email address")
        
        return self

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

    @field_validator("orcid_id")
    @classmethod
    def validate_orcid_id(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("ORCID ID is required")
        
        # ORCID format: 0000-0000-0000-0000 (with dashes) or 0000000000000000 (without dashes)
        orcid_pattern = r'^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$|^\d{16}$'
        if not re.match(orcid_pattern, v):
            raise ValueError("Invalid ORCID ID format. Use format: 0000-0000-0000-0000")
        
        # Normalize to dashed format
        if len(v) == 16:
            v = f"{v[:4]}-{v[4:8]}-{v[8:12]}-{v[12:]}"
        
        return v

    @field_validator("scopus_id")
    @classmethod
    def validate_scopus_id(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Scopus ID is required")
        
        # Scopus ID is numeric
        if not v.isdigit():
            raise ValueError("Scopus ID must be numeric")
        
        if len(v) < 5 or len(v) > 15:
            raise ValueError("Scopus ID must be between 5 and 15 digits")
        
        return v

    @field_validator("wos_id")
    @classmethod
    def validate_wos_id(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Web of Science ID is required")
        
        # WOS Researcher ID format: typically starts with a letter followed by alphanumeric
        # Common formats: A-1234-5678 or similar
        wos_pattern = r'^[A-Z]-\d{4}-\d{4}$|^[A-Za-z0-9\-]{5,20}$'
        if not re.match(wos_pattern, v):
            raise ValueError("Invalid Web of Science ID format")
        
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
