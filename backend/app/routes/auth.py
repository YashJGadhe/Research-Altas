"""
ResearchAtlas - Authentication Routes

API endpoints for registration, login, and current user retrieval.
"""

import traceback
from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, MessageResponse
from app.services.auth_service import AuthService
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Service instance
auth_service = AuthService()


@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    """
    Register a new user account.

    Validates all fields, checks for duplicates, hashes password,
    and creates the user account.

    Returns 409 if email already exists.
    """
    # Validate password confirmation
    if request.password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )

    try:
        await auth_service.register_user(
            full_name=request.full_name,
            email=request.email,
            password=request.password,
            role=request.role,
            department=request.department,
            orcid_id=request.orcid_id,
            scopus_id=request.scopus_id,
            wos_id=request.wos_id,
        )
        return MessageResponse(
            message="Registration successful. You can now login.",
            success=True,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except Exception as e:
        print(f"[ERROR] Registration failed: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}",
        )


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    Authenticate user and return JWT access token.

    Verifies credentials and account status.
    Returns token and user information on success.
    """
    try:
        result = await auth_service.authenticate_user(
            email=request.email,
            password=request.password,
        )
        return result
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    except Exception as e:
        print(f"[ERROR] Login failed: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}",
        )


@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get the currently authenticated user's information.

    Requires valid JWT token.
    Returns user data without sensitive fields.
    """
    return current_user
