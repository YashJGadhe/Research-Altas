"""
ResearchAtlas - User Model

Defines the structure and validation for user documents in MongoDB.
This is the core authentication model that all future features reference.

The user document serves as the authentication anchor.
Future collections (faculty_profiles, publications, notifications, etc.)
will reference users by their _id (user_id).
"""

from datetime import datetime, timezone
from typing import Optional
from bson import ObjectId


class UserModel:
    """
    User model representing an authenticated user in the system.

    Fields:
        _id: ObjectId - Unique identifier (MongoDB primary key)
        full_name: str - User's full name
        email: str - Normalized email (lowercase, stripped)
        password_hash: str - Bcrypt hashed password (NEVER exposed in API)
        role: str - User role (admin, faculty, student)
        department: str - User's department
        orcid_id: str - ORCID researcher identifier
        scopus_id: str - Scopus author identifier
        wos_id: str - Web of Science researcher identifier
        is_active: bool - Whether the account is active
        created_at: datetime - Account creation timestamp
        updated_at: datetime - Last update timestamp

    Design Notes:
        - This model is intentionally minimal for authentication.
        - Faculty research data will be stored in separate collections
          linked by user_id (the _id field as string).
        - This separation allows the user model to remain stable
          while research features evolve independently.
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

        Args:
            full_name: User's full name
            email: Normalized email address
            password_hash: Hashed password
            role: User role
            department: User department
            orcid_id: ORCID researcher identifier (optional)
            scopus_id: Scopus author identifier (optional)
            wos_id: Web of Science researcher identifier (optional)

        Returns:
            Complete user document dictionary
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

        Args:
            user_doc: Raw MongoDB document

        Returns:
            Safe user dictionary for API responses
        """
        if user_doc is None:
            return None

        # Safely get datetime fields
        created_at = user_doc.get("created_at")
        updated_at = user_doc.get("updated_at")
        
        # Convert datetime to ISO format string
        if isinstance(created_at, datetime):
            created_at_str = created_at.isoformat()
        else:
            created_at_str = str(created_at) if created_at else ""
            
        if isinstance(updated_at, datetime):
            updated_at_str = updated_at.isoformat()
        else:
            updated_at_str = str(updated_at) if updated_at else ""

        response = {
            "id": str(user_doc["_id"]),
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
        return [UserModel.to_response(user) for user in users]
