"""
Google Scholar Source Service

Fetches researcher publications from Google Scholar using scholarly library.
Note: Google Scholar doesn't have an official API, so we use web scraping.
"""
import asyncio
from typing import List, Optional, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from app.models.publication import NormalizedPublication
from app.core.config import settings


class GoogleScholarService:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1)
    
    async def fetch_publications(self, google_scholar_author_id: str) -> Dict[str, Any]:
        """
        Fetch all publications for a researcher from Google Scholar.
        
        Args:
            google_scholar_author_id: Google Scholar Author ID
        
        Returns:
            Dict with status, publications, and metadata
        """
        try:
            # Run scholarly in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                self._fetch_scholarly_data,
                google_scholar_author_id
            )
            return result
        
        except Exception as e:
            return {
                "status": "failed",
                "publications": [],
                "error": str(e),
                "publications_count": 0
            }
    
    def _fetch_scholarly_data(self, author_id: str) -> Dict[str, Any]:
        """Fetch data using scholarly library (runs in thread)"""
        try:
            from scholarly import scholarly
            
            # Search for author by ID
            author = scholarly.search_author_id(author_id)
            
            if not author:
                return {
                    "status": "failed",
                    "publications": [],
                    "error": "Author not found on Google Scholar",
                    "publications_count": 0
                }
            
            # Fill author with publications
            scholarly.fill(author, sections=['publications'])
            
            publications_data = author.get('publications', [])
            publications = self._normalize_publications(publications_data, author_id)
            
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
                "error": f"Google Scholar error: {str(e)}",
                "publications_count": 0
            }
    
    def _normalize_publications(self, publications_data: List[Dict], author_id: str) -> List[NormalizedPublication]:
        """Normalize Google Scholar publications into common format"""
        publications = []
        
        for pub_data in publications_data:
            try:
                bib = pub_data.get('bib', {})
                
                # Extract title
                title = bib.get('title')
                if not title:
                    continue
                
                # Extract year
                year = None
                pub_year = bib.get('pub_year')
                if pub_year:
                    try:
                        year = int(pub_year)
                    except:
                        pass
                
                # Extract authors
                authors_list = bib.get('author', [])
                authors = ", ".join(authors_list) if authors_list else None
                
                # Extract publication/journal name
                publication_name = bib.get('journal') or bib.get('venue')
                
                # Extract citation count
                citation_count = pub_data.get('num_citations')
                
                # Extract URL
                url = pub_data.get('pub_url') or pub_data.get('eprint_url')
                
                # Google Scholar doesn't provide DOI, ISSN, etc. in most cases
                # We'll try to extract what we can
                
                publication = NormalizedPublication(
                    source="Google Scholar",
                    paper_name=title,
                    year=year,
                    date=str(year) if year else None,
                    author_name=authors,
                    work_type=None,  # Google Scholar doesn't provide work type
                    doi=None,  # Not usually available
                    url=url,
                    citation_count=citation_count,
                    publication_name=publication_name,
                    scopus_id=None,
                    wos_id=None,
                    issn=None,
                    eissn=None,
                    isbn=None,
                    volume=None,
                    issue=None,
                    pages=None,
                    publisher=None
                )
                
                publications.append(publication)
            
            except Exception as e:
                print(f"Error normalizing Google Scholar publication: {e}")
                continue
        
        return publications
    
    def get_profile_url(self, author_id: str) -> str:
        """Get Google Scholar profile URL"""
        return f"https://scholar.google.com/citations?user={author_id}"
