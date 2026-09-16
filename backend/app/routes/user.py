"""
ResearchAtlas - User Management Routes

Admin-only API endpoints for managing all users.
"""

from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas.user import UserUpdateRequest
from app.services.user_service import UserService
from app.core.dependencies import require_admin

router = APIRouter(prefix="/api/users", tags=["User Management"])

# Service instance
user_service = UserService()


@router.get("/")
async def get_all_users(current_user: dict = Depends(require_admin)):
    """
    Get all users in the system.

    Admin only. Returns list of all users with their roles and status.
    """
    users = await user_service.get_all_users()
    return {"users": users, "total": len(users)}


@router.get("/{user_id}")
async def get_user(user_id: str, current_user: dict = Depends(require_admin)):
    """
    Get a specific user by ID.

    Admin only. Returns user details.
    """
    user = await user_service.get_user_by_id_response(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.put("/{user_id}")
async def update_user(
    user_id: str,
    request: UserUpdateRequest,
    current_user: dict = Depends(require_admin),
):
    """
    Update a user's information.

    Admin only. Can update name, role, department, and active status.
    Prevents admin from deactivating themselves.
    """
    # Prevent admin from deactivating themselves
    if user_id == str(current_user.get("id", current_user.get("_id", ""))):
        if request.is_active is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot deactivate your own account",
            )

    update_data = request.model_dump(exclude_none=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    user = await user_service.update_user(user_id, update_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: str, current_user: dict = Depends(require_admin)):
    """
    Delete a user from the system.

    Admin only. Permanently removes the user account.
    Prevents admin from deleting themselves.
    """
    # Prevent admin from deleting themselves
    current_user_id = str(current_user.get("id", current_user.get("_id", "")))
    if user_id == current_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot delete your own account",
        )

    deleted = await user_service.delete_user(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return {"message": "User deleted successfully", "success": True}
