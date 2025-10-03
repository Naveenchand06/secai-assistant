from fastapi import FastAPI, Request, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import json
import os
import uvicorn
from dotenv import load_dotenv
from langgraph_agents import scan_app, ScanState
from database import scan_analysis_collection, scan_analysis_helper, test_connection, client, user_collection
from models.scan_analysis import ScanAnalysis
from models.user import UserCreate, UserLogin, Project, APIKey
from services.auth_service import register_user, login_user, get_current_user, get_user
from services.project_service import create_project, get_user_projects, create_api_key, get_project_api_keys, delete_api_key, get_project_by_id, get_project_by_api_key
from datetime import datetime
from contextlib import asynccontextmanager
from pydantic import BaseModel
import asyncio
from jose import JWTError, jwt

# Optional authentication function for API key endpoints
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)

async def get_current_user_optional(token: str = Depends(oauth2_scheme)) -> dict:
    """Get the current user from the JWT token if available, otherwise return None"""
    if not token:
        return None
        
    try:
        # Import SECRET_KEY and ALGORITHM from auth_service
        from services.auth_service import SECRET_KEY, ALGORITHM
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
    except JWTError:
        return None
    
    user = await get_user(email)
    if user is None:
        return None
    
    return user

# Project creation request model
class ProjectCreate(BaseModel):
    project_name: str
    project_description: str = None

# API key creation request model
class APIKeyCreate(BaseModel):
    validity_days: int = 30

# Load environment variables from .env file
load_dotenv()

async def get_project_from_api_key(api_key: str) -> dict:
    """Get project associated with an API key"""
    # Find user with the project that has this API key
    user = await user_collection.find_one({
        "projects.api_keys.key": api_key,
        "projects.api_keys.is_active": True
    })
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or inactive API key"
        )
    
    # Find the project that contains this API key
    for project in user.get("projects", []):
        for key in project.get("api_keys", []):
            if key.get("key") == api_key and key.get("is_active"):
                # Check if API key is expired
                if datetime.now() > datetime.fromisoformat(key.get("expires_at").replace("Z", "+00:00")):
                    raise HTTPException(
                        status_code=401,
                        detail="API key has expired"
                    )
                return project
    
    raise HTTPException(
        status_code=401,
        detail="Invalid API key"
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Test database connection on startup
    """
    try:
        connection_success = await test_connection()
        if connection_success:
            print("Database connection successful!")
        else:
            print("Database connection failed!")
    except Exception as e:
        print(f"Error testing database connection: {e}")

    yield 

app = FastAPI(title="SecAI", version="0.1.0", lifespan=lifespan)

# CORS middleware to allow requests for receiving webhooks from GitHub Actions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    """
    Health check endpoint to verify the application is running
    """
    return {"status": "healthy", "message": "SecAI DevSecOps Assistant is running....;) 💚"}


@app.post("/register")
async def register(user_data: UserCreate):
    """
    Register a new user
    """
    return await register_user(user_data)


@app.post("/login")
async def login(user_data: UserLogin):
    """
    Login endpoint to authenticate user and return JWT token
    """
    return await login_user(user_data)


@app.post("/projects")
async def create_new_project(project_data: ProjectCreate, current_user: dict = Depends(get_current_user)):
    """Create a new project for the authenticated user"""
    project = await create_project(current_user.email, project_data.project_name, project_data.project_description)
    if project:
        return project
    raise HTTPException(
        status_code=500,
        detail="Failed to create project"
    )

@app.get("/projects")
async def list_user_projects(current_user: dict = Depends(get_current_user)):
    """Get all projects for the authenticated user"""
    projects = await get_user_projects(current_user.email)
    return projects

@app.get("/projects/{project_id}")
async def get_project(project_id: str, current_user: dict = Depends(get_current_user)):
    """Get a specific project by ID for the authenticated user"""
    project = await get_project_by_id(current_user.email, project_id)
    if project:
        return project
    raise HTTPException(
        status_code=404,
        detail="Project not found"
    )

@app.post("/projects/{project_id}/api-keys")
async def create_project_api_key(project_id: str, api_key_data: APIKeyCreate, current_user: dict = Depends(get_current_user)):
    """Create a new API key for a specific project"""
    try:
        api_key = await create_api_key(current_user.email, project_id, api_key_data.validity_days)
        if api_key:
            return api_key
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    except Exception as e:
        if "maximum number of API keys" in str(e):
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        raise HTTPException(
            status_code=500,
            detail="Failed to create API key"
        )

@app.get("/projects/{project_id}/api-keys")
async def list_project_api_keys(project_id: str, current_user: dict = Depends(get_current_user)):
    """Get all API keys for a specific project"""
    api_keys = await get_project_api_keys(current_user.email, project_id)
    return api_keys

@app.delete("/projects/{project_id}/api-keys/{api_key}")
async def delete_project_api_key(project_id: str, api_key: str, current_user: dict = Depends(get_current_user)):
    """Delete an API key from a specific project"""
    success = await delete_api_key(current_user.email, project_id, api_key)
    if success:
        return {"message": "API key deleted successfully"}
    raise HTTPException(
        status_code=404,
        detail="Project or API key not found"
    )

@app.get("/projects/{project_id}/scan-results")
async def get_project_scan_results(project_id: str, current_user: dict = Depends(get_current_user)):
    """Get all scan results for a specific project"""
    # Verify that the project belongs to the current user
    project = await get_project_by_id(current_user.email, project_id)
    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    
    # Retrieve scan analyses associated with this project
    scan_results = []
    async for scan_analysis in scan_analysis_collection.find({"project_id": project_id}):
        scan_results.append(scan_analysis_helper(scan_analysis))
    
    return scan_results

@app.post("/projects/{project_id}/scan/docker")
async def receive_docker_scan(
    project_id: str,
    request: Request, 
    x_api_key: str = Header(None),
    current_user: dict = Depends(get_current_user_optional)
):
    """
    Endpoint to receive Docker scan results from GitHub Actions workflow.
    Can be authenticated either with a JWT token or an API key.
    """
    project_info = None
    print("TEST: current user ", current_user)
    print("TEST: api-key ", x_api_key)

    # If no JWT token user, try to authenticate with API key
    if not current_user and x_api_key:
        # Validate API key
        project = await get_project_by_api_key(x_api_key)
        print("TEST: project from api key ", project)
        
        # If API key is valid, check if it belongs to the specified project
        if project:
            # Verify that the project ID from the API key matches the project ID in the URL
            if project.get("project_id") != project_id:
                raise HTTPException(
                    status_code=403,
                    detail="API key does not belong to the specified project"
                )
            project_info = project
        else:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired API key"
            )
    
    # If neither authentication method is provided or valid, raise an error
    if not current_user and not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )
    
    # Check if request body is empty
    body = await request.body()
    if not body:
        raise HTTPException(
            status_code=400,
            detail="Empty request body received. Please provide Docker scan results in JSON format."
        )

    # Get the JSON body from the request
    try:
        scan_result = await request.json()
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON format received. Please provide a valid JSON format."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )
    
    print_scan_results = os.getenv("PRINT_SCAN_RESULTS", "True").lower() == "true"
    # Printing for debugging purposes
    if print_scan_results:
        print("Received Docker scan result:")
        print(json.dumps(scan_result, indent=2))
    
    # Using LangGraph multi-agent system to process the scanresult
    try:
        # Initialize the state with scan data
        initial_state = ScanState({
            "scan_data": scan_result,
            "human_readable": "",
            "risk_analysis": "",
            "solutions": ""
        })
        
        final_state = scan_app.invoke(initial_state)
        
        # Create scan analysis object
        scan_analysis = ScanAnalysis(
            status="success",
            message="Docker scan result received and processed through multi-agent system",
            human_readable=final_state.get("human_readable", ""),
            risk_analysis=final_state.get("risk_analysis", ""),
            solutions=final_state.get("solutions", ""),
            scan_data=scan_result,
            created_at=datetime.now()
        )
        
        # Save to MongoDB
        scan_analysis_dict = scan_analysis.model_dump()
        scan_analysis_dict.pop("id", None)
        
        # Add project information if authenticated with API key
        if project_info:
            scan_analysis_dict["project_id"] = project_info.get("project_id")
            scan_analysis_dict["project_name"] = project_info.get("project_name")
        
        # Insert into database
        result = await scan_analysis_collection.insert_one(scan_analysis_dict)
        
        # Add the MongoDB document ID to the response
        response_data = {
            "id": str(result.inserted_id),
            "status": "success",
            "message": "Docker scan result received and processed through multi-agent system",
            "human_readable": final_state.get("human_readable", ""),
            "risk_analysis": final_state.get("risk_analysis", ""),
            "solutions": final_state.get("solutions", "")
        }
        
        # Add project information to response if authenticated with API key
        if project_info:
            response_data["project_id"] = project_info.get("project_id")
            response_data["project_name"] = project_info.get("project_name")
        
        # Return success response
        return response_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process scan result: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
