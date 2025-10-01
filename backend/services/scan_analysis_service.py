from database import scan_analysis_collection, scan_analysis_helper
from models.scan_analysis import ScanAnalysis
from bson.objectid import ObjectId
from datetime import datetime
from typing import List

async def add_scan_analysis(scan_analysis_data: dict) -> dict:
    """Add a new scan analysis to the database"""
    scan_analysis_data["created_at"] = datetime.now()
    
    scan_analysis = await scan_analysis_collection.insert_one(scan_analysis_data)
    new_scan_analysis = await scan_analysis_collection.find_one({"_id": scan_analysis.inserted_id})
    return scan_analysis_helper(new_scan_analysis)

async def retrieve_scan_analyses() -> List[dict]:
    """Retrieve all scan analyses from the database"""
    scan_analyses = []
    async for scan_analysis in scan_analysis_collection.find():
        scan_analyses.append(scan_analysis_helper(scan_analysis))
    return scan_analyses

async def retrieve_scan_analysis(id: str) -> dict:
    """Retrieve a scan analysis by ID"""
    scan_analysis = await scan_analysis_collection.find_one({"_id": ObjectId(id)})
    if scan_analysis:
        return scan_analysis_helper(scan_analysis)
    return None

async def update_scan_analysis(id: str, data: dict) -> dict:
    """Update a scan analysis by ID"""
    if len(data) < 1:
        return False
    
    scan_analysis = await scan_analysis_collection.find_one({"_id": ObjectId(id)})
    if scan_analysis:
        updated_scan_analysis = await scan_analysis_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        
        if updated_scan_analysis:
            scan_analysis = await scan_analysis_collection.find_one({"_id": ObjectId(id)})
            return scan_analysis_helper(scan_analysis)
        
    return None

async def delete_scan_analysis(id: str) -> bool:
    """Delete a scan analysis by ID"""
    scan_analysis = await scan_analysis_collection.find_one({"_id": ObjectId(id)})
    if scan_analysis:
        await scan_analysis_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False
