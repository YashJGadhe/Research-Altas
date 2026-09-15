"""
ResearchAtlas - Publication Model

MongoDB model for storing research publications.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId


class Publication:
    """
    Publication model for storing research papers.
    
    Stores publication data from various sources (ORCID, Scopus, WoS, etc.)
    """
    
    COLLECTION_NAME = "research_publications"
    
    @staticmethod
    def create_publication(
        faculty_id: str,
        faculty_name: str,
        source: str,
        source_work_id: str,
        title: str,
        authors: List[str],
        publication_venue: str,
        publication_date: str,
        year: int,
        doi: str,
        url: str,
        work_type_raw: str,
        work_type: str,
        source_metadata: Optional[Dict] = None
    ) -> dict:
        """Create a new publication document."""
        now = datetime.utcnow()
        
        return {
            "faculty_id": faculty_id,
            "faculty_name": faculty_name,
            "source": source,
            "source_work_id": source_work_id,
            "title": title,
            "authors": authors,
            "publication_venue": publication_venue,
            "publication_date": publication_date,
            "year": year,
            "doi": doi,
            "url": url,
            "work_type_raw": work_type_raw,
            "work_type": work_type,
            "source_metadata": source_metadata or {},
            "is_duplicate": False,
            "duplicate_of": None,
            "duplicate_reason": None,
            "fetched_at": now,
            "created_at": now,
            "updated_at": now
        }
    
    @staticmethod
    def to_response(record: dict) -> dict:
        """Convert publication record to API response format."""
        if not record:
            return None
        
        return {
            "id": str(record["_id"]),
            "faculty_id": record.get("faculty_id", ""),
            "faculty_name": record.get("faculty_name", ""),
            "source": record.get("source", ""),
            "source_work_id": record.get("source_work_id", ""),
            "title": record.get("title", ""),
            "authors": record.get("authors", []),
            "publication_venue": record.get("publication_venue", ""),
            "publication_date": record.get("publication_date", ""),
            "year": record.get("year"),
            "doi": record.get("doi", ""),
            "url": record.get("url", ""),
            "work_type_raw": record.get("work_type_raw", ""),
            "work_type": record.get("work_type", ""),
            "is_duplicate": record.get("is_duplicate", False),
            "fetched_at": record.get("fetched_at").isoformat() if record.get("fetched_at") else None,
            "created_at": record.get("created_at").isoformat() if record.get("created_at") else None,
            "updated_at": record.get("updated_at").isoformat() if record.get("updated_at") else None
        }
    
    @staticmethod
    def to_list_response(records: list) -> list:
        """Convert list of publication records to API response format."""
        return [Publication.to_response(record) for record in records]


class PublicationHistory:
    """
    Publication history model for tracking changes to publication metadata.
    """
    
    COLLECTION_NAME = "research_publication_history"
    
    @staticmethod
    def create_history(
        publication_id: str,
        faculty_id: str,
        source: str,
        old_data: Dict,
        new_data: Dict,
        changed_fields: List[str],
        changed_by: str
    ) -> dict:
        """Create a new publication history record."""
        return {
            "publication_id": publication_id,
            "faculty_id": faculty_id,
            "source": source,
            "old_data": old_data,
            "new_data": new_data,
            "changed_fields": changed_fields,
            "changed_at": datetime.utcnow(),
            "changed_by": changed_by
        }
    
    @staticmethod
    def to_response(record: dict) -> dict:
        """Convert history record to API response format."""
        if not record:
            return None
        
        return {
            "id": str(record["_id"]),
            "publication_id": record.get("publication_id", ""),
            "faculty_id": record.get("faculty_id", ""),
            "source": record.get("source", ""),
            "old_data": record.get("old_data", {}),
            "new_data": record.get("new_data", {}),
            "changed_fields": record.get("changed_fields", []),
            "changed_at": record.get("changed_at").isoformat() if record.get("changed_at") else None,
            "changed_by": record.get("changed_by", "")
        }
