from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import uvicorn
from dotenv import load_dotenv
from langgraph_agents import scan_app, ScanState
from database import scan_analysis_collection, scan_analysis_helper, test_connection, client
from models.scan_analysis import ScanAnalysis
from models.user import UserCreate, UserLogin, Project
from services.auth_service import register_user, login_user, get_current_user
from services.project_service import create_project, get_user_projects
from datetime import datetime
from contextlib import asynccontextmanager
from pydantic import BaseModel

# Project creation request model
class ProjectCreate(BaseModel):
    project_name: str
    project_description: str = None

# Load environment variables from .env file
load_dotenv()

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

@app.post("/scan/docker")
async def receive_docker_scan(request: Request, current_user: dict = Depends(get_current_user)):
    """
    Endpoint to receive Docker scan results from GitHub Actions workflow
    """
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
    
    # print_scan_results = os.getenv("PRINT_SCAN_RESULTS", "True").lower() == "true"
    # # Printingf for debugging purposes
    # if print_scan_results:
    #     print("Received Docker scan result:")
    #     print(json.dumps(scan_result, indent=2))
    
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
        
        # Return success response
        return response_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process scan result: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
