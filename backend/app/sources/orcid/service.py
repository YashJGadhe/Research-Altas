"""
ORCID Source Service

Fetches researcher publications from ORCID public API.
ORCID does NOT provide citation counts.
"""
import httpx
from typing import List, Optional, Dict, Any
from app.models.publication import NormalizedPublication
from app.core.config import settings


class ORCIDService:
    BASE_URL = "https://pub.orcid.org/v3.0"
    
    def __init__(self):
        self.headers = {
            "Accept": "application/json",
        }
        if settings.ORCID_CLIENT_ID and settings.ORCID_CLIENT_SECRET:
            # For member API (if credentials provided)
            pass
    
    async def fetch_publications(self, orcid_id: str) -> Dict[str, Any]:
        """
        Fetch all publications for a researcher from ORCID.
        
        Args:
            orcid_id: ORCID ID (e.g., "0000-0002-1825-0097")
        
        Returns:
            Dict with status, publications, and metadata
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Fetch works summary
                works_url = f"{self.BASE_URL}/{orcid_id}/works"
                response = await client.get(works_url, headers=self.headers)
                
                if response.status_code != 200:
                    return {
                        "status": "failed",
                        "publications": [],
                        "error": f"ORCID API returned status {response.status_code}",
                        "publications_count": 0
                    }
                
                works_data = response.json()
                publications = self._normalize_works(works_data, orcid_id)
                
                return {
                    "status": "success",
                    "publications": publications,
                    "error": None,
                    "publications_count": len(publications)
                }
        
        except Exception as e:
            return {
                "status": "failed",
                "publications": [],
                "error": str(e),
                "publications_count": 0
            }
    
    def _normalize_works(self, works_data: Dict, orcid_id: str) -> List[NormalizedPublication]:
        """Normalize ORCID works into common publication format"""
        publications = []
        
        groups = works_data.get("group", [])
        
        for group in groups:
            summaries = group.get("work-summary", [])
            if not summaries:
                continue
            
            # Use the first summary (most detailed)
            work = summaries[0]
            
            try:
                # Extract title
                title = self._extract_title(work)
                if not title:
                    continue
                
                # Extract publication date
                pub_date = self._extract_date(work)
                year = self._extract_year(work)
                
                # Extract DOI
                doi = self._extract_doi(work)
                
                # Extract work type
                work_type = work.get("type", "")
                
                # Extract journal/conference name
                journal_name = self._extract_journal(work)
                
                # Extract URL
                url = work.get("url", {}).get("value") if work.get("url") else None
                
                # Extract publication details
                volume = self._extract_field(work, "volume")
                issue = self._extract_field(work, "issue")
                pages = self._extract_field(work, "pages")
                
                # Extract authors
                authors = self._extract_authors(work)
                
                # ORCID does NOT provide citation counts
                publication = NormalizedPublication(
                    source="ORCID",
                    paper_name=title,
                    year=year,
                    date=pub_date,
                    author_name=authors,
                    work_type=work_type,
                    doi=doi,
                    url=url,
                    citation_count=None,  # ORCID doesn't provide citations
                    publication_name=journal_name,
                    scopus_id=None,
                    wos_id=None,
                    issn=None,
                    eissn=None,
                    isbn=None,
                    volume=volume,
                    issue=issue,
                    pages=pages,
                    publisher=None
                )
                
                publications.append(publication)
            
            except Exception as e:
                print(f"Error normalizing ORCID work: {e}")
                continue
        
        return publications
    
    def _extract_title(self, work: Dict) -> Optional[str]:
        """Extract publication title"""
        title_obj = work.get("title", {})
        if title_obj:
            return title_obj.get("title", {}).get("value")
        return None
    
    def _extract_date(self, work: Dict) -> Optional[str]:
        """Extract publication date"""
        pub_date = work.get("publication-date", {})
        if not pub_date:
            return None
        
        year = pub_date.get("year", {}).get("value")
        month = pub_date.get("month", {}).get("value")
        day = pub_date.get("day", {}).get("value")
        
        if year:
            if month and day:
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            elif month:
                return f"{year}-{month.zfill(2)}"
            return year
        
        return None
    
    def _extract_year(self, work: Dict) -> Optional[int]:
        """Extract publication year"""
        pub_date = work.get("publication-date", {})
        if pub_date:
            year = pub_date.get("year", {}).get("value")
            if year:
                try:
                    return int(year)
                except:
                    pass
        return None
    
    def _extract_doi(self, work: Dict) -> Optional[str]:
        """Extract DOI from external identifiers"""
        external_ids = work.get("external-ids", {}).get("external-id", [])
        
        for ext_id in external_ids:
            if ext_id.get("external-id-type") == "doi":
                return ext_id.get("external-id-value")
        
        return None
    
    def _extract_journal(self, work: Dict) -> Optional[str]:
        """Extract journal/conference name"""
        journal_title = work.get("journal-title", {})
        if journal_title:
            return journal_title.get("value")
        return None
    
    def _extract_field(self, work: Dict, field: str) -> Optional[str]:
        """Extract a specific field from citation details"""
        citation = work.get("journal-title", {})
        # ORCID doesn't always have detailed citation info
        return None
    
    def _extract_authors(self, work: Dict) -> Optional[str]:
        """Extract authors as comma-separated string"""
        contributors = work.get("contributors", {}).get("contributor", [])
        
        if not contributors:
            return None
        
        authors = []
        for contrib in contributors:
            credit_name = contrib.get("credit-name", {}).get("value")
            if credit_name:
                authors.append(credit_name)
        
        return ", ".join(authors) if authors else None
    
    def get_profile_url(self, orcid_id: str) -> str:
        """Get ORCID profile URL"""
        return f"https://orcid.org/{orcid_id}"
