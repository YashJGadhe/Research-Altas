"""
Unified Researcher Service

Coordinates fetching from all platforms and handles MongoDB persistence.
"""
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from bson import ObjectId

from app.sources.orcid.service import ORCIDService
from app.sources.scopus.service import ScopusService
from app.sources.google_scholar.service import GoogleScholarService
from app.sources.wos.service import WOSService
from app.models.publication import (
    NormalizedPublication,
    ResearcherIdentifiers,
    ProfileURLs,
    MongoDBPublication,
    MongoDBResearcher
)
from app.database.mongodb import get_database


class UnifiedResearcherService:
    def __init__(self):
        self.orcid_service = ORCIDService()
        self.scopus_service = ScopusService()
        self.google_scholar_service = GoogleScholarService()
        self.wos_service = WOSService()
    
    async def search_researcher(
        self,
        orcid: Optional[str] = None,
        scopus_author_id: Optional[str] = None,
        google_scholar_author_id: Optional[str] = None,
        wos_researcher_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for a researcher across multiple platforms.
        
        Args:
            orcid: ORCID ID
            scopus_author_id: Scopus Author ID
            google_scholar_author_id: Google Scholar Author ID
            wos_researcher_id: Web of Science Researcher ID
        
        Returns:
            Complete researcher data with publications from all platforms
        """
        # Create researcher key (unique identifier)
        researcher_key = self._create_researcher_key(
            orcid, scopus_author_id, google_scholar_author_id, wos_researcher_id
        )
        
        # Create identifiers object
        identifiers = ResearcherIdentifiers(
            orcid=orcid,
            scopus_author_id=scopus_author_id,
            google_scholar_author_id=google_scholar_author_id,
            wos_researcher_id=wos_researcher_id
        )
        
        # Create profile URLs
        profile_urls = ProfileURLs(
            orcid=self.orcid_service.get_profile_url(orcid) if orcid else None,
            scopus=self.scopus_service.get_profile_url(scopus_author_id) if scopus_author_id else None,
            google_scholar=self.google_scholar_service.get_profile_url(google_scholar_author_id) if google_scholar_author_id else None,
            wos=self.wos_service.get_profile_url(wos_researcher_id) if wos_researcher_id else None
        )
        
        # Fetch from all platforms in parallel
        tasks = []
        sources_status = {}
        
        if orcid:
            tasks.append(self._fetch_platform("ORCID", self.orcid_service.fetch_publications(orcid)))
        
        if scopus_author_id:
            tasks.append(self._fetch_platform("Scopus", self.scopus_service.fetch_publications(scopus_author_id)))
        
        if google_scholar_author_id:
            tasks.append(self._fetch_platform("Google Scholar", self.google_scholar_service.fetch_publications(google_scholar_author_id)))
        
        if wos_researcher_id:
            tasks.append(self._fetch_platform("Web of Science", self.wos_service.fetch_publications(wos_researcher_id)))
        
        # Execute all fetch tasks
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        all_publications = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                platform_name = ["ORCID", "Scopus", "Google Scholar", "Web of Science"][i]
                sources_status[platform_name] = {
                    "status": "failed",
                    "publications_count": 0,
                    "error": str(result)
                }
            else:
                platform_name = result["platform"]
                sources_status[platform_name] = {
                    "status": result["status"],
                    "publications_count": result["publications_count"],
                    "error": result.get("error")
                }
                all_publications.extend(result["publications"])
        
        # Save to MongoDB
        mongodb_result = await self._save_to_mongodb(
            researcher_key=researcher_key,
            identifiers=identifiers,
            profile_urls=profile_urls,
            platforms=sources_status,
            publications=all_publications
        )
        
        # Prepare response
        columns = [
            "source", "paper_name", "year", "date", "author_name", "work_type",
            "doi", "url", "citation_count", "publication_name", "scopus_id",
            "wos_id", "issn", "eissn", "isbn", "volume", "issue", "pages", "publisher"
        ]
        
        response = {
            "researcher_ids": identifiers.dict(),
            "sources": sources_status,
            "publications": [pub.dict() for pub in all_publications],
            "columns": columns,
            "total_publications": len(all_publications),
            "mongodb": mongodb_result
        }
        
        return response
    
    async def _fetch_platform(self, platform_name: str, fetch_task) -> Dict[str, Any]:
        """Fetch from a single platform"""
        try:
            result = await fetch_task
            result["platform"] = platform_name
            return result
        except Exception as e:
            return {
                "platform": platform_name,
                "status": "failed",
                "publications": [],
                "error": str(e),
                "publications_count": 0
            }
    
    def _create_researcher_key(
        self,
        orcid: Optional[str],
        scopus_author_id: Optional[str],
        google_scholar_author_id: Optional[str],
        wos_researcher_id: Optional[str]
    ) -> str:
        """Create a unique researcher key"""
        parts = []
        if orcid:
            parts.append(f"orcid:{orcid}")
        if scopus_author_id:
            parts.append(f"scopus:{scopus_author_id}")
        if google_scholar_author_id:
            parts.append(f"gscholar:{google_scholar_author_id}")
        if wos_researcher_id:
            parts.append(f"wos:{wos_researcher_id}")
        
        return "|".join(parts) if parts else "unknown"
    
    async def _save_to_mongodb(
        self,
        researcher_key: str,
        identifiers: ResearcherIdentifiers,
        profile_urls: ProfileURLs,
        platforms: Dict,
        publications: List[NormalizedPublication]
    ) -> Dict[str, Any]:
        """Save researcher and publications to MongoDB"""
        try:
            db = get_database()
            
            # Save or update researcher
            researcher_doc = {
                "researcher_key": researcher_key,
                "identifiers": identifiers.dict(),
                "profile_urls": profile_urls.dict(),
                "platforms": platforms,
                "last_synced_at": datetime.utcnow(),
                "sync_status": "success" if any(p["status"] == "success" for p in platforms.values()) else "failed",
                "updated_at": datetime.utcnow()
            }
            
            await db.researchers.update_one(
                {"researcher_key": researcher_key},
                {"$set": researcher_doc},
                upsert=True
            )
            
            # Save publications
            publications_saved = 0
            for pub in publications:
                try:
                    # Create unique source_record_id based on platform
                    source_record_id = self._create_source_record_id(pub)
                    
                    pub_doc = {
                        "researcher_key": researcher_key,
                        "platform": pub.source,
                        "source_record_id": source_record_id,
                        "title": pub.paper_name,
                        "authors": pub.author_name,
                        "publication_year": pub.year,
                        "publication_date": pub.date,
                        "work_type": pub.work_type,
                        "doi": pub.doi,
                        "url": pub.url,
                        "citation_count": pub.citation_count,
                        "issn": pub.issn,
                        "eissn": pub.eissn,
                        "isbn": pub.isbn,
                        "volume": pub.volume,
                        "issue": pub.issue,
                        "pages": pub.pages,
                        "publisher": pub.publisher,
                        "publication_name": pub.publication_name,
                        "scopus_id": pub.scopus_id,
                        "wos_id": pub.wos_id,
                        "platform_data": {},
                        "raw_data": pub.dict(),
                        "updated_at": datetime.utcnow()
                    }
                    
                    # Use upsert to avoid duplicates
                    await db.publications.update_one(
                        {
                            "researcher_key": researcher_key,
                            "platform": pub.source,
                            "source_record_id": source_record_id
                        },
                        {"$set": pub_doc},
                        upsert=True
                    )
                    
                    publications_saved += 1
                
                except Exception as e:
                    print(f"Error saving publication: {e}")
                    continue
            
            # Save sync log
            sync_log = {
                "researcher_key": researcher_key,
                "synced_at": datetime.utcnow(),
                "platforms": platforms,
                "total_publications": len(publications),
                "publications_saved": publications_saved
            }
            
            await db.sync_logs.insert_one(sync_log)
            
            return {
                "saved": True,
                "researcher_key": researcher_key,
                "publications_saved": publications_saved,
                "error": None
            }
        
        except Exception as e:
            return {
                "saved": False,
                "researcher_key": researcher_key,
                "publications_saved": 0,
                "error": str(e)
            }
    
    def _create_source_record_id(self, pub: NormalizedPublication) -> str:
        """Create a stable source record ID for deduplication"""
        # Priority: DOI > platform-specific ID > title+year
        if pub.doi:
            return f"doi:{pub.doi}"
        
        if pub.source == "ORCID":
            # ORCID doesn't provide a stable work ID in our current implementation
            # Use DOI or title+year
            if pub.doi:
                return f"doi:{pub.doi}"
            return f"orcid:{pub.paper_name}:{pub.year}"
        
        if pub.source == "Scopus" and pub.scopus_id:
            return f"scopus:{pub.scopus_id}"
        
        if pub.source == "Web of Science" and pub.wos_id:
            return f"wos:{pub.wos_id}"
        
        if pub.source == "Google Scholar":
            # Google Scholar doesn't provide stable IDs
            # Use title+year as fallback
            return f"gscholar:{pub.paper_name}:{pub.year}"
        
        # Final fallback: title+year
        return f"{pub.source}:{pub.paper_name}:{pub.year}"
