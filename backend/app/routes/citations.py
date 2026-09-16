"""
ResearchAtlas - Citation Routes

API routes for citation management operations.
"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import require_admin
from app.schemas.citation import (
    CitationRecordListResponse,
    CitationRecordResponse,
    CitationUpdateRequest,
    CitationHistoryListResponse,
    FetchResultResponse
)
from app.services.citation_service import CitationService
from app.services.orcid_service import OrcidService

router = APIRouter(prefix="/api/citations", tags=["Citations"])

# Service instances
citation_service = CitationService()
orcid_service = OrcidService()


@router.get("/", response_model=CitationRecordListResponse)
async def get_all_citations(current_user: dict = Depends(require_admin)):
    """
    Get all citation records.
    
    Admin only endpoint.
    """
    records = await citation_service.get_all_records()
    return CitationRecordListResponse(records=records, total=len(records))


@router.get("/{record_id}", response_model=CitationRecordResponse)
async def get_citation_by_id(
    record_id: str,
    current_user: dict = Depends(require_admin)
):
    """
    Get a specific citation record by ID.
    
    Admin only endpoint.
    """
    record = await citation_service.get_record_by_id(record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Citation record not found"
        )
    return record


@router.get("/faculty/{faculty_id}", response_model=CitationRecordResponse)
async def get_citation_by_faculty_id(
    faculty_id: str,
    current_user: dict = Depends(require_admin)
):
    """
    Get citation record by faculty ID.
    
    Admin only endpoint.
    """
    record = await citation_service.get_record_by_faculty_id(faculty_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Citation record not found for this faculty"
        )
    return record


@router.put("/{record_id}", response_model=CitationRecordResponse)
async def update_citation(
    record_id: str,
    update_data: CitationUpdateRequest,
    current_user: dict = Depends(require_admin)
):
    """
    Manually update a citation record.
    
    Admin only endpoint. Creates history snapshot before updating.
    """
    # Convert Pydantic model to dict, excluding None values
    update_dict = update_data.model_dump(exclude_none=True)
    
    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update"
        )
    
    updated_record = await citation_service.update_record(
        record_id=record_id,
        update_data=update_dict,
        updated_by=current_user["email"],
        change_source="manual",
        source_platform="MANUAL"
    )
    
    if not updated_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Citation record not found"
        )
    
    return updated_record


@router.get("/{record_id}/history", response_model=CitationHistoryListResponse)
async def get_citation_history(
    record_id: str,
    current_user: dict = Depends(require_admin)
):
    """
    Get citation history for a specific record.
    
    Admin only endpoint.
    """
    # First get the record to get faculty_id
    record = await citation_service.get_record_by_id(record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Citation record not found"
        )
    
    history = await citation_service.get_history_by_faculty_id(record["faculty_id"])
    return CitationHistoryListResponse(history=history, total=len(history))


@router.post("/{record_id}/fetch/orcid", response_model=FetchResultResponse)
async def fetch_orcid_data(
    record_id: str,
    current_user: dict = Depends(require_admin)
):
    """
    Fetch data from ORCID for a specific faculty member.
    
    Admin only endpoint.
    """
    # Get the citation record
    record = await citation_service.get_record_by_id(record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Citation record not found"
        )
    
    # Check if ORCID ID is configured
    orcid_id = record.get("orcid", {}).get("id", "")
    if not orcid_id:
        return FetchResultResponse(
            success=False,
            message="ORCID ID not configured for this faculty member",
            faculty_id=record["faculty_id"],
            source="ORCID",
            records_found=0,
            records_updated=0,
            history_created=0
        )
    
    # Validate ORCID ID format
    if not orcid_service.validate_orcid_id(orcid_id):
        return FetchResultResponse(
            success=False,
            message=f"Invalid ORCID ID format: {orcid_id}",
            faculty_id=record["faculty_id"],
            source="ORCID",
            records_found=0,
            records_updated=0,
            history_created=0
        )
    
    # Start fetch log
    started_at = datetime.utcnow()
    
    try:
        # Fetch data from ORCID
        orcid_data = await orcid_service.get_researcher_profile(orcid_id)
        
        if not orcid_data:
            # Log failed fetch
            await citation_service.create_fetch_log(
                faculty_id=record["faculty_id"],
                faculty_name=record["faculty_name"],
                source="ORCID",
                status="failed",
                started_at=started_at,
                completed_at=datetime.utcnow(),
                error_message="Failed to fetch data from ORCID API",
                triggered_by=current_user["email"]
            )
            
            return FetchResultResponse(
                success=False,
                message="Failed to fetch data from ORCID API",
                faculty_id=record["faculty_id"],
                source="ORCID",
                records_found=0,
                records_updated=0,
                history_created=0
            )
        
        # Update ORCID information in citation record
        update_data = {
            "orcid": {
                "id": orcid_data["orcid_id"],
                "url": orcid_data["orcid_url"]
            },
            "source_status": {
                **record.get("source_status", {}),
                "orcid": "success"
            }
        }
        
        # Update the record
        updated_record = await citation_service.update_record(
            record_id=record_id,
            update_data=update_data,
            updated_by=current_user["email"],
            change_source="api",
            source_platform="ORCID"
        )
        
        # Log successful fetch
        await citation_service.create_fetch_log(
            faculty_id=record["faculty_id"],
            faculty_name=record["faculty_name"],
            source="ORCID",
            status="success",
            started_at=started_at,
            completed_at=datetime.utcnow(),
            records_found=orcid_data["works_count"],
            records_updated=1,
            triggered_by=current_user["email"]
        )
        
        return FetchResultResponse(
            success=True,
            message="ORCID data fetched successfully",
            faculty_id=record["faculty_id"],
            source="ORCID",
            records_found=orcid_data["works_count"],
            records_updated=1,
            history_created=0,  # ORCID doesn't provide citation metrics
            data=orcid_data
        )
        
    except Exception as e:
        # Log error
        await citation_service.create_fetch_log(
            faculty_id=record["faculty_id"],
            faculty_name=record["faculty_name"],
            source="ORCID",
            status="error",
            started_at=started_at,
            completed_at=datetime.utcnow(),
            error_message=str(e),
            triggered_by=current_user["email"]
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching ORCID data: {str(e)}"
        )


@router.get("/logs/fetch", response_model=list)
async def get_fetch_logs(
    faculty_id: Optional[str] = None,
    limit: int = 50,
    current_user: dict = Depends(require_admin)
):
    """
    Get fetch logs for auditing.
    
    Admin only endpoint.
    """
    logs = await citation_service.get_fetch_logs(faculty_id=faculty_id, limit=limit)
    return logs
