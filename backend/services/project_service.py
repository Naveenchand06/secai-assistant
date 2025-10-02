from database import user_collection, user_helper
from models.user import Project
from bson.objectid import ObjectId
from datetime import datetime
import uuid
from typing import List

async def create_project(user_email: str, project_name: str, project_description: str = None) -> dict:
    """Create a new project for a user"""
    # Generate a unique project ID
    project_id = str(uuid.uuid4())
    
    # Create project object
    project = Project(
        project_id=project_id,
        project_name=project_name,
        project_description=project_description,
        created_at=datetime.now()
    )
    
    # Add project to user's project list
    result = await user_collection.update_one(
        {"email": user_email},
        {"$push": {"projects": project.model_dump()}}
    )
    
    if result.modified_count == 1:
        # Retrieve updated user
        user = await user_collection.find_one({"email": user_email})
        if user:
            return project.model_dump()
    
    return None

async def get_user_projects(user_email: str) -> List[dict]:
    """Retrieve all projects for a specific user"""
    user = await user_collection.find_one({"email": user_email})
    if user:
        return user.get("projects", [])
    return []
