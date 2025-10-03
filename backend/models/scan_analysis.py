from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class ScanAnalysis(BaseModel):
    status: str
    message: str
    human_readable: str
    risk_analysis: str
    solutions: str
    scan_data: Dict[str, Any]
    project_id: Optional[str] = None
    project_name: Optional[str] = None
    created_at: Optional[datetime] = None
