"""
ResearchAtlas - Dependencies Module

Reusable FastAPI dependencies for authentication and authorization.
"""

from typing import List, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security import verify_token
from app.services.user_service import UserService

# Bearer token scheme
security = HTTPBearer()

# Service instances
user_service = UserService()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Dependency: Extract and validate the current user from JWT token.
    """
    try:
        token = credentials.credentials
        payload = verify_token(token)

        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = await user_service.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.get("is_active", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated",
            )

        return user
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] get_current_user failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_roles(allowed_roles: List[str]):
    """
    Factory function: Create a dependency that checks if user has one of the allowed roles.
    """
    async def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user.get("role") not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return role_checker


# Pre-built role dependencies for convenience
require_admin = require_roles(["admin"])
require_faculty = require_roles(["faculty"])
require_student = require_roles(["student"])
require_admin_or_faculty = require_roles(["admin", "faculty"])
require_admin_or_student = require_roles(["admin", "student"])
