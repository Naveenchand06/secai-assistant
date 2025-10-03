from database import user_collection, user_helper
from models.user import Project, APIKey
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import uuid
import secrets
from typing import List, Optional

async def create_project(user_email: str, project_name: str, project_description: str = None) -> dict:
    """Create a new project for a user"""
    # Generate a unique project ID
    project_id = str(uuid.uuid4())
    
    # Create project object
    project = Project(
        project_id=project_id,
        project_name=project_name,
        project_description=project_description,
        created_at=datetime.now(),
        api_keys=[]
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

async def create_api_key(user_email: str, project_id: str, validity_days: int = 30) -> Optional[dict]:
    """Create a new API key for a specific project"""
    # Check if user exists
    user = await user_collection.find_one({"email": user_email})
    if not user:
        return None
    
    # Find the project in user's projects
    projects = user.get("projects", [])
    project_index = None
    for i, project in enumerate(projects):
        if project.get("project_id") == project_id:
            project_index = i
            break
    
    if project_index is None:
        return None
    
    # Check if project already has 3 API keys
    project = projects[project_index]
    api_keys = project.get("api_keys", [])
    if len(api_keys) >= 3:
        raise Exception("Project already has the maximum number of API keys (3)")
    
    # Generate a new API key
    key = secrets.token_urlsafe(32)
    
    # Create API key object
    api_key = APIKey(
        key=key,
        created_at=datetime.now(),
        expires_at=datetime.now() + timedelta(days=validity_days),
        is_active=True
    )
    
    # Add API key to project
    result = await user_collection.update_one(
        {"email": user_email, "projects.project_id": project_id},
        {"$push": {"projects.$.api_keys": api_key.model_dump()}}
    )
    
    if result.modified_count == 1:
        return api_key.model_dump()
    
    return None

async def get_project_api_keys(user_email: str, project_id: str) -> List[dict]:
    """Retrieve all API keys for a specific project"""
    user = await user_collection.find_one({"email": user_email})
    if not user:
        return []
    
    # Find the project in user's projects
    projects = user.get("projects", [])
    for project in projects:
        if project.get("project_id") == project_id:
            return project.get("api_keys", [])
    
    return []

async def delete_api_key(user_email: str, project_id: str, api_key: str) -> bool:
    """Delete an API key from a specific project"""
    # Check if user exists
    user = await user_collection.find_one({"email": user_email})
    if not user:
        return False
    
    # Remove API key from project
    result = await user_collection.update_one(
        {"email": user_email, "projects.project_id": project_id},
        {"$pull": {"projects.$.api_keys": {"key": api_key}}}
    )
    
    return result.modified_count == 1

async def get_project_by_id(user_email: str, project_id: str) -> Optional[dict]:
    """Retrieve a specific project by its ID"""
    user = await user_collection.find_one({"email": user_email})
    if not user:
        return None
    
    # Find the project in user's projects
    projects = user.get("projects", [])
    for project in projects:
        if project.get("project_id") == project_id:
            return project
    
    return None

async def get_project_by_api_key(api_key: str) -> Optional[dict]:
    """Retrieve a project by its API key"""
    # Find user with the project that has this API key
    user = await user_collection.find_one({
        "projects.api_keys.key": api_key,
        "projects.api_keys.is_active": True
    })
    
    if not user:
        return None
    
    # Find the project that contains this API key
    for project in user.get("projects", []):
        for key in project.get("api_keys", []):
            expires_at_str = key.get("expires_at")
            
            if key.get("key") == api_key and key.get("is_active"):
                if expires_at_str:  
                    try:
                        pass
                        # expires_at = datetime.fromisoformat(expires_at_str.replace("Z", "+00:00"))
                        # if datetime.now() > expires_at:
                        #     return None  
                    except ValueError:
                        pass
                
                return project
    
    return None
