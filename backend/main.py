from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import uvicorn
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="SecAI DevSecOps Assistant", version="0.1.0")

# Initialize Cerebras client
client = Cerebras(
    api_key=os.environ.get("CEREBRAS_API_KEY")
)

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
            "message": "Invalid JSON format received. Please provide Docker scan results in valid JSON format.",
            "explanation": None
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error processing request: {str(e)}",
            "explanation": None
        }
    
    print_scan_results = os.getenv("PRINT_SCAN_RESULTS", "True").lower() == "true"
    # Print the scan result for debugging purposes
    if print_scan_results:
        print("Received Docker scan result:")
        print(json.dumps(scan_result, indent=2))
    
    cerebras_model = os.getenv("CEREBRAS_MODEL", "llama3.1-8b")
    
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a security expert. Provide a human-readable summary of the following Docker vulnerability scan results, highlighting the most critical issues and suggesting remediation steps."
                },
                {
                    "role": "user",
                    "content": f"Here are the Docker scan results: {json.dumps(scan_result)}"
                },
            ],
            model=cerebras_model,
            max_tokens=20000,
            temperature=0.5,
            top_p=0.8
        )
        
        # Extract the explanation from the response
        explanation = "No explanation generated"
        if response.choices:
            explanation = response.choices[0].message.content

        # Return success response
        return {
            "status": "success", 
            "message": "Docker scan result received and processed",
            "explanation": explanation
        }
    except Exception as e:
        # Handle any errors in processing
        return {
            "status": "error",
            "message": f"Failed to generate explanation: {str(e)}",
            "explanation": None
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
