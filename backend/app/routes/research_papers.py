"""
ResearchAtlas - Research Papers Routes

API routes for managing research publications.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional, List, Dict, Any

from app.core.dependencies import require_admin
from app.services.research_paper_service import ResearchPaperService
from app.services.faculty_service import FacultyService

router = APIRouter(prefix="/api/research-papers", tags=["Research Papers"])

# Service instances
research_paper_service = ResearchPaperService()
faculty_service = FacultyService()


@router.post("/faculty/{faculty_id}/fetch/orcid")
async def fetch_orcid_publications(
    faculty_id: str,
    current_user: dict = Depends(require_admin)
):
    """
    Fetch publications from ORCID for a specific faculty member.
    
    Admin only endpoint.
    """
    # Get faculty member
    faculty = await faculty_service.get_faculty_by_id(faculty_id)
    
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty member not found"
        )
    
    # Check if ORCID ID is configured
    orcid_id = faculty.get("orcid_id", "")
    if not orcid_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ORCID ID not configured for this faculty member"
        )
    
    # Fetch publications
    result = await research_paper_service.fetch_orcid_publications(
        faculty_id=faculty_id,
        faculty_name=faculty.get("full_name", ""),
        orcid_id=orcid_id
    )
    
    return result


@router.get("/faculty/{faculty_id}")
async def get_faculty_publications(
    faculty_id: str,
    source: Optional[str] = Query(None, description="Filter by source (ORCID, Scopus, etc.)"),
    work_type: Optional[str] = Query(None, description="Filter by work type"),
    year: Optional[int] = Query(None, description="Filter by year"),
    search: Optional[str] = Query(None, description="Search query"),
    sort_by: str = Query("year_desc", description="Sort order (year_desc, year_asc)"),
    current_user: dict = Depends(require_admin)
):
    """
    Get publications for a specific faculty member with optional filters.
    
    Admin only endpoint.
    """
    # Get faculty member
    faculty = await faculty_service.get_faculty_by_id(faculty_id)
    
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty member not found"
        )
    
    # Get publications
    publications = await research_paper_service.get_faculty_publications(
        faculty_id=faculty_id,
        source=source,
        work_type=work_type,
        year=year,
        search=search,
        sort_by=sort_by
    )
    
    return {
        "faculty_id": faculty_id,
        "faculty_name": faculty.get("full_name", ""),
        "publications": publications,
        "total": len(publications)
    }


@router.get("/faculty/{faculty_id}/statistics")
async def get_faculty_publication_statistics(
    faculty_id: str,
    current_user: dict = Depends(require_admin)
):
    """
    Get publication statistics for a specific faculty member.
    
    Admin only endpoint.
    """
    # Get faculty member
    faculty = await faculty_service.get_faculty_by_id(faculty_id)
    
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty member not found"
        )
    
    # Get statistics
    statistics = await research_paper_service.get_publication_statistics(faculty_id)
    
    return {
        "faculty_id": faculty_id,
        "faculty_name": faculty.get("full_name", ""),
        "statistics": statistics
    }


@router.get("/faculty/{faculty_id}/work-types")
async def get_faculty_work_types(
    faculty_id: str,
    current_user: dict = Depends(require_admin)
):
    """
    Get available work types for a faculty member's publications.
    
    Admin only endpoint.
    """
    # Get faculty member
    faculty = await faculty_service.get_faculty_by_id(faculty_id)
    
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty member not found"
        )
    
    # Get publications
    publications = await research_paper_service.get_faculty_publications(faculty_id=faculty_id)
    
    # Extract unique work types
    work_types = set()
    for pub in publications:
        work_type = pub.get("work_type")
        if work_type:
            work_types.add(work_type)
    
    return {
        "faculty_id": faculty_id,
        "work_types": sorted(list(work_types))
    }


@router.get("/faculty/{faculty_id}/years")
async def get_faculty_publication_years(
    faculty_id: str,
    current_user: dict = Depends(require_admin)
):
    """
    Get available publication years for a faculty member.
    
    Admin only endpoint.
    """
    # Get faculty member
    faculty = await faculty_service.get_faculty_by_id(faculty_id)
    
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty member not found"
        )
    
    # Get publications
    publications = await research_paper_service.get_faculty_publications(faculty_id=faculty_id)
    
    # Extract unique years
    years = set()
    for pub in publications:
        year = pub.get("year")
        if year:
            years.add(year)
    
    return {
        "faculty_id": faculty_id,
        "years": sorted(list(years), reverse=True)
    }
