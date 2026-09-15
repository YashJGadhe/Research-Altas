"""
ResearchAtlas - User Model

Defines the structure and validation for user documents in MongoDB.
"""

from datetime import datetime, timezone
from typing import Optional
from bson import ObjectId


class UserModel:
    """
    User model representing an authenticated user in the system.
    """

    COLLECTION_NAME = "users"

    @staticmethod
    def create_user_doc(
        full_name: str,
        email: str,
        password_hash: str,
        role: str,
        department: str,
        orcid_id: str = "",
        scopus_id: str = "",
        wos_id: str = "",
    ) -> dict:
        """
        Create a new user document for insertion.
        """
        now = datetime.now(timezone.utc)
        return {
            "full_name": full_name,
            "email": email,
            "password_hash": password_hash,
            "role": role,
            "department": department,
            "orcid_id": orcid_id or "",
            "scopus_id": scopus_id or "",
            "wos_id": wos_id or "",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        }

    @staticmethod
    def to_response(user_doc: dict) -> dict:
        """
        Convert a user document to an API response.
        Removes sensitive fields like password_hash.
        """
        if user_doc is None:
            return None

        # Safely get datetime fields
        created_at = user_doc.get("created_at")
        updated_at = user_doc.get("updated_at")
        
        # Convert datetime to ISO format string
        if isinstance(created_at, datetime):
            created_at_str = created_at.isoformat()
        elif created_at:
            created_at_str = str(created_at)
        else:
            created_at_str = ""
            
        if isinstance(updated_at, datetime):
            updated_at_str = updated_at.isoformat()
        elif updated_at:
            updated_at_str = str(updated_at)
        else:
            updated_at_str = ""

        # Safely get _id
        user_id = user_doc.get("_id")
        if user_id:
            user_id_str = str(user_id)
        else:
            user_id_str = ""

        response = {
            "id": user_id_str,
            "full_name": user_doc.get("full_name", ""),
            "email": user_doc.get("email", ""),
            "role": user_doc.get("role", ""),
            "department": user_doc.get("department", ""),
            "orcid_id": user_doc.get("orcid_id", ""),
            "scopus_id": user_doc.get("scopus_id", ""),
            "wos_id": user_doc.get("wos_id", ""),
            "is_active": user_doc.get("is_active", True),
            "created_at": created_at_str,
            "updated_at": updated_at_str,
        }
        return response

    @staticmethod
    def to_list_response(users: list) -> list:
        """Convert a list of user documents to API response format."""
        return [UserModel.to_response(user) for user in users if user is not None]
