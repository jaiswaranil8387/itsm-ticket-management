# GitHub Actions Workflows

This directory contains GitHub Actions workflows for the ITSM Ticket Management project.

## Workflows

### app-pipeline.yml

**Name:** Python Linting (Flake8)

**Purpose:** This CI/CD pipeline automates code quality checks, security scans, testing, and Docker image building/deployment for the Python Flask application.

#### Triggers
- **Push** to `master` branch when files in `src/` directory are changed
- **Pull Request** to `master` branch when files in `src/` directory are changed

#### Permissions
- `contents: write` - Required for pushing version updates back to the repository

#### Jobs

##### ci-cd-pipeline
Runs on `ubuntu-latest` and includes the following steps:

1. **Checkout Code** - Clones the repository with full history
2. **Set up Python 3.10** - Installs Python with pip caching
3. **Install Dependencies** - Installs app and dev dependencies from requirements files
4. **Run Flake8** - Lints Python code in `src/` directory with specific rules:
   - Max complexity: 11
   - Max line length: 127
   - Shows statistics but doesn't fail the build
5. **Run Tests** - Executes pytest on the test suite in `src/test/`
6. **Run Bandit Security Scan** - Scans for security issues, showing only Medium and High severity
7. **Run pip-audit Security Scan** - Checks for vulnerable dependencies
8. **Run Semgrep Security Scan** - Performs static analysis for security vulnerabilities
9. **Run Gitleaks** - Scans for secrets and sensitive data leaks
10. **Calculate Version** - Generates a new version tag based on base version + GitHub run number
11. **Build Docker Image** - Builds Docker image with the calculated version tag
12. **Run Trivy Vulnerability Scanner** - Scans the Docker image for OS and library vulnerabilities
13. **Log in to Docker Hub** - Authenticates with Docker Hub using secrets
14. **Push Docker Image** - Pushes the versioned and latest tags to Docker Hub
15. **Update K8s Manifest & Push to GitHub** - Updates the Kubernetes deployment manifest with the new image version and commits the change

#### Requirements

**Secrets:**
- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub password
- `GITHUB_TOKEN` - Automatically provided by GitHub

**Files:**
- `src/requirements.txt` - Application dependencies
- `src/requirements-dev.txt` - Development dependencies (Flake8, pytest, bandit, semgrep)
- `src/reports/.trivyignore` - Trivy vulnerability ignore rules
- `k8s/application_deployment/app/active-deployment.yaml` - Kubernetes deployment manifest

#### Outputs

- **Docker Image:** `jaiswaranil8387/anil_doc_repo:{version}` and `latest` tags pushed to Docker Hub
- **Kubernetes Manifest Update:** Automatic update of image version in `k8s/application_deployment/app/active-deployment.yaml`

#### Versioning

The pipeline uses semantic versioning based on:
- Base version extracted from the current Kubernetes manifest
- GitHub Actions run number as the patch version
- Format: `v{base}.{run_number}` (e.g., `v7.45`)

#### Security Features

- **Code Quality:** Flake8 linting
- **Testing:** pytest unit tests
- **Security Scans:**
  - Bandit for Python security issues
  - pip-audit for dependency vulnerabilities
  - Semgrep for static analysis
  - Gitleaks for secrets detection
  - Trivy for container vulnerabilities

#### Notes

- The pipeline is designed to be non-blocking for most checks (using `--exit-zero` flags) to allow development to continue while maintaining quality gates
- Version updates are automatically committed with `[skip ci]` to prevent infinite loops
- All scans focus on the `src/` directory to maintain scope and performance
