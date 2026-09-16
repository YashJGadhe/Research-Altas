"""
Unified Publication Model

All platforms (ORCID, Scopus, Google Scholar, Web of Science) must normalize
their data into this common format.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class NormalizedPublication(BaseModel):
    """Common publication format for all platforms"""
    source: str = Field(..., description="Platform name: ORCID, Scopus, Google Scholar, Web of Science")
    paper_name: str = Field(..., description="Publication title")
    year: Optional[int] = Field(None, description="Publication year")
    date: Optional[str] = Field(None, description="Publication date (YYYY-MM-DD or YYYY)")
    author_name: Optional[str] = Field(None, description="Author name(s)")
    work_type: Optional[str] = Field(None, description="Work type (journal-article, conference-paper, etc.)")
    doi: Optional[str] = Field(None, description="Digital Object Identifier")
    url: Optional[str] = Field(None, description="Publication URL")
    citation_count: Optional[int] = Field(None, description="Citation count (platform-specific)")
    publication_name: Optional[str] = Field(None, description="Journal/Conference name")
    scopus_id: Optional[str] = Field(None, description="Scopus-specific ID")
    wos_id: Optional[str] = Field(None, description="Web of Science-specific ID")
    issn: Optional[str] = Field(None, description="ISSN")
    eissn: Optional[str] = Field(None, description="E-ISSN")
    isbn: Optional[str] = Field(None, description="ISBN")
    volume: Optional[str] = Field(None, description="Volume number")
    issue: Optional[str] = Field(None, description="Issue number")
    pages: Optional[str] = Field(None, description="Page range")
    publisher: Optional[str] = Field(None, description="Publisher name")


class ResearcherIdentifiers(BaseModel):
    """Researcher platform identifiers"""
    orcid: Optional[str] = None
    scopus_author_id: Optional[str] = None
    google_scholar_author_id: Optional[str] = None
    wos_researcher_id: Optional[str] = None


class ProfileURLs(BaseModel):
    """Researcher profile URLs"""
    orcid: Optional[str] = None
    scopus: Optional[str] = None
    google_scholar: Optional[str] = None
    wos: Optional[str] = None


class PlatformStatus(BaseModel):
    """Status of each platform fetch"""
    status: str = "pending"  # pending, success, failed
    publications_count: int = 0
    error: Optional[str] = None


class ResearcherSearchResponse(BaseModel):
    """Complete response for researcher search"""
    researcher_ids: ResearcherIdentifiers
    sources: dict = Field(default_factory=dict)
    publications: List[NormalizedPublication] = Field(default_factory=list)
    columns: List[str] = Field(default_factory=list)
    total_publications: int = 0
    mongodb: dict = Field(default_factory=dict)


class MongoDBPublication(BaseModel):
    """MongoDB publication document structure"""
    researcher_key: str
    platform: str
    source_record_id: str
    title: str
    authors: Optional[str] = None
    publication_year: Optional[int] = None
    publication_date: Optional[str] = None
    work_type: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    citation_count: Optional[int] = None
    issn: Optional[str] = None
    eissn: Optional[str] = None
    isbn: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    publisher: Optional[str] = None
    publication_name: Optional[str] = None
    scopus_id: Optional[str] = None
    wos_id: Optional[str] = None
    platform_data: dict = Field(default_factory=dict)
    raw_data: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class MongoDBResearcher(BaseModel):
    """MongoDB researcher document structure"""
    researcher_key: str
    identifiers: ResearcherIdentifiers
    profile_urls: ProfileURLs
    platforms: dict = Field(default_factory=dict)
    last_synced_at: Optional[datetime] = None
    sync_status: str = "pending"
    updated_at: datetime = Field(default_factory=datetime.utcnow)
