"""
ResearchAtlas - Citation Models

MongoDB models for citation management and historical data tracking.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId


class CitationRecord:
    """
    Citation record model for faculty research metrics.
    
    Stores current citation data from multiple sources:
    - Web of Science
    - Scopus
    - Google Scholar
    - ORCID
    - OpenAlex
    """
    
    COLLECTION_NAME = "citation_records"
    
    @staticmethod
    def create_record(
        faculty_id: str,
        faculty_name: str,
        web_of_science: Optional[Dict] = None,
        scopus: Optional[Dict] = None,
        google_scholar: Optional[Dict] = None,
        publons_url: str = "",
        scopus_url: str = "",
        google_scholar_url: str = "",
        researchgate_url: str = "",
        orcid: Optional[Dict] = None,
        openalex: Optional[Dict] = None,
        source_status: Optional[Dict] = None,
        last_fetched_at: Optional[datetime] = None,
    ) -> dict:
        """Create a new citation record document."""
        now = datetime.utcnow()
        
        return {
            "faculty_id": faculty_id,
            "faculty_name": faculty_name,
            "web_of_science": web_of_science or {
                "papers": 0,
                "citations": 0,
                "h_index": 0,
                "profile_url": ""
            },
            "scopus": scopus or {
                "papers": 0,
                "citations": 0,
                "h_index": 0,
                "profile_url": ""
            },
            "google_scholar": google_scholar or {
                "papers": 0,
                "citations": 0,
                "h_index": 0,
                "i10_index": 0,
                "profile_url": ""
            },
            "publons_url": publons_url,
            "scopus_url": scopus_url,
            "google_scholar_url": google_scholar_url,
            "researchgate_url": researchgate_url,
            "orcid": orcid or {
                "id": "",
                "url": ""
            },
            "openalex": openalex or {
                "id": "",
                "url": ""
            },
            "source_status": source_status or {
                "web_of_science": "not_configured",
                "scopus": "not_configured",
                "google_scholar": "not_configured",
                "orcid": "not_configured",
                "openalex": "not_configured"
            },
            "last_fetched_at": last_fetched_at,
            "created_at": now,
            "updated_at": now,
            "updated_by": None
        }
    
    @staticmethod
    def to_response(record: dict) -> dict:
        """Convert citation record to API response format."""
        if not record:
            return None
        
        return {
            "id": str(record["_id"]),
            "faculty_id": record.get("faculty_id", ""),
            "faculty_name": record.get("faculty_name", ""),
            "web_of_science": record.get("web_of_science", {}),
            "scopus": record.get("scopus", {}),
            "google_scholar": record.get("google_scholar", {}),
            "publons_url": record.get("publons_url", ""),
            "scopus_url": record.get("scopus_url", ""),
            "google_scholar_url": record.get("google_scholar_url", ""),
            "researchgate_url": record.get("researchgate_url", ""),
            "orcid": record.get("orcid", {}),
            "openalex": record.get("openalex", {}),
            "source_status": record.get("source_status", {}),
            "last_fetched_at": record.get("last_fetched_at").isoformat() if record.get("last_fetched_at") else None,
            "created_at": record.get("created_at").isoformat() if record.get("created_at") else None,
            "updated_at": record.get("updated_at").isoformat() if record.get("updated_at") else None,
            "updated_by": record.get("updated_by")
        }


class CitationHistory:
    """
    Citation history model for tracking changes over time.
    
    Stores snapshots of previous citation data whenever changes occur.
    """
    
    COLLECTION_NAME = "citation_history"
    
    @staticmethod
    def create_snapshot(
        citation_record_id: str,
        faculty_id: str,
        faculty_name: str,
        snapshot: Dict[str, Any],
        changed_fields: List[str],
        change_source: str,  # "manual" or "api"
        source_platform: str,  # "ORCID", "SCOPUS", "WOS", "GOOGLE_SCHOLAR", "OPENALEX", "MANUAL"
        created_by: Optional[str] = None
    ) -> dict:
        """Create a new citation history snapshot."""
        now = datetime.utcnow()
        
        return {
            "citation_record_id": citation_record_id,
            "faculty_id": faculty_id,
            "faculty_name": faculty_name,
            "snapshot": snapshot,
            "changed_fields": changed_fields,
            "change_source": change_source,
            "source_platform": source_platform,
            "created_at": now,
            "created_by": created_by
        }
    
    @staticmethod
    def to_response(record: dict) -> dict:
        """Convert citation history record to API response format."""
        if not record:
            return None
        
        return {
            "id": str(record["_id"]),
            "citation_record_id": record.get("citation_record_id", ""),
            "faculty_id": record.get("faculty_id", ""),
            "faculty_name": record.get("faculty_name", ""),
            "snapshot": record.get("snapshot", {}),
            "changed_fields": record.get("changed_fields", []),
            "change_source": record.get("change_source", ""),
            "source_platform": record.get("source_platform", ""),
            "created_at": record.get("created_at").isoformat() if record.get("created_at") else None,
            "created_by": record.get("created_by")
        }


class CitationFetchLog:
    """
    Citation fetch log model for tracking API fetch operations.
    
    Stores audit information about API calls and their results.
    """
    
    COLLECTION_NAME = "citation_fetch_logs"
    
    @staticmethod
    def create_log(
        faculty_id: str,
        faculty_name: str,
        source: str,
        status: str,
        started_at: datetime,
        completed_at: Optional[datetime] = None,
        records_found: int = 0,
        records_updated: int = 0,
        error_message: Optional[str] = None,
        triggered_by: Optional[str] = None
    ) -> dict:
        """Create a new fetch log entry."""
        return {
            "faculty_id": faculty_id,
            "faculty_name": faculty_name,
            "source": source,
            "status": status,
            "started_at": started_at,
            "completed_at": completed_at,
            "records_found": records_found,
            "records_updated": records_updated,
            "error_message": error_message,
            "triggered_by": triggered_by
        }
    
    @staticmethod
    def to_response(record: dict) -> dict:
        """Convert fetch log to API response format."""
        if not record:
            return None
        
        return {
            "id": str(record["_id"]),
            "faculty_id": record.get("faculty_id", ""),
            "faculty_name": record.get("faculty_name", ""),
            "source": record.get("source", ""),
            "status": record.get("status", ""),
            "started_at": record.get("started_at").isoformat() if record.get("started_at") else None,
            "completed_at": record.get("completed_at").isoformat() if record.get("completed_at") else None,
            "records_found": record.get("records_found", 0),
            "records_updated": record.get("records_updated", 0),
            "error_message": record.get("error_message"),
            "triggered_by": record.get("triggered_by")
        }
