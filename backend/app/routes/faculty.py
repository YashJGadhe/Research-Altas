"""
ResearchAtlas - Faculty Management Routes

Admin-only API endpoints for managing faculty members.
Future prompts will extend these routes with research profile endpoints.
"""

from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas.user import FacultyCreateRequest, FacultyUpdateRequest, FacultyStatusUpdate
from app.services.faculty_service import FacultyService
from app.core.dependencies import require_admin

router = APIRouter(prefix="/api/faculty", tags=["Faculty Management"])

# Service instance
faculty_service = FacultyService()


@router.get("/")
async def get_all_faculty(current_user: dict = Depends(require_admin)):
    """
    Get all faculty members.

    Admin only. Returns list of all faculty with their details.
    """
    faculty = await faculty_service.get_all_faculty()
    return {"faculty": faculty, "total": len(faculty)}


@router.get("/{faculty_id}")
async def get_faculty(faculty_id: str, current_user: dict = Depends(require_admin)):
    """
    Get a specific faculty member by ID.

    Admin only. Returns faculty details.
    """
    faculty = await faculty_service.get_faculty_by_id(faculty_id)
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty member not found",
        )
    return faculty


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_faculty(
    request: FacultyCreateRequest,
    current_user: dict = Depends(require_admin),
):
    """
    Create a new faculty member account.

    Admin only. Creates a user with faculty role.
    """
    try:
        faculty = await faculty_service.create_faculty(
            full_name=request.full_name,
            email=request.email,
            password=request.password,
            department=request.department,
            orcid_id=request.orcid_id,
            scopus_id=request.scopus_id,
            wos_id=request.wos_id,
        )
        return faculty
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating faculty member.",
        )


@router.put("/{faculty_id}")
async def update_faculty(
    faculty_id: str,
    request: FacultyUpdateRequest,
    current_user: dict = Depends(require_admin),
):
    """
    Update a faculty member's information.

    Admin only. Can update name, department, and active status.
    """
    update_data = request.model_dump(exclude_none=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    faculty = await faculty_service.update_faculty(faculty_id, update_data)
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty member not found",
        )
    return faculty


@router.patch("/{faculty_id}/status")
async def toggle_faculty_status(
    faculty_id: str,
    request: FacultyStatusUpdate,
    current_user: dict = Depends(require_admin),
):
    """
    Activate or deactivate a faculty member.

    Admin only. Deactivated faculty cannot login.
    """
    faculty = await faculty_service.toggle_faculty_status(faculty_id, request.is_active)
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty member not found",
        )
    return faculty


@router.delete("/{faculty_id}", status_code=status.HTTP_200_OK)
async def delete_faculty(faculty_id: str, current_user: dict = Depends(require_admin)):
    """
    Delete a faculty member.

    Admin only. Permanently removes the faculty account.
    """
    deleted = await faculty_service.delete_faculty(faculty_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty member not found",
        )
    return {"message": "Faculty member deleted successfully", "success": True}
