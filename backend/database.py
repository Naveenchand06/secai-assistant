import motor.motor_asyncio
import os
import logging
from dotenv import load_dotenv
import certifi

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# MongoDB connection setup
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DATABASE = os.getenv("DATABASE_NAME", "secai")

logger.info(f"Database name: {MONGODB_DATABASE}")

# Create MongoDB client
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL, tlsCAFile=certifi.where())
database = client[MONGODB_DATABASE]

# Test connection
async def test_connection():
    try:
        await client.admin.command('ping')
        logger.info("MongoDB connection successful!")
        return True
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}")
        return False

# Collections
user_collection = database.get_collection("users")
scan_analysis_collection = database.get_collection("scan_analyses")

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "projects": user["projects"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }

def scan_analysis_helper(scan_analysis) -> dict:
    return {
        "id": str(scan_analysis["_id"]),
        "status": scan_analysis["status"],
        "message": scan_analysis["message"],
        "human_readable": scan_analysis["human_readable"],
        "risk_analysis": scan_analysis["risk_analysis"],
        "solutions": scan_analysis["solutions"],
        "scan_data": scan_analysis["scan_data"],
        "created_at": scan_analysis["created_at"]
    }
