from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import uvicorn
from dotenv import load_dotenv
from langgraph_agents import scan_app, ScanState

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="SecAI", version="0.1.0")

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

@app.post("/scan/docker")
async def receive_docker_scan(request: Request):
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
    
    # Check if the JSON object is empty
    if not scan_result:
        raise HTTPException(
            status_code=400,
            detail="Empty JSON object received. Please provide Docker scan results in JSON format."
        )
    
    print_scan_results = os.getenv("PRINT_SCAN_RESULTS", "True").lower() == "true"
    # Printingf for debugging purposes
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
        
        # Return success response
        return {
            "status": "success",
            "message": "Docker scan result received and processed through multi-agent system",
            "human_readable": final_state.get("human_readable", ""),
            "risk_analysis": final_state.get("risk_analysis", ""),
            "solutions": final_state.get("solutions", "")
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process scan result: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
