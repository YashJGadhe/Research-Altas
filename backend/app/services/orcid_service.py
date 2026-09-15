"""
ResearchAtlas - ORCID Service

Service for integrating with ORCID API to fetch researcher data.
"""

import httpx
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.core.config import settings


class OrcidService:
    """Service for ORCID API integration."""
    
    def __init__(self):
        self.base_url = "https://pub.orcid.org/v3.0"
        self.client_id = settings.ORCID_CLIENT_ID if hasattr(settings, 'ORCID_CLIENT_ID') else ""
        self.client_secret = settings.ORCID_CLIENT_SECRET if hasattr(settings, 'ORCID_CLIENT_SECRET') else ""
    
    async def get_researcher_profile(self, orcid_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch researcher profile from ORCID.
        
        Args:
            orcid_id: ORCID ID (e.g., "0000-0002-1825-0097")
        
        Returns:
            Dictionary with researcher profile data or None if not found
        """
        if not orcid_id:
            return None
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Fetch person data
                person_url = f"{self.base_url}/{orcid_id}/person"
                person_response = await client.get(
                    person_url,
                    headers={"Accept": "application/json"}
                )
                
                if person_response.status_code != 200:
                    print(f"[ORCID] Failed to fetch person data: {person_response.status_code}")
                    return None
                
                person_data = person_response.json()
                
                # Fetch works/publications
                works_url = f"{self.base_url}/{orcid_id}/works"
                works_response = await client.get(
                    works_url,
                    headers={"Accept": "application/json"}
                )
                
                works_data = None
                if works_response.status_code == 200:
                    works_data = works_response.json()
                
                # Parse and normalize data
                return self._normalize_orcid_data(orcid_id, person_data, works_data)
                
        except httpx.TimeoutException:
            print(f"[ORCID] Timeout fetching data for {orcid_id}")
            return None
        except Exception as e:
            print(f"[ORCID] Error fetching data for {orcid_id}: {str(e)}")
            return None
    
    def _normalize_orcid_data(
        self,
        orcid_id: str,
        person_data: Dict,
        works_data: Optional[Dict]
    ) -> Dict[str, Any]:
        """
        Normalize ORCID API response to our internal format.
        
        Note: ORCID does NOT provide citation metrics like h-index or i10-index.
        It only provides researcher identity, profile info, and works/publications.
        """
        normalized = {
            "orcid_id": orcid_id,
            "orcid_url": f"https://orcid.org/{orcid_id}",
            "name": self._extract_name(person_data),
            "biography": self._extract_biography(person_data),
            "affiliations": self._extract_affiliations(person_data),
            "works_count": 0,
            "works": []
        }
        
        # Extract works if available
        if works_data and "group" in works_data:
            works = []
            for group in works_data["group"]:
                work_summary = self._extract_work_summary(group)
                if work_summary:
                    works.append(work_summary)
            
            normalized["works_count"] = len(works)
            normalized["works"] = works
        
        return normalized
    
    def _extract_name(self, person_data: Dict) -> str:
        """Extract full name from ORCID person data."""
        try:
            name = person_data.get("name", {})
            given_name = name.get("given-name", {}).get("value", "")
            family_name = name.get("family-name", {}).get("value", "")
            
            if given_name and family_name:
                return f"{given_name} {family_name}"
            elif given_name:
                return given_name
            elif family_name:
                return family_name
            
            return ""
        except Exception:
            return ""
    
    def _extract_biography(self, person_data: Dict) -> str:
        """Extract biography from ORCID person data."""
        try:
            biography = person_data.get("biography", {})
            return biography.get("content", "")
        except Exception:
            return ""
    
    def _extract_affiliations(self, person_data: Dict) -> List[Dict]:
        """Extract affiliations from ORCID person data."""
        affiliations = []
        
        try:
            # Employment affiliations
            employments = person_data.get("employments", {}).get("affiliation-group", [])
            for emp in employments:
                summary = emp.get("summaries", [{}])[0].get("employment-summary", {})
                if summary:
                    affiliations.append({
                        "type": "employment",
                        "organization": summary.get("organization", {}).get("name", ""),
                        "role": summary.get("role-title", ""),
                        "start_year": self._extract_year(summary.get("start-date"))
                    })
            
            # Education affiliations
            educations = person_data.get("educations", {}).get("affiliation-group", [])
            for edu in educations:
                summary = edu.get("summaries", [{}])[0].get("education-summary", {})
                if summary:
                    affiliations.append({
                        "type": "education",
                        "organization": summary.get("organization", {}).get("name", ""),
                        "role": summary.get("role-title", ""),
                        "start_year": self._extract_year(summary.get("start-date"))
                    })
        
        except Exception as e:
            print(f"[ORCID] Error extracting affiliations: {str(e)}")
        
        return affiliations
    
    def _extract_year(self, date_obj: Optional[Dict]) -> Optional[int]:
        """Extract year from ORCID date object."""
        try:
            if date_obj and "year" in date_obj:
                return int(date_obj["year"].get("value"))
            return None
        except Exception:
            return None
    
    def _extract_work_summary(self, work_group: Dict) -> Optional[Dict]:
        """Extract work summary from ORCID work group."""
        try:
            summaries = work_group.get("work-summary", [])
            if not summaries:
                return None
            
            # Get the first work summary
            work = summaries[0]
            
            return {
                "title": work.get("title", {}).get("title", {}).get("value", ""),
                "type": work.get("type", ""),
                "publication_year": self._extract_year(work.get("publication-date")),
                "journal": work.get("journal-title", {}).get("value", ""),
                "doi": self._extract_doi(work.get("external-ids", {}))
            }
        except Exception:
            return None
    
    def _extract_doi(self, external_ids: Dict) -> Optional[str]:
        """Extract DOI from external identifiers."""
        try:
            ids = external_ids.get("external-id", [])
            for ext_id in ids:
                if ext_id.get("external-id-type") == "doi":
                    return ext_id.get("external-id-value")
            return None
        except Exception:
            return None
    
    def validate_orcid_id(self, orcid_id: str) -> bool:
        """
        Validate ORCID ID format.
        
        ORCID IDs follow the format: 0000-0000-0000-0000
        The last character can be a digit or 'X' (checksum).
        """
        if not orcid_id:
            return False
        
        # Remove any whitespace
        orcid_id = orcid_id.strip()
        
        # Check format with dashes
        import re
        pattern = r'^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$'
        
        return bool(re.match(pattern, orcid_id))
