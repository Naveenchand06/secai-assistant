# ⛊ SecAI Assistant: AI-Powered DevSecOps Intelligence

SecAI Assistant is an **AI-driven platform** built to modernize and simplify the **DevSecOps workflow**.

It ingests raw vulnerability data from open-source scanners (like **Trivy**) and leverages **Meta’s Llama models**, running on the **Cerebras AI compute platform**, to **analyze, prioritize, explain, and generate precise remediation steps** for security findings.

This repository provides the complete project structure, including the **frontend application**, the **backend API**, and the **GitHub Action** for smooth CI/CD integration.

---

## 🙌 Powered By & Special Thanks

This project is powered by **[Cerebras](https://cloud.cerebras.ai)** and **[Meta Llama Models](https://inference-docs.cerebras.ai/models/llama-33-70b)**

- **Cerebras**: The creators of the **world’s largest and fastest AI chip**, paired with an inferencing platform.
- **Meta Llama Models**: Advanced open-weight LLMs designed for cutting-edge reasoning and language tasks.

> ⚡ SecAI Assistant uses **Cerebras Cloud AI** to process vulnerability scan results, making analysis significantly faster compared to other LLMs such as **GPT** or **Gemini Models**.

Special thanks to **[WeMakeDevs](https://github.com/WeMakeDevs)** for organizing the [FuturStack GenAI Hackathon](https://www.wemakedevs.org/hackathons/futurestack25)

---

## 🚀 Live Demo & Access

🎥 **Watch the Demo Video:**

[![SecAI Demo](https://img.youtube.com/vi/YPyKlW_tZSM/0.jpg)](https://www.youtube.com/watch?v=YPyKlW_tZSM)


Experience the SecAI Assistant directly:

➡️ **Application:** [https://secai-assistant.vercel.app/](https://secai-assistant.vercel.app/)

---

## ✨ Core Features

- **Intelligent Analysis:** Converts technical vulnerability reports into clear, natural language explanations.
- **Prioritization:** Uses AI to assess the real-world impact and likelihood of exploitation, helping teams focus on critical issues first.
- **Actionable Remediation:** Generates precise, easy-to-implement code patches and configuration changes to fix vulnerabilities.
- **Seamless Integration:** Dedicated GitHub Action for one-step deployment into existing CI pipelines.

---

## 📦 Project Structure (Monorepo)

This repository is structured as a **monorepo** to manage the different components of the SecAI Assistant ecosystem:

| Folder          | Description                                                                                            | Technology Stack                              |
| --------------- | ------------------------------------------------------------------------------------------------------ | --------------------------------------------- |
| `frontend/`     | The user interface for viewing scan results, analysis, and remediation suggestions.                    | React, TypeScript, Tailwind CSS, Vercel       |
| `backend/`      | The core API service responsible for data ingestion, authentication, and communication with AI models. | Python, Fast API, Meta Llama Models, Cerebras, Google Cloud |
| `secai-action/` | The source code for the official GitHub Action that uploads Trivy JSON reports to the backend.         | Composite Action (Shell Script), YAML               |

---

## 🔗 CI/CD Integration

To easily integrate SecAI Assistant into your existing **Continuous Integration workflows**, use our dedicated GitHub Action.

The action automatically posts your vulnerability scan results to the SecAI backend for analysis:

```yaml
- name: Upload Scan Results to SecAI
  uses: Naveenchand06/secai-assistant/secai-action@v1.0.0
  with:
    secai-url: ${{ secrets.SECAI_URL }}
    project-id: ${{ secrets.SECAI_PROJECT_ID }}
    api-key: ${{ secrets.SECAI_PROJECT_API_KEY }}
    scan-file-path: "combined-trivy-results.json"
```
