"""
ResearchAtlas - Citation Schemas

Pydantic schemas for citation management validation.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime


class CitationMetricsBase(BaseModel):
    """Base schema for citation metrics."""
    papers: int = Field(default=0, ge=0)
    citations: int = Field(default=0, ge=0)
    h_index: int = Field(default=0, ge=0)
    profile_url: str = ""


class GoogleScholarMetrics(CitationMetricsBase):
    """Google Scholar specific metrics."""
    i10_index: int = Field(default=0, ge=0)


class OrcidInfo(BaseModel):
    """ORCID information."""
    id: str = ""
    url: str = ""


class OpenAlexInfo(BaseModel):
    """OpenAlex information."""
    id: str = ""
    url: str = ""


class SourceStatus(BaseModel):
    """Status of each data source."""
    web_of_science: str = "not_configured"
    scopus: str = "not_configured"
    google_scholar: str = "not_configured"
    orcid: str = "not_configured"
    openalex: str = "not_configured"


class CitationRecordResponse(BaseModel):
    """Response schema for citation records."""
    id: str
    faculty_id: str
    faculty_name: str
    web_of_science: Dict[str, Any]
    scopus: Dict[str, Any]
    google_scholar: Dict[str, Any]
    publons_url: str
    scopus_url: str
    google_scholar_url: str
    researchgate_url: str
    orcid: Dict[str, Any]
    openalex: Dict[str, Any]
    source_status: Dict[str, Any]
    last_fetched_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    updated_by: Optional[str] = None


class CitationRecordListResponse(BaseModel):
    """Response schema for list of citation records."""
    records: List[CitationRecordResponse]
    total: int


class CitationUpdateRequest(BaseModel):
    """Request schema for manual citation update."""
    web_of_science: Optional[Dict[str, Any]] = None
    scopus: Optional[Dict[str, Any]] = None
    google_scholar: Optional[Dict[str, Any]] = None
    publons_url: Optional[str] = None
    scopus_url: Optional[str] = None
    google_scholar_url: Optional[str] = None
    researchgate_url: Optional[str] = None
    orcid: Optional[Dict[str, Any]] = None
    openalex: Optional[Dict[str, Any]] = None

    @field_validator("publons_url", "scopus_url", "google_scholar_url", "researchgate_url")
    @classmethod
    def validate_url(cls, v):
        if v and not v.startswith(("http://", "https://", "")):
            raise ValueError("URL must start with http:// or https://")
        return v


class CitationHistoryResponse(BaseModel):
    """Response schema for citation history."""
    id: str
    citation_record_id: str
    faculty_id: str
    faculty_name: str
    snapshot: Dict[str, Any]
    changed_fields: List[str]
    change_source: str
    source_platform: str
    created_at: Optional[str] = None
    created_by: Optional[str] = None


class CitationHistoryListResponse(BaseModel):
    """Response schema for list of citation history records."""
    history: List[CitationHistoryResponse]
    total: int


class FetchResultResponse(BaseModel):
    """Response schema for API fetch result."""
    success: bool
    message: str
    faculty_id: Optional[str] = None
    source: str
    records_found: int = 0
    records_updated: int = 0
    history_created: int = 0
    data: Optional[Dict[str, Any]] = None


class FetchLogResponse(BaseModel):
    """Response schema for fetch log."""
    id: str
    faculty_id: str
    faculty_name: str
    source: str
    status: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    records_found: int = 0
    records_updated: int = 0
    error_message: Optional[str] = None
    triggered_by: Optional[str] = None
