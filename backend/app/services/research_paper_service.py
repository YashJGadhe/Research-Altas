"""
ResearchAtlas - Research Paper Service

Service for managing research publications from various sources.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple
from bson import ObjectId
import re

from app.database.database import get_collection
from app.models.publication import Publication, PublicationHistory
from app.services.orcid_service import OrcidService


class ResearchPaperService:
    """Service for research publication management."""
    
    def __init__(self):
        self.publications_collection = Publication.COLLECTION_NAME
        self.history_collection = PublicationHistory.COLLECTION_NAME
        self.orcid_service = OrcidService()
    
    def _get_publications_collection(self):
        """Get publications collection."""
        return get_collection(self.publications_collection)
    
    def _get_history_collection(self):
        """Get history collection."""
        return get_collection(self.history_collection)
    
    async def fetch_orcid_publications(
        self,
        faculty_id: str,
        faculty_name: str,
        orcid_id: str
    ) -> Dict[str, Any]:
        """
        Fetch publications from ORCID for a faculty member.
        
        Args:
            faculty_id: Faculty member ID
            faculty_name: Faculty member name
            orcid_id: ORCID ID
        
        Returns:
            Dictionary with fetch results including publications and statistics
        """
        # Fetch ORCID data
        orcid_data = await self.orcid_service.get_researcher_profile(orcid_id)
        
        if not orcid_data:
            return {
                "success": False,
                "faculty_id": faculty_id,
                "faculty_name": faculty_name,
                "source": "ORCID",
                "fetched_count": 0,
                "duplicates_removed": 0,
                "unique_count": 0,
                "status": "failed",
                "error": "Failed to fetch data from ORCID",
                "publications": []
            }
        
        works = orcid_data.get("works", [])
        fetched_count = len(works)
        
        # Normalize and deduplicate works
        normalized_works = self._normalize_orcid_works(faculty_id, faculty_name, works)
        unique_works, duplicates_removed = self._detect_and_remove_duplicates(normalized_works)
        
        # Store publications in MongoDB
        stored_count = await self._store_publications(unique_works)
        
        return {
            "success": True,
            "faculty_id": faculty_id,
            "faculty_name": faculty_name,
            "source": "ORCID",
            "fetched_count": fetched_count,
            "duplicates_removed": duplicates_removed,
            "unique_count": len(unique_works),
            "stored_count": stored_count,
            "status": "success",
            "publications": unique_works
        }
    
    def _normalize_orcid_works(
        self,
        faculty_id: str,
        faculty_name: str,
        works: List[Dict]
    ) -> List[Dict]:
        """
        Normalize ORCID works to publication format.
        
        Args:
            faculty_id: Faculty member ID
            faculty_name: Faculty member name
            works: List of ORCID works
        
        Returns:
            List of normalized publication dictionaries
        """
        normalized = []
        
        for work in works:
            try:
                # Extract work ID
                source_work_id = work.get("put-code", "")
                
                # Extract title
                title = work.get("title", "")
                if not title or self._is_url_like(title):
                    title = "Untitled / Source Record"
                
                # Extract authors (ORCID doesn't always provide this)
                authors = work.get("contributors", [])
                if not authors:
                    authors = ["Not Available"]
                
                # Extract publication venue
                publication_venue = work.get("journal", "")
                if not publication_venue:
                    publication_venue = "Not Available"
                
                # Extract publication date
                publication_date = work.get("publication_date", "")
                year = work.get("publication_year")
                
                # Extract DOI
                doi = work.get("doi", "")
                if doi:
                    # Normalize DOI (remove URL prefix if present)
                    doi = self._normalize_doi(doi)
                
                # Extract URL
                url = work.get("url", "")
                if not url and doi:
                    url = f"https://doi.org/{doi}"
                
                # Extract work type
                work_type_raw = work.get("type", "")
                work_type = self._normalize_work_type(work_type_raw)
                
                # Create publication document
                publication = Publication.create_publication(
                    faculty_id=faculty_id,
                    faculty_name=faculty_name,
                    source="ORCID",
                    source_work_id=str(source_work_id),
                    title=title,
                    authors=authors if isinstance(authors, list) else [authors],
                    publication_venue=publication_venue,
                    publication_date=publication_date,
                    year=year,
                    doi=doi,
                    url=url,
                    work_type_raw=work_type_raw,
                    work_type=work_type,
                    source_metadata={
                        "orcid_work_id": source_work_id,
                        "raw_work_type": work_type_raw,
                        "source_url": url
                    }
                )
                
                normalized.append(publication)
                
            except Exception as e:
                print(f"[ResearchPaperService] Error normalizing work: {str(e)}")
                continue
        
        return normalized
    
    def _normalize_doi(self, doi: str) -> str:
        """
        Normalize DOI by removing URL prefixes.
        
        Args:
            doi: DOI string (may include URL prefix)
        
        Returns:
            Normalized DOI
        """
        if not doi:
            return ""
        
        # Remove common DOI URL prefixes
        doi = doi.strip()
        prefixes = [
            "https://doi.org/",
            "http://doi.org/",
            "https://dx.doi.org/",
            "http://dx.doi.org/",
            "doi:",
            "DOI:"
        ]
        
        for prefix in prefixes:
            if doi.startswith(prefix):
                doi = doi[len(prefix):]
                break
        
        return doi
    
    def _normalize_work_type(self, work_type_raw: str) -> str:
        """
        Normalize ORCID work type to display format.
        
        Args:
            work_type_raw: Raw ORCID work type
        
        Returns:
            Normalized work type for display
        """
        if not work_type_raw:
            return "Other"
        
        # Map ORCID work types to display names
        type_mapping = {
            "journal-article": "Journal Article",
            "conference-paper": "Conference Paper",
            "book": "Book",
            "book-chapter": "Book Chapter",
            "edited-book": "Edited Book",
            "preprint": "Preprint",
            "patent": "Patent",
            "thesis": "Thesis",
            "report": "Report",
            "dataset": "Dataset",
            "other": "Other"
        }
        
        return type_mapping.get(work_type_raw.lower(), "Other")
    
    def _is_url_like(self, text: str) -> bool:
        """
        Check if text looks like a URL.
        
        Args:
            text: Text to check
        
        Returns:
            True if text looks like a URL
        """
        if not text:
            return False
        
        url_patterns = [
            r'^https?://',
            r'^ftp://',
            r'^www\.',
            r'^doi:',
            r'^10\.\d{4,}'
        ]
        
        for pattern in url_patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def _detect_and_remove_duplicates(
        self,
        publications: List[Dict]
    ) -> Tuple[List[Dict], int]:
        """
        Detect and remove duplicate publications.
        
        Duplicate detection priority:
        1. DOI (if available)
        2. ORCID Work ID (source_work_id)
        3. Normalized title + year
        
        Args:
            publications: List of publication dictionaries
        
        Returns:
            Tuple of (unique publications, duplicates removed count)
        """
        seen_dois = set()
        seen_work_ids = set()
        seen_title_years = set()
        
        unique_publications = []
        duplicates_removed = 0
        
        for pub in publications:
            is_duplicate = False
            duplicate_reason = None
            
            # Check DOI
            doi = pub.get("doi", "")
            if doi:
                normalized_doi = doi.lower()
                if normalized_doi in seen_dois:
                    is_duplicate = True
                    duplicate_reason = "same_doi"
                else:
                    seen_dois.add(normalized_doi)
            
            # Check ORCID Work ID
            if not is_duplicate:
                work_id = pub.get("source_work_id", "")
                if work_id:
                    if work_id in seen_work_ids:
                        is_duplicate = True
                        duplicate_reason = "same_orcid_work_id"
                    else:
                        seen_work_ids.add(work_id)
            
            # Check title + year
            if not is_duplicate:
                title = pub.get("title", "").lower().strip()
                year = pub.get("year")
                
                if title and year:
                    title_year_key = f"{title}|{year}"
                    if title_year_key in seen_title_years:
                        is_duplicate = True
                        duplicate_reason = "same_title_and_year"
                    else:
                        seen_title_years.add(title_year_key)
            
            if is_duplicate:
                duplicates_removed += 1
                pub["is_duplicate"] = True
                pub["duplicate_reason"] = duplicate_reason
            else:
                unique_publications.append(pub)
        
        return unique_publications, duplicates_removed
    
    async def _store_publications(self, publications: List[Dict]) -> int:
        """
        Store publications in MongoDB.
        
        Uses upsert to prevent duplicate records on re-fetch.
        
        Args:
            publications: List of publication dictionaries
        
        Returns:
            Number of publications stored/updated
        """
        collection = self._get_publications_collection()
        stored_count = 0
        
        for pub in publications:
            try:
                # Create unique key for upsert
                # Priority: faculty_id + source + source_work_id
                # Fallback: faculty_id + source + DOI
                # Last resort: faculty_id + source + title + year
                
                filter_key = {}
                
                if pub.get("source_work_id"):
                    filter_key = {
                        "faculty_id": pub["faculty_id"],
                        "source": pub["source"],
                        "source_work_id": pub["source_work_id"]
                    }
                elif pub.get("doi"):
                    filter_key = {
                        "faculty_id": pub["faculty_id"],
                        "source": pub["source"],
                        "doi": pub["doi"]
                    }
                else:
                    # Use title + year as last resort
                    filter_key = {
                        "faculty_id": pub["faculty_id"],
                        "source": pub["source"],
                        "title": pub["title"],
                        "year": pub.get("year")
                    }
                
                # Update or insert
                pub["updated_at"] = datetime.utcnow()
                
                result = await collection.update_one(
                    filter_key,
                    {"$set": pub},
                    upsert=True
                )
                
                stored_count += 1
                
            except Exception as e:
                print(f"[ResearchPaperService] Error storing publication: {str(e)}")
                continue
        
        return stored_count
    
    async def get_faculty_publications(
        self,
        faculty_id: str,
        source: Optional[str] = None,
        work_type: Optional[str] = None,
        year: Optional[int] = None,
        search: Optional[str] = None,
        sort_by: str = "year_desc"
    ) -> List[Dict]:
        """
        Get publications for a faculty member with optional filters.
        
        Args:
            faculty_id: Faculty member ID
            source: Filter by source (ORCID, Scopus, etc.)
            work_type: Filter by work type
            year: Filter by year
            search: Search query (title, authors, venue, DOI)
            sort_by: Sort order (year_desc, year_asc)
        
        Returns:
            List of publication dictionaries
        """
        collection = self._get_publications_collection()
        
        # Build query
        query = {
            "faculty_id": faculty_id,
            "is_duplicate": False
        }
        
        if source:
            query["source"] = source
        
        if work_type:
            query["work_type"] = work_type
        
        if year:
            query["year"] = year
        
        if search:
            # Search in title, authors, venue, DOI
            search_regex = {"$regex": search, "$options": "i"}
            query["$or"] = [
                {"title": search_regex},
                {"authors": search_regex},
                {"publication_venue": search_regex},
                {"doi": search_regex}
            ]
        
        # Build sort
        sort_order = -1 if sort_by == "year_desc" else 1
        sort_criteria = [("year", sort_order), ("publication_date", sort_order)]
        
        # Execute query
        cursor = collection.find(query).sort(sort_criteria)
        publications = await cursor.to_list(length=None)
        
        return Publication.to_list_response(publications)
    
    async def get_publication_statistics(self, faculty_id: str) -> Dict[str, Any]:
        """
        Get publication statistics for a faculty member.
        
        Args:
            faculty_id: Faculty member ID
        
        Returns:
            Dictionary with statistics
        """
        collection = self._get_publications_collection()
        
        # Get all non-duplicate publications
        query = {"faculty_id": faculty_id, "is_duplicate": False}
        publications = await collection.find(query).to_list(length=None)
        
        if not publications:
            return {
                "total_publications": 0,
                "by_source": {},
                "by_work_type": {},
                "year_range": {"min": None, "max": None},
                "last_fetched": None
            }
        
        # Calculate statistics
        by_source = {}
        by_work_type = {}
        years = []
        last_fetched = None
        
        for pub in publications:
            # Count by source
            source = pub.get("source", "Unknown")
            by_source[source] = by_source.get(source, 0) + 1
            
            # Count by work type
            work_type = pub.get("work_type", "Other")
            by_work_type[work_type] = by_work_type.get(work_type, 0) + 1
            
            # Collect years
            year = pub.get("year")
            if year:
                years.append(year)
            
            # Track last fetched
            fetched_at = pub.get("fetched_at")
            if fetched_at:
                if last_fetched is None or fetched_at > last_fetched:
                    last_fetched = fetched_at
        
        return {
            "total_publications": len(publications),
            "by_source": by_source,
            "by_work_type": by_work_type,
            "year_range": {
                "min": min(years) if years else None,
                "max": max(years) if years else None
            },
            "last_fetched": last_fetched.isoformat() if last_fetched else None
        }
