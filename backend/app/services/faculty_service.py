"""
ResearchAtlas - Faculty Service

Business logic for faculty management operations.
Admin can manage faculty members.
Faculty records are linked to user accounts.

Future prompts will extend this service with:
- Research profile management
- Publication tracking
- Platform ID management
- Research metrics
"""

from datetime import datetime, timezone
from typing import Optional, List, Dict
from bson import ObjectId

from app.database.database import get_collection
from app.core.security import hash_password
from app.models.user import UserModel


class FacultyService:
    """Service for faculty management operations."""

    def __init__(self):
        self.users_collection_name = "users"

    def _get_collection(self):
        return get_collection(self.users_collection_name)

    async def get_all_faculty(self) -> List[Dict]:
        """
        Get all faculty members.

        Returns:
            List of faculty user response dictionaries
        """
        collection = self._get_collection()
        cursor = collection.find({"role": "faculty"}).sort("created_at", -1)
        users = await cursor.to_list(length=None)
        return UserModel.to_list_response(users)

    async def get_faculty_by_id(self, faculty_id: str) -> Optional[Dict]:
        """
        Get a faculty member by their user ID.

        Args:
            faculty_id: Faculty user's ObjectId string

        Returns:
            Faculty response dictionary or None
        """
        collection = self._get_collection()
        try:
            user = await collection.find_one({
                "_id": ObjectId(faculty_id),
                "role": "faculty",
            })
        except Exception:
            return None

        if user:
            return UserModel.to_response(user)
        return None

    async def create_faculty(
        self,
        full_name: str,
        email: str,
        password: str,
        department: str,
        orcid_id: str,
        scopus_id: str,
        wos_id: str,
    ) -> Dict:
        """
        Create a new faculty member (admin operation).

        Args:
            full_name: Faculty member's full name
            email: Faculty member's email
            password: Plain-text password (will be hashed)
            department: Department
            orcid_id: ORCID researcher identifier
            scopus_id: Scopus author identifier
            wos_id: Web of Science researcher identifier

        Returns:
            Created faculty response dictionary

        Raises:
            ValueError: If email already exists
        """
        collection = self._get_collection()

        # Check for duplicate email
        existing = await collection.find_one({"email": email.lower().strip()})
        if existing:
            raise ValueError("An account with this email already exists")

        # Check for duplicate ORCID ID
        existing_orcid = await collection.find_one({"orcid_id": orcid_id})
        if existing_orcid:
            raise ValueError("An account with this ORCID ID already exists")

        # Check for duplicate Scopus ID
        existing_scopus = await collection.find_one({"scopus_id": scopus_id})
        if existing_scopus:
            raise ValueError("An account with this Scopus ID already exists")

        # Check for duplicate WOS ID
        existing_wos = await collection.find_one({"wos_id": wos_id})
        if existing_wos:
            raise ValueError("An account with this Web of Science ID already exists")

        # Create user document
        now = datetime.now(timezone.utc)
        user_doc = {
            "full_name": full_name.strip(),
            "email": email.lower().strip(),
            "password_hash": hash_password(password),
            "role": "faculty",
            "department": department,
            "orcid_id": orcid_id,
            "scopus_id": scopus_id,
            "wos_id": wos_id,
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        }

        result = await collection.insert_one(user_doc)
        user_doc["_id"] = result.inserted_id

        return UserModel.to_response(user_doc)

    async def update_faculty(self, faculty_id: str, update_data: Dict) -> Optional[Dict]:
        """
        Update a faculty member's information.

        Args:
            faculty_id: Faculty user's ObjectId string
            update_ Fields to update

        Returns:
            Updated faculty response or None
        """
        collection = self._get_collection()

        # Remove None values
        update_data = {k: v for k, v in update_data.items() if v is not None}

        if not update_data:
            return await self.get_faculty_by_id(faculty_id)

        # Ensure we only update faculty
        update_data["updated_at"] = datetime.now(timezone.utc)

        try:
            result = await collection.find_one_and_update(
                {"_id": ObjectId(faculty_id), "role": "faculty"},
                {"$set": update_data},
                return_document=True,
            )
        except Exception:
            return None

        if result:
            return UserModel.to_response(result)
        return None

    async def toggle_faculty_status(self, faculty_id: str, is_active: bool) -> Optional[Dict]:
        """
        Activate or deactivate a faculty member.

        Args:
            faculty_id: Faculty user's ObjectId string
            is_active: New active status

        Returns:
            Updated faculty response or None
        """
        collection = self._get_collection()

        try:
            result = await collection.find_one_and_update(
                {"_id": ObjectId(faculty_id), "role": "faculty"},
                {
                    "$set": {
                        "is_active": is_active,
                        "updated_at": datetime.now(timezone.utc),
                    }
                },
                return_document=True,
            )
        except Exception:
            return None

        if result:
            return UserModel.to_response(result)
        return None

    async def delete_faculty(self, faculty_id: str) -> bool:
        """
        Delete a faculty member.

        Args:
            faculty_id: Faculty user's ObjectId string

        Returns:
            True if deleted, False if not found
        """
        collection = self._get_collection()
        try:
            result = await collection.delete_one({
                "_id": ObjectId(faculty_id),
                "role": "faculty",
            })
            return result.deleted_count > 0
        except Exception:
            return False
