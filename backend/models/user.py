from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import uuid

class Project(BaseModel):
    project_id: str
    project_name: str
    project_description: Optional[str] = None
    created_at: Optional[datetime] = None

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class User(BaseModel):
    username: str
    email: str
    password: Optional[str] = None
    projects: Optional[List[Project]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserInDB(User):
    hashed_password: str
