# SecAI Scan Uploader Action

This GitHub Action submits Trivy JSON scan results to the SecAI backend API for AI-powered vulnerability analysis, reporting, and remediation suggestions.

It is designed to be run immediately after a container image scan using a tool like Trivy, allowing you to integrate SecAI seamlessly into your CI/CD pipeline.

---

## 🚀 Getting Started

To use this action, you must first have the Trivy scan results saved as a JSON file in your workflow environment.

### Prerequisites

1.  **Trivy Scan:** Your CI/CD step before this action must run a Trivy scan and save the output to a JSON file (e.g., `trivy image --format json -o combined-trivy-results.json your-image-name`).
2.  **SecAI Credentials:** You need the following credentials, which should be stored as GitHub Secrets in your repository:
    - `SECAI_URL`
    - `SECAI_PROJECT_ID`
    - `SECAI_PROJECT_API_KEY`

### Usage Example

Add the following step to your GitHub workflow (`.github/workflows/ci.yml`):

```yaml
name: CI/CD Pipeline with SecAI Analysis

on:
  push:
    branches: ["main"]

jobs:
  scan-and-analyze:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      # 1. (Example) Build and Scan your Docker image using Trivy
      - name: Run Trivy Scan
        id: trivy_scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.IMAGE_TAG }}
          scan-type: "image"
          scanners: "vuln"
          exit-code: "0"
          ignore-unfixed: false
          severity: "HIGH,CRITICAL"
          format: "json"
          output: "combined-trivy-results.json"

      # 2. Post Results to SecAI for Analysis
      - name: Upload Scan Results to SecAI
        uses: Naveenchand06/Your-SecAI-Repo/secai-action
        with:
          # Required Inputs (Use your GitHub Secrets)
          secai-url: ${{ secrets.SECAI_URL }}
          project-id: ${{ secrets.SECAI_PROJECT_ID }}
          api-key: ${{ secrets.SECAI_PROJECT_API_KEY }}
          # Optional: Specify the file name if different from the default
          scan-file-path: "combined-trivy-results.json"
```
