"""
Web of Science Source Service

Fetches researcher publications from Web of Science API.
Requires institutional API access.
"""
import httpx
from typing import List, Optional, Dict, Any
from app.models.publication import NormalizedPublication
from app.core.config import settings


class WOSService:
    BASE_URL = "https://api.clarivate.com/apis/wos-starter/v1"
    
    def __init__(self):
        self.api_key = settings.WOS_API_KEY
    
    async def fetch_publications(self, wos_researcher_id: str) -> Dict[str, Any]:
        """
        Fetch all publications for a researcher from Web of Science.
        
        Args:
            wos_researcher_id: Web of Science Researcher ID
        
        Returns:
            Dict with status, publications, and metadata
        """
        if not self.api_key:
            return {
                "status": "failed",
                "publications": [],
                "error": "Web of Science API key not configured",
                "publications_count": 0
            }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                headers = {
                    "X-API-Key": self.api_key,
                    "Accept": "application/json"
                }
                
                # Search for documents by researcher
                # WoS uses different identifiers - we'll try multiple approaches
                all_publications = []
                
                # Try searching by researcher ID
                params = {
                    "query": f"RI={wos_researcher_id}",
                    "limit": 100,
                    "page": 1
                }
                
                while True:
                    response = await client.get(
                        f"{self.BASE_URL}/documents",
                        headers=headers,
                        params=params
                    )
                    
                    if response.status_code != 200:
                        if params["page"] == 1:
                            return {
                                "status": "failed",
                                "publications": [],
                                "error": f"Web of Science API returned status {response.status_code}",
                                "publications_count": 0
                            }
                        break
                    
                    data = response.json()
                    documents = data.get("hits", [])
                    
                    if not documents:
                        break
                    
                    publications = self._normalize_documents(documents, wos_researcher_id)
                    all_publications.extend(publications)
                    
                    # Check if there are more pages
                    total_pages = data.get("metadata", {}).get("total", 0)
                    if params["page"] >= total_pages:
                        break
                    
                    params["page"] += 1
                
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
    
    def _normalize_documents(self, documents: List[Dict], wos_researcher_id: str) -> List[NormalizedPublication]:
        """Normalize Web of Science documents into common format"""
        publications = []
        
        for doc in documents:
            try:
                # Extract title
                title = doc.get("title")
                if not title:
                    continue
                
                # Extract publication date
                date = doc.get("publication_date") or doc.get("published_date")
                year = self._extract_year(date)
                
                # Extract work type
                work_type = doc.get("type") or doc.get("doctype")
                
                # Extract DOI
                doi = doc.get("doi")
                
                # Extract WoS ID
                wos_id = doc.get("uid") or doc.get("wos_id") or doc.get("ut")
                
                # Extract citation count
                citation_count = None
                times_cited = doc.get("times_cited")
                if times_cited is not None:
                    try:
                        citation_count = int(times_cited)
                    except:
                        pass
                
                # Extract publication/journal name
                publication_name = doc.get("source_title") or doc.get("journal")
                
                # Extract ISSN
                issn = doc.get("issn")
                eissn = doc.get("eissn")
                
                # Extract volume, issue, pages
                volume = doc.get("volume")
                issue = doc.get("issue")
                pages = doc.get("pages")
                
                # Extract authors
                authors = self._extract_authors(doc)
                
                # Extract URL
                url = doc.get("url") or (f"https://www.webofscience.com/wos/woscc/full-record/{wos_id}" if wos_id else None)
                
                publication = NormalizedPublication(
                    source="Web of Science",
                    paper_name=title,
                    year=year,
                    date=date,
                    author_name=authors,
                    work_type=work_type,
                    doi=doi,
                    url=url,
                    citation_count=citation_count,
                    publication_name=publication_name,
                    scopus_id=None,
                    wos_id=wos_id,
                    issn=issn,
                    eissn=eissn,
                    isbn=None,
                    volume=volume,
                    issue=issue,
                    pages=pages,
                    publisher=doc.get("publisher")
                )
                
                publications.append(publication)
            
            except Exception as e:
                print(f"Error normalizing WoS document: {e}")
                continue
        
        return publications
    
    def _extract_year(self, date_str: Optional[str]) -> Optional[int]:
        """Extract year from date string"""
        if not date_str:
            return None
        
        try:
            # Try various date formats
            if "-" in date_str:
                year = int(date_str.split("-")[0])
            elif "/" in date_str:
                year = int(date_str.split("/")[-1])
            else:
                year = int(date_str[:4])
            return year
        except:
            return None
    
    def _extract_authors(self, doc: Dict) -> Optional[str]:
        """Extract authors as comma-separated string"""
        authors_list = []
        
        # Try different author fields
        authors = doc.get("authors", [])
        if isinstance(authors, list):
            for author in authors:
                if isinstance(author, dict):
                    name = author.get("name") or author.get("full_name")
                    if name:
                        authors_list.append(name)
                elif isinstance(author, str):
                    authors_list.append(author)
        
        return ", ".join(authors_list) if authors_list else None
    
    def get_profile_url(self, wos_researcher_id: str) -> str:
        """Get Web of Science researcher profile URL"""
        return f"https://www.webofscience.com/wos/author/record/{wos_researcher_id}"
