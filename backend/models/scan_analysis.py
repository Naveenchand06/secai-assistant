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
    created_at: Optional[datetime] = None
