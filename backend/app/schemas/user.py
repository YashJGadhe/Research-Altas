"""
ResearchAtlas - User Schemas

Pydantic models for user management request/response validation.
"""

from pydantic import BaseModel, field_validator
from typing import Optional
import re


class UserResponse(BaseModel):
    """Schema for user API response."""
    id: str
    full_name: str
    email: str
    role: str
    department: str
    orcid_id: str
    scopus_id: str
    wos_id: str
    is_active: bool
    created_at: str
    updated_at: str


class UserUpdateRequest(BaseModel):
    """Schema for admin user update request."""
    full_name: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    orcid_id: Optional[str] = None
    scopus_id: Optional[str] = None
    wos_id: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v):
        if v is not None:
            v = v.strip()
            if len(v) < 2:
                raise ValueError("Full name must be at least 2 characters")
            if len(v) > 100:
                raise ValueError("Full name must not exceed 100 characters")
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        if v is not None:
            valid_roles = ["admin", "faculty", "student"]
            if v not in valid_roles:
                raise ValueError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        return v

    @field_validator("department")
    @classmethod
    def validate_department(cls, v):
        if v is not None:
            valid_departments = ["CSE"]
            if v not in valid_departments:
                raise ValueError(f"Invalid department. Must be one of: {', '.join(valid_departments)}")
        return v

    @field_validator("orcid_id")
    @classmethod
    def validate_orcid_id(cls, v):
        if v is not None:
            v = v.strip()
            if v:
                orcid_pattern = r'^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$|^\d{16}$'
                if not re.match(orcid_pattern, v):
                    raise ValueError("Invalid ORCID ID format")
                if len(v) == 16:
                    v = f"{v[:4]}-{v[4:8]}-{v[8:12]}-{v[12:]}"
        return v

    @field_validator("scopus_id")
    @classmethod
    def validate_scopus_id(cls, v):
        if v is not None:
            v = v.strip()
            if v:
                if not v.isdigit():
                    raise ValueError("Scopus ID must be numeric")
                if len(v) < 5 or len(v) > 15:
                    raise ValueError("Scopus ID must be between 5 and 15 digits")
        return v

    @field_validator("wos_id")
    @classmethod
    def validate_wos_id(cls, v):
        if v is not None:
            v = v.strip()
            if v:
                wos_pattern = r'^[A-Z]-\d{4}-\d{4}$|^[A-Za-z0-9\-]{5,20}$'
                if not re.match(wos_pattern, v):
                    raise ValueError("Invalid Web of Science ID format")
        return v


class FacultyCreateRequest(BaseModel):
    """Schema for admin creating a faculty member."""
    full_name: str
    email: str
    password: str
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
        return v

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v):
        v = v.strip().lower()
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_pattern, v):
            raise ValueError("Invalid email format")
        # Faculty must use raisoni.net domain
        if not v.endswith("@raisoni.net"):
            raise ValueError("Faculty must register with a @raisoni.net email address")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
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
        orcid_pattern = r'^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$|^\d{16}$'
        if not re.match(orcid_pattern, v):
            raise ValueError("Invalid ORCID ID format")
        if len(v) == 16:
            v = f"{v[:4]}-{v[4:8]}-{v[8:12]}-{v[12:]}"
        return v

    @field_validator("scopus_id")
    @classmethod
    def validate_scopus_id(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Scopus ID is required")
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
        wos_pattern = r'^[A-Z]-\d{4}-\d{4}$|^[A-Za-z0-9\-]{5,20}$'
        if not re.match(wos_pattern, v):
            raise ValueError("Invalid Web of Science ID format")
        return v


class FacultyUpdateRequest(BaseModel):
    """Schema for admin updating a faculty member."""
    full_name: Optional[str] = None
    department: Optional[str] = None
    orcid_id: Optional[str] = None
    scopus_id: Optional[str] = None
    wos_id: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("department")
    @classmethod
    def validate_department(cls, v):
        if v is not None:
            valid_departments = ["CSE"]
            if v not in valid_departments:
                raise ValueError(f"Invalid department. Must be one of: {', '.join(valid_departments)}")
        return v


class FacultyStatusUpdate(BaseModel):
    """Schema for toggling faculty active status."""
    is_active: bool
