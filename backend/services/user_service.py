from database import user_collection, user_helper
from models.user import User
from bson.objectid import ObjectId
from datetime import datetime
from typing import List

async def add_user(user_data: dict) -> dict:
    """Add a new user to the database"""
    user_data["created_at"] = datetime.now()
    user_data["updated_at"] = datetime.now()
    
    # Hash password if present
    if "password" in user_data:
        from services.auth_service import get_password_hash
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
    
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

async def retrieve_users() -> List[dict]:
    """Retrieve all users from the database"""
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users

async def retrieve_user(id: str) -> dict:
    """Retrieve a user by ID"""
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)
    return None

async def update_user(id: str, data: dict) -> dict:
    """Update a user by ID"""
    if len(data) < 1:
        return False
    
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        
        if updated_user:
            user = await user_collection.find_one({"_id": ObjectId(id)})
            return user_helper(user)
        
    return None

async def delete_user(id: str) -> bool:
    """Delete a user by ID"""
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False
