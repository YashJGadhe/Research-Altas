"""
Researcher API Endpoints

Provides endpoints for searching researchers and fetching publications.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from pydantic import BaseModel

from app.services.researcher_service import UnifiedResearcherService


router = APIRouter(prefix="/api/researchers", tags=["Researchers"])


class ResearcherSearchRequest(BaseModel):
    orcid: Optional[str] = None
    scopus_author_id: Optional[str] = None
    google_scholar_author_id: Optional[str] = None
    wos_researcher_id: Optional[str] = None


@router.post("/search")
async def search_researcher(request: ResearcherSearchRequest):
    """
    Search for a researcher across multiple platforms.
    
    At least one identifier must be provided.
    """
    # Validate that at least one identifier is provided
    if not any([
        request.orcid,
        request.scopus_author_id,
        request.google_scholar_author_id,
        request.wos_researcher_id
    ]):
        raise HTTPException(
            status_code=400,
            detail="At least one researcher identifier must be provided"
        )
    
    service = UnifiedResearcherService()
    
    try:
        result = await service.search_researcher(
            orcid=request.orcid,
            scopus_author_id=request.scopus_author_id,
            google_scholar_author_id=request.google_scholar_author_id,
            wos_researcher_id=request.wos_researcher_id
        )
        
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching researcher: {str(e)}"
        )


@router.get("/search")
async def search_researcher_get(
    orcid: Optional[str] = Query(None),
    scopus_author_id: Optional[str] = Query(None),
    google_scholar_author_id: Optional[str] = Query(None),
    wos_researcher_id: Optional[str] = Query(None)
):
    """
    Search for a researcher using GET method.
    
    At least one identifier must be provided as query parameter.
    """
    # Validate that at least one identifier is provided
    if not any([orcid, scopus_author_id, google_scholar_author_id, wos_researcher_id]):
        raise HTTPException(
            status_code=400,
            detail="At least one researcher identifier must be provided"
        )
    
    service = UnifiedResearcherService()
    
    try:
        result = await service.search_researcher(
            orcid=orcid,
            scopus_author_id=scopus_author_id,
            google_scholar_author_id=google_scholar_author_id,
            wos_researcher_id=wos_researcher_id
        )
        
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching researcher: {str(e)}"
        )
