"""
ResearchAtlas - User Service

Business logic for user management operations.
"""

from datetime import datetime, timezone
from typing import Optional, List, Dict
from bson import ObjectId

from app.database.database import get_collection
from app.models.user import UserModel


class UserService:
    """Service for user management operations."""

    def __init__(self):
        self.collection_name = "users"

    def _get_collection(self):
        return get_collection(self.collection_name)

    async def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """
        Get a user by ID. Returns response format (for dependency use).
        """
        collection = self._get_collection()
        try:
            user = await collection.find_one({"_id": ObjectId(user_id)})
            if user:
                # Convert to response format
                return UserModel.to_response(user)
            return None
        except Exception as e:
            print(f"[ERROR] get_user_by_id failed: {str(e)}")
            return None

    async def get_all_users(self) -> List[Dict]:
        """
        Get all users.
        """
        collection = self._get_collection()
        cursor = collection.find({}).sort("created_at", -1)
        users = await cursor.to_list(length=None)
        return UserModel.to_list_response(users)

    async def get_user_by_id_response(self, user_id: str) -> Optional[Dict]:
        """
        Get a user by ID in response format.
        """
        return await self.get_user_by_id(user_id)

    async def update_user(self, user_id: str, update_data: Dict) -> Optional[Dict]:
        """
        Update a user's information.
        """
        collection = self._get_collection()

        # Remove None values
        update_data = {k: v for k, v in update_data.items() if v is not None}

        if not update_
            return await self.get_user_by_id_response(user_id)

        # Add updated_at timestamp
        update_data["updated_at"] = datetime.now(timezone.utc)

        try:
            result = await collection.find_one_and_update(
                {"_id": ObjectId(user_id)},
                {"$set": update_data},
                return_document=True,
            )
        except Exception as e:
            print(f"[ERROR] update_user failed: {str(e)}")
            return None

        if result:
            return UserModel.to_response(result)
        return None

    async def delete_user(self, user_id: str) -> bool:
        """
        Delete a user.
        """
        collection = self._get_collection()
        try:
            result = await collection.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"[ERROR] delete_user failed: {str(e)}")
            return False

    async def get_users_by_role(self, role: str) -> List[Dict]:
        """
        Get all users with a specific role.
        """
        collection = self._get_collection()
        cursor = collection.find({"role": role}).sort("created_at", -1)
        users = await cursor.to_list(length=None)
        return UserModel.to_list_response(users)

    async def get_user_by_email(self, email: str) -> Optional[Dict]:
        """
        Get a user by email.
        """
        collection = self._get_collection()
        user = await collection.find_one({"email": email})
        if user:
            return UserModel.to_response(user)
        return None
