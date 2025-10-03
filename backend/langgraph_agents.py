from cerebras.cloud.sdk import Cerebras
from langchain_cerebras import ChatCerebras
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from typing import Dict, Any
import json
import os
from dotenv import load_dotenv

load_dotenv()

model = ChatCerebras(model=os.getenv("CEREBRAS_MODEL", 'llama3.1-8b'))

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

# Setting Entry Point
scan_workflow.set_entry_point("convert_json")

# Compile the workflow
scan_app = scan_workflow.compile()
