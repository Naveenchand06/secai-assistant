from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class Project(BaseModel):
    project_name: str
    project_id: str

class User(BaseModel):
    username: str
    email: str
    password: str
    projects: Optional[List[Project]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
