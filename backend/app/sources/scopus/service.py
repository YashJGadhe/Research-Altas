"""
Scopus Source Service

Fetches researcher publications from Scopus Search API.
Uses AU-ID query to search by Scopus Author ID.
"""
import httpx
from typing import List, Optional, Dict, Any
from app.models.publication import NormalizedPublication
from app.core.config import settings


class ScopusService:
    SEARCH_URL = "https://api.elsevier.com/content/search/scopus"
    
    def __init__(self):
        self.api_key = settings.SCOPUS_API_KEY
    
    async def fetch_publications(self, scopus_author_id: str) -> Dict[str, Any]:
        """
        Fetch all publications for a researcher from Scopus.
        
        Args:
            scopus_author_id: Scopus Author ID (e.g., "57487968600")
        
        Returns:
            Dict with status, publications, and metadata
        """
        if not self.api_key:
            return {
                "status": "failed",
                "publications": [],
                "error": "Scopus API key not configured",
                "publications_count": 0
            }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Use Scopus Search API with AU-ID query
                params = {
                    "query": f"AU-ID({scopus_author_id})",
                    "apiKey": self.api_key,
                    "httpAccept": "application/json",
                    "count": 100,  # Max results per page
                    "start": 0
                }
                
                all_publications = []
                start = 0
                
                # Paginate through results
                while True:
                    params["start"] = start
                    response = await client.get(self.SEARCH_URL, params=params)
                    
                    if response.status_code != 200:
                        if start == 0:
                            return {
                                "status": "failed",
                                "publications": [],
                                "error": f"Scopus API returned status {response.status_code}",
                                "publications_count": 0
                            }
                        break
                    
                    data = response.json()
                    search_results = data.get("search-results", {})
                    entries = search_results.get("entry", [])
                    
                    if not entries:
                        break
                    
                    publications = self._normalize_entries(entries, scopus_author_id)
                    all_publications.extend(publications)
                    
                    # Check if there are more results
                    total_results = int(search_results.get("opensearch:totalResults", 0))
                    start += len(entries)
                    
                    if start >= total_results:
                        break
                
                return {
                    "status": "success",
                    "publications": all_publications,
                    "error": None,
                    "publications_count": len(all_publications)
                }
        
        except Exception as e:
            return {
                "status": "failed",
                "publications": [],
                "error": str(e),
                "publications_count": 0
            }
    
    def _normalize_entries(self, entries: List[Dict], scopus_author_id: str) -> List[NormalizedPublication]:
        """Normalize Scopus entries into common publication format"""
        publications = []
        
        for entry in entries:
            try:
                # Extract title
                title = entry.get("dc:title")
                if not title:
                    continue
                
                # Extract publication date
                date = entry.get("prism:coverDate")
                year = self._extract_year(date)
                
                # Extract work type
                work_type = entry.get("subtypeDescription") or entry.get("prism:aggregationType")
                
                # Extract DOI
                doi = None
                identifiers = entry.get("prism:doi")
                if identifiers:
                    doi = identifiers
                
                # Extract Scopus ID (EID)
                scopus_id = entry.get("eid")
                
                # Extract citation count
                citation_count = None
                cited_by = entry.get("citedby-count")
                if cited_by:
                    try:
                        citation_count = int(cited_by)
                    except:
                        pass
                
                # Extract publication/journal name
                publication_name = entry.get("prism:publicationName")
                
                # Extract ISSN
                issn = entry.get("prism:issn")
                eissn = entry.get("prism:eIssn")
                
                # Extract volume, issue, pages
                volume = entry.get("prism:volume")
                issue = entry.get("prism:issueIdentifier")
                pages = entry.get("prism:pageRange")
                
                # Extract authors
                authors = self._extract_authors(entry)
                
                # Extract URL
                url = None
                links = entry.get("link", [])
                for link in links:
                    if link.get("@ref") == "scopus":
                        url = link.get("@href")
                        break
                
                publication = NormalizedPublication(
                    source="Scopus",
                    paper_name=title,
                    year=year,
                    date=date,
                    author_name=authors,
                    work_type=work_type,
                    doi=doi,
                    url=url,
                    citation_count=citation_count,
                    publication_name=publication_name,
                    scopus_id=scopus_id,
                    wos_id=None,
                    issn=issn,
                    eissn=eissn,
                    isbn=None,
                    volume=volume,
                    issue=issue,
                    pages=pages,
                    publisher=entry.get("dc:publisher")
                )
                
                publications.append(publication)
            
            except Exception as e:
                print(f"Error normalizing Scopus entry: {e}")
                continue
        
        return publications
    
    def _extract_year(self, date_str: Optional[str]) -> Optional[int]:
        """Extract year from date string"""
        if not date_str:
            return None
        
        try:
            # Format: YYYY-MM-DD
            year = int(date_str.split("-")[0])
            return year
        except:
            return None
    
    def _extract_authors(self, entry: Dict) -> Optional[str]:
        """Extract authors as comma-separated string"""
        authors_list = []
        
        # Try to get authors from dc:creator
        creators = entry.get("dc:creator")
        if creators:
            if isinstance(creators, str):
                authors_list.append(creators)
            elif isinstance(creators, list):
                for creator in creators:
                    if isinstance(creator, dict):
                        name = creator.get("$")
                        if name:
                            authors_list.append(name)
                    elif isinstance(creator, str):
                        authors_list.append(creator)
        
        return ", ".join(authors_list) if authors_list else None
    
    def get_profile_url(self, scopus_author_id: str) -> str:
        """Get Scopus author profile URL"""
        return f"https://www.scopus.com/authid/detail.uri?authorId={scopus_author_id}"
