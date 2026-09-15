"""
ResearchAtlas - Authentication Service

Business logic for authentication operations.
Handles registration, login, and user verification.
"""

from datetime import datetime, timezone
from typing import Optional, Dict
from bson import ObjectId

from app.database.database import get_collection
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import UserModel


class AuthService:
    """Service for authentication operations."""

    def __init__(self):
        self.users_collection_name = "users"

    def _get_collection(self):
        return get_collection(self.users_collection_name)

    async def register_user(
        self,
        full_name: str,
        email: str,
        password: str,
        role: str,
        department: str,
        orcid_id: str,
        scopus_id: str,
        wos_id: str,
    ) -> Dict:
        """
        Register a new user.
        """
        collection = self._get_collection()

        # Check for duplicate email
        existing_user = await collection.find_one({"email": email})
        if existing_user:
            raise ValueError("An account with this email already exists")

        # Check for duplicate ORCID ID (only if not empty)
        if orcid_id:
            existing_orcid = await collection.find_one({"orcid_id": orcid_id})
            if existing_orcid:
                raise ValueError("An account with this ORCID ID already exists")

        # Check for duplicate Scopus ID (only if not empty)
        if scopus_id:
            existing_scopus = await collection.find_one({"scopus_id": scopus_id})
            if existing_scopus:
                raise ValueError("An account with this Scopus ID already exists")

        # Check for duplicate WOS ID (only if not empty)
        if wos_id:
            existing_wos = await collection.find_one({"wos_id": wos_id})
            if existing_wos:
                raise ValueError("An account with this Web of Science ID already exists")

        # Hash password
        password_hash = hash_password(password)

        # Create user document
        user_doc = UserModel.create_user_doc(
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role=role,
            department=department,
            orcid_id=orcid_id,
            scopus_id=scopus_id,
            wos_id=wos_id,
        )

        # Insert into database
        result = await collection.insert_one(user_doc)
        user_doc["_id"] = result.inserted_id

        return UserModel.to_response(user_doc)

    async def authenticate_user(self, email: str, password: str) -> Dict:
        """
        Authenticate a user and generate JWT token.
        
        Returns:
            Dict with access_token, token_type, and user data
        """
        collection = self._get_collection()

        # Find user by email
        user = await collection.find_one({"email": email})
        if not user:
            raise ValueError("Invalid email or password")

        # Check if account is active
        if not user.get("is_active", False):
            raise PermissionError("Your account has been deactivated. Please contact an administrator.")

        # Verify password
        password_hash = user.get("password_hash")
        if not password_hash:
            raise ValueError("Invalid email or password")
            
        if not verify_password(password, password_hash):
            raise ValueError("Invalid email or password")

        # Generate JWT token
        token_data = {
            "sub": str(user["_id"]),
            "email": user["email"],
            "role": user["role"],
        }
        access_token = create_access_token(data=token_data)

        # Convert user to response format
        user_response = UserModel.to_response(user)

        # Return in the exact format expected by frontend
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_response,
        }

    async def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """
        Get a user by their ID.
        """
        collection = self._get_collection()

        try:
            user = await collection.find_one({"_id": ObjectId(user_id)})
        except Exception as e:
            print(f"[ERROR] get_user_by_id failed: {str(e)}")
            return None

        if user:
            return UserModel.to_response(user)
        return None
