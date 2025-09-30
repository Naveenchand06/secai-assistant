from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import uvicorn
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras
from langchain_cerebras import ChatCerebras
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from typing import Dict, Any, List

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="SecAI", version="0.1.0")

model = ChatCerebras(model="llama3.1-8b")

# State structure 
class ScanState(dict):
    scan_data: Dict[str, Any]
    human_readable: str
    risk_analysis: str
    solutions: str


def convert_json_report(state: ScanState) -> ScanState:
    """Convert and validate JSON report"""
    return state

def make_human_readable(state: ScanState) -> ScanState:
    """Convert technical scan data into human-readable format"""
    scan_data = state.get("scan_data", {})
    
    # Create a prompt for making the report human-readable
    prompt = f"""
    You are security specialist. Convert the following Docker vulnerability scan results into a human-readable format:
    {json.dumps(scan_data, indent=2)}
    
    Please format the output in a clear, structured way that is easy for non-technical stakeholders to understand.
    """
    
    response = model.invoke([HumanMessage(content=prompt)])
    state["human_readable"] = response.content
    return state

def analyze_security_risks(state: ScanState) -> ScanState:
    """Analyze security risks from the scan data"""
    scan_data = state.get("scan_data", {})
    human_readable = state.get("human_readable", "")
    
    # Create a prompt for analyzing security risks
    prompt = f"""
    You are a security expert. Analyze the following Docker vulnerability scan results and identify the security risks:
    
    Human-readable report:
    {human_readable}
    
    Technical scan data:
    {json.dumps(scan_data, indent=2)}
    
    Please highlight the most critical issues and their potential impact.
    """
    
    response = model.invoke([HumanMessage(content=prompt)])
    state["risk_analysis"] = response.content
    return state

def suggest_solutions(state: ScanState) -> ScanState:
    """Suggest solutions for the identified security risks"""
    scan_data = state.get("scan_data", {})
    human_readable = state.get("human_readable", "")
    risk_analysis = state.get("risk_analysis", "")
    
    # Create a prompt for suggesting solutions
    prompt = f"""
    You are Secirty Specialist and DevSecOps Engineer. Based on the following security risk analysis, suggest practical solutions and remediation steps:
    
    Risk Analysis:
    {risk_analysis}
    
    Human-readable report:
    {human_readable}
    
    Technical scan data:
    {json.dumps(scan_data, indent=2)}
    
    Please provide actionable steps that can be taken to address these vulnerabilities.
    """
    
    response = model.invoke([HumanMessage(content=prompt)])
    state["solutions"] = response.content
    return state

# LangGraph workflow
scan_workflow = StateGraph(ScanState)

# Adding nodes for each agent
scan_workflow.add_node("convert_json", convert_json_report)
scan_workflow.add_node("make_readable", make_human_readable)
scan_workflow.add_node("analyze_risks", analyze_security_risks)
scan_workflow.add_node("suggest_solutions", suggest_solutions)

# Add edges to define the workflow - sequential execution
scan_workflow.add_edge("convert_json", "make_readable")
scan_workflow.add_edge("make_readable", "analyze_risks")
scan_workflow.add_edge("analyze_risks", "suggest_solutions")
scan_workflow.add_edge("suggest_solutions", END)

# Setting Netry Point
scan_workflow.set_entry_point("convert_json")

# Compile the workflow
scan_app = scan_workflow.compile()

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
    return {"status": "healthy", "message": "SecAI DevSecOps Assistant is running 💚"}

@app.post("/scan/docker")
async def receive_docker_scan(request: Request):
    """
    Endpoint to receive Docker scan results from GitHub Actions workflow
    """
    # Check if request body is empty
    body = await request.body()
    if not body:
        return {
            "status": "error",
            "message": "Empty request body received. Please provide Docker scan results in JSON format.",
            "explanation": None
        }

    # Get the JSON body from the request
    try:
        scan_result = await request.json()
    except json.JSONDecodeError as e:
        return {
            "status": "error",
            "message": "Invalid JSON format received. Please provide a valid JSON format.",
            "explanation": None
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error processing request: {str(e)}",
            "explanation": None
        }
    
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
        return {
            "status": "error",
            "message": f"Failed to process scan result through multi-agent system: {str(e)}",
            "human_readable": None,
            "risk_analysis": None,
            "solutions": None
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
