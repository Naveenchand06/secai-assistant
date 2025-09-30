# SecAI Vulnerable Demo Project

This project contains intentionally vulnerable code for testing security scanning tools like Trivy.

## Backend Application

The backend is a Python Flask application with the following vulnerabilities:

1. **Outdated Flask version (0.12.3)** - Contains multiple security vulnerabilities including:

   - CVE-2018-1000656: Weak password hashing
   - CVE-2019-1010083: Open redirect
   - Other vulnerabilities related to this version

2. **Outdated Requests library (2.19.1)** - Contains security vulnerabilities:

   - CVE-2018-18074: Improper certificate validation

3. **Outdated Django version (1.11.20)** - Contains security vulnerabilities:

   - Multiple CVEs for this version including XSS, SQL injection, and CSRF vulnerabilities

4. **Outdated Jinja2 version (2.7.2)** - Contains security vulnerabilities:

   - CVE-2016-10745: Template injection vulnerability

5. **Outdated Werkzeug version (0.15.3)** - Contains security vulnerabilities:

   - CVE-2019-14806: HTTP header injection

6. **Insecure Code Pattern in app.py**:
   - The `/fetch` endpoint is vulnerable to Server-Side Request Forgery (SSRF) as it makes requests to user-provided URLs without validation

## Frontend Application

The frontend uses vulnerable versions of JavaScript libraries:

1. **Outdated jQuery version (1.12.4)** - Contains security vulnerabilities:

   - CVE-2015-9251: Cross-site scripting (XSS)
   - CVE-2019-11358: Prototype pollution
   - CVE-2020-11022: Cross-site scripting (XSS)

2. **Outdated Lodash version (4.17.10)** - Contains security vulnerabilities:

   - CVE-2019-10744: Prototype pollution
   - CVE-2020-8203: Prototype pollution

3. **Outdated Express version (4.15.2)** - Contains security vulnerabilities:

   - CVE-2017-16139: Regular expression denial of service (ReDoS)
   - CVE-2018-3714: Path traversal vulnerability

4. **Outdated Handlebars version (4.0.12)** - Contains security vulnerabilities:
   - CVE-2019-19919: Prototype pollution
   - CVE-2021-23369: Remote code execution

## Dockerfile

The backend Dockerfile uses Python 3.6-alpine which is an outdated version and may contain OS-level vulnerabilities.

## Testing with Trivy

You can scan this project with Trivy using the following commands:

```bash
# Scan the backend requirements
trivy fs secai-project-demo/backend/requirements.txt

# Scan the frontend package.json
trivy fs secai-project-demo/frontend/package.json

# Scan the backend Docker image
trivy image --input secai-project-demo/backend/Dockerfile

# Scan for all vulnerabilities
trivy fs secai-project-demo/
```
