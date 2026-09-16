"""
ResearchAtlas - Unified Research Paper Service

Supports fetching publications from all 4 platforms:
- ORCID
- Scopus
- Google Scholar
- Web of Science

All platforms return normalized publication data in the same format.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId
import httpx
import asyncio

from app.database.database import get_collection
from app.models.publication import Publication
from app.services.orcid_service import OrcidService


class UnifiedResearchPaperService:
    """Unified service for fetching publications from all platforms."""
    
    def __init__(self):
        self.publications_collection = "research_publications"
        self.orcid_service = OrcidService()
    
    def _get_publications_collection(self):
        """Get publications collection."""
        return get_collection(self.publications_collection)
    
    async def fetch_publications(
        self,
        faculty_id: str,
        faculty_name: str,
        platform: str,
        identifiers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Fetch publications from specified platform.
        
        Args:
            faculty_id: Faculty member ID
            faculty_name: Faculty member name
            platform: Platform name (ORCID, Scopus, Google Scholar, Web of Science)
            identifiers: Platform-specific identifiers
        
        Returns:
            Dictionary with fetch results
        """
        try:
            if platform == "ORCID":
                return await self._fetch_orcid(faculty_id, faculty_name, identifiers)
            elif platform == "Scopus":
                return await self._fetch_scopus(faculty_id, faculty_name, identifiers)
            elif platform == "Google Scholar":
                return await self._fetch_google_scholar(faculty_id, faculty_name, identifiers)
            elif platform == "Web of Science":
                return await self._fetch_wos(faculty_id, faculty_name, identifiers)
            else:
                return {
                    "success": False,
                    "faculty_id": faculty_id,
                    "faculty_name": faculty_name,
                    "source": platform,
                    "fetched_count": 0,
                    "duplicates_removed": 0,
                    "unique_count": 0,
                    "stored_count": 0,
                    "status": "failed",
                    "error": f"Unsupported platform: {platform}",
                    "publications": []
                }
        except Exception as e:
            return {
                "success": False,
                "faculty_id": faculty_id,
                "faculty_name": faculty_name,
                "source": platform,
                "fetched_count": 0,
                "duplicates_removed": 0,
                "unique_count": 0,
                "stored_count": 0,
                "status": "failed",
                "error": str(e),
                "publications": []
            }
    
    async def _fetch_orcid(
        self,
        faculty_id: str,
        faculty_name: str,
        identifiers: Dict[str, str]
    ) -> Dict[str, Any]:
        """Fetch publications from ORCID."""
        orcid_id = identifiers.get("orcid_id", "")
        
        if not orcid_id:
            return {
                "success": False,
                "faculty_id": faculty_id,
                "faculty_name": faculty_name,
                "source": "ORCID",
                "fetched_count": 0,
                "duplicates_removed": 0,
                "unique_count": 0,
                "stored_count": 0,
                "status": "failed",
                "error": "ORCID ID not provided",
                "publications": []
            }
        
        # Fetch from ORCID
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
                "stored_count": 0,
                "status": "failed",
                "error": "Failed to fetch data from ORCID",
                "publications": []
            }
        
        works = orcid_data.get("works", [])
        fetched_count = len(works)
        
        # Normalize ORCID works to unified format
        normalized_works = self._normalize_orcid_works(faculty_id, faculty_name, works)
        
        # Detect and remove duplicates
        unique_works, duplicates_removed = self._detect_and_remove_duplicates(normalized_works)
        
        # Store in MongoDB
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
    
    async def _fetch_scopus(
        self,
        faculty_id: str,
        faculty_name: str,
        identifiers: Dict[str, str]
    ) -> Dict[str, Any]:
        """Fetch publications from Scopus."""
        scopus_id = identifiers.get("scopus_id", "")
        
        if not scopus_id:
            return {
                "success": False,
                "faculty_id": faculty_id,
                "faculty_name": faculty_name,
                "source": "Scopus",
                "fetched_count": 0,
                "duplicates_removed": 0,
                "unique_count": 0,
                "stored_count": 0,
                "status": "failed",
                "error": "Scopus ID not provided",
                "publications": []
            }
        
        try:
            # Fetch from Scopus API
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Note: This is a placeholder - actual Scopus API requires API key
                # For now, return mock data structure
                return {
                    "success": False,
                    "faculty_id": faculty_id,
                    "faculty_name": faculty_name,
                    "source": "Scopus",
                    "fetched_count": 0,
                    "duplicates_removed": 0,
                    "unique_count": 0,
                    "stored_count": 0,
                    "status": "failed",
                    "error": "Scopus API integration not yet implemented. Requires API key configuration.",
                    "publications": []
                }
        except Exception as e:
            return {
                "success": False,
                "faculty_id": faculty_id,
                "faculty_name": faculty_name,
                "source": "Scopus",
                "fetched_count": 0,
                "duplicates_removed": 0,
                "unique_count": 0,
                "stored_count": 0,
                "status": "failed",
                "error": str(e),
                "publications": []
            }
    
    async def _fetch_google_scholar(
        self,
        faculty_id: str,
        faculty_name: str,
        identifiers: Dict[str, str]
    ) -> Dict[str, Any]:
        """Fetch publications from Google Scholar."""
        gs_id = identifiers.get("google_scholar_id", "")
        
        if not gs_id:
            return {
                "success": False,
                "faculty_id": faculty_id,
                "faculty_name": faculty_name,
                "source": "Google Scholar",
                "fetched_count": 0,
                "duplicates_removed": 0,
                "unique_count": 0,
                "stored_count": 0,
                "status": "failed",
                "error": "Google Scholar ID not provided",
                "publications": []
            }
        
        try:
            # Note: Google Scholar doesn't have official API
            # This is a placeholder for future implementation
            return {
                "success": False,
                "faculty_id": faculty_id,
                "faculty_name": faculty_name,
                "source": "Google Scholar",
                "fetched_count": 0,
                "duplicates_removed": 0,
                "unique_count": 0,
                "stored_count": 0,
                "status": "failed",
                "error": "Google Scholar integration not yet implemented. No official API available.",
                "publications": []
            }
        except Exception as e:
            return {
                "success": False,
                "faculty_id": faculty_id,
                "faculty_name": faculty_name,
                "source": "Google Scholar",
                "fetched_count": 0,
                "duplicates_removed": 0,
                "unique_count": 0,
                "stored_count": 0,
                "status": "failed",
                "error": str(e),
                "publications": []
            }
    
    async def _fetch_wos(
        self,
        faculty_id: str,
        faculty_name: str,
        identifiers: Dict[str, str]
    ) -> Dict[str, Any]:
        """Fetch publications from Web of Science."""
        wos_id = identifiers.get("wos_id", "")
        
        if not wos_id:
            return {
                "success": False,
                "faculty_id": faculty_id,
                "faculty_name": faculty_name,
                "source": "Web of Science",
                "fetched_count": 0,
                "duplicates_removed": 0,
                "unique_count": 0,
                "stored_count": 0,
                "status": "failed",
                "error": "Web of Science ID not provided",
                "publications": []
            }
        
        try:
            # Note: WoS API requires institutional access
            # This is a placeholder for future implementation
            return {
                "success": False,
                "faculty_id": faculty_id,
                "faculty_name": faculty_name,
                "source": "Web of Science",
                "fetched_count": 0,
                "duplicates_removed": 0,
                "unique_count": 0,
                "stored_count": 0,
                "status": "failed",
                "error": "Web of Science integration not yet implemented. Requires institutional API access.",
                "publications": []
            }
        except Exception as e:
            return {
                "success": False,
                "faculty_id": faculty_id,
                "faculty_name": faculty_name,
                "source": "Web of Science",
                "fetched_count": 0,
                "duplicates_removed": 0,
                "unique_count": 0,
                "stored_count": 0,
                "status": "failed",
                "error": str(e),
                "publications": []
            }
    
    def _normalize_orcid_works(
        self,
        faculty_id: str,
        faculty_name: str,
        works: List[Dict]
    ) -> List[Dict]:
        """
        Normalize ORCID works to unified publication format.
        
        All platforms must return the same normalized format:
        - source
        - paper_name
        - year
        - date
        - author_name
        - work_type
        - doi
        - url
        - citation_count
        - publication_name
        - scopus_id
        - wos_id
        - issn
        - eissn
        - isbn
        - volume
        - issue
        - pages
        - publisher
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
                    doi = self._normalize_doi(doi)
                
                # Extract URL
                url = work.get("url", "")
                if not url and doi:
                    url = f"https://doi.org/{doi}"
                
                # Extract work type
                work_type_raw = work.get("type", "")
                work_type = self._normalize_work_type(work_type_raw)
                
                # Create unified publication document
                publication = {
                    "faculty_id": faculty_id,
                    "faculty_name": faculty_name,
                    "source": "ORCID",
                    "source_work_id": str(source_work_id),
                    "paper_name": title,
                    "year": year,
                    "date": publication_date,
                    "author_name": ", ".join(authors) if isinstance(authors, list) else authors,
                    "work_type": work_type,
                    "work_type_raw": work_type_raw,
                    "doi": doi,
                    "url": url,
                    "citation_count": None,  # ORCID doesn't provide citation counts
                    "publication_name": publication_venue,
                    "scopus_id": None,
                    "wos_id": None,
                    "issn": work.get("issn"),
                    "eissn": work.get("eissn"),
                    "isbn": work.get("isbn"),
                    "volume": work.get("volume"),
                    "issue": work.get("issue"),
                    "pages": work.get("pages"),
                    "publisher": work.get("publisher"),
                    "is_duplicate": False,
                    "duplicate_of": None,
                    "duplicate_reason": None,
                    "fetched_at": datetime.utcnow(),
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
                
                normalized.append(publication)
                
            except Exception as e:
                print(f"[UnifiedResearchPaperService] Error normalizing work: {str(e)}")
                continue
        
        return normalized
    
    def _normalize_doi(self, doi: str) -> str:
        """Normalize DOI by removing URL prefixes."""
        if not doi:
            return ""
        
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
        """Normalize work type to display format."""
        if not work_type_raw:
            return "Other"
        
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
        """Check if text looks like a URL."""
        if not text:
            return False
        
        import re
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
    ) -> tuple[List[Dict], int]:
        """Detect and remove duplicate publications."""
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
            
            # Check work ID
            if not is_duplicate:
                work_id = pub.get("source_work_id", "")
                if work_id:
                    if work_id in seen_work_ids:
                        is_duplicate = True
                        duplicate_reason = "same_work_id"
                    else:
                        seen_work_ids.add(work_id)
            
            # Check title + year
            if not is_duplicate:
                title = pub.get("paper_name", "").lower().strip()
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
        """Store publications in MongoDB."""
        collection = self._get_publications_collection()
        stored_count = 0
        
        for pub in publications:
            try:
                # Create unique key for upsert
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
                    filter_key = {
                        "faculty_id": pub["faculty_id"],
                        "source": pub["source"],
                        "paper_name": pub["paper_name"],
                        "year": pub.get("year")
                    }
                
                pub["updated_at"] = datetime.utcnow()
                
                result = await collection.update_one(
                    filter_key,
                    {"$set": pub},
                    upsert=True
                )
                
                stored_count += 1
                
            except Exception as e:
                print(f"[UnifiedResearchPaperService] Error storing publication: {str(e)}")
                continue
        
        return stored_count
    
    async def get_faculty_publications(
        self,
        faculty_id: str,
        source: Optional[str] = None,
        work_type: Optional[str] = None,
        year: Optional[int] = None,
        month: Optional[int] = None,
        date: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Dict]:
        """Get publications for a faculty member with optional filters."""
        collection = self._get_publications_collection()
        
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
        
        if month:
            query["date"] = {
                "$regex": f"^[0-9]{{4}}-{month:02d}"
            }
        
        if date:
            query["date"] = date
        
        if search:
            search_regex = {"$regex": search, "$options": "i"}
            query["$or"] = [
                {"paper_name": search_regex},
                {"author_name": search_regex},
                {"publication_name": search_regex},
                {"doi": search_regex}
            ]
        
        cursor = collection.find(query)
        publications = await cursor.to_list(length=None)
        
        return Publication.to_list_response(publications)
    
    async def get_publication_statistics(self, faculty_id: str) -> Dict[str, Any]:
        """Get publication statistics for a faculty member."""
        collection = self._get_publications_collection()
        
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
        
        by_source = {}
        by_work_type = {}
        years = []
        last_fetched = None
        
        for pub in publications:
            source = pub.get("source", "Unknown")
            by_source[source] = by_source.get(source, 0) + 1
            
            work_type = pub.get("work_type", "Other")
            by_work_type[work_type] = by_work_type.get(work_type, 0) + 1
            
            year = pub.get("year")
            if year:
                years.append(year)
            
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
