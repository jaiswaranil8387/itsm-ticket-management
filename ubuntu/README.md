```markdown
# Ubuntu Deployment Environment

This folder provides a Docker-based setup for running the Kubernetes deployment pipeline in a consistent Ubuntu environment, eliminating "it works on my machine" issues.

## Overview

The setup uses a custom Ubuntu Docker image pre-installed with all necessary DevOps tools (AWS CLI, Kubectl, Terraform, Ansible, etc.), allowing deployments to run in a standardized container regardless of the host OS.

## ⚠️ Windows Host Setup (One-Time Configuration)

**Crucial:** All the following steps must be performed on your **Windows Host Machine**. The `docker-compose-ubuntu.yml` file is configured to automatically mount (sync) your Windows credentials into the Linux container. You do **not** need to copy these files into the container manually.

### 1. Configure AWS CLI
If you haven't configured AWS on your Windows machine yet, follow these steps:

1.  Open PowerShell or Command Prompt.
2.  Run the configuration command:
    ```powershell
    aws configure
    ```
3.  Enter your details when prompted:
    - **AWS Access Key ID:** `[Your Access Key]`
    - **AWS Secret Access Key:** `[Your Secret Key]`
    - **Default region name:** `ap-south-1` (or your preferred region)
    - **Default output format:** `json`
    
    *(These credentials will be automatically shared with the container via the `~/.aws` volume map.)*

### 2. Configure GitHub SSH Access
To allow the container to pull code and push changes automatically without passwords:

1.  **Generate a new SSH key** (if you don't have one):
    ```powershell
    ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
    ```
    *Press Enter to accept the default file location (`C:\Users\<User>\.ssh\id_rsa`).*

2.  **Add the key to GitHub:**
    - Copy the public key content:
      ```powershell
      type $env:USERPROFILE\.ssh\id_rsa.pub
      ```
    - Go to **GitHub Settings** > **SSH and GPG keys** > **New SSH key**.
    - Paste the key and save.

### 3. Setup EC2 Key Pair (`flask-key.pem`)
This key is required for Ansible to connect to your EC2 instances.

1.  Login to the **AWS Console** > **EC2** > **Key Pairs**.
2.  Click **Create key pair**.
3.  **Name:** `flask-key`
4.  **Key pair type:** `RSA`
5.  **Private key file format:** `.pem`
6.  Click **Create key pair** to download the file.
7.  **IMPORTANT:** Move the downloaded `flask-key.pem` file to your Windows SSH directory:
    - **Move to:** `C:\Users\<YourUserName>\.ssh\flask-key.pem`
    
    *(The container will look for `~/.ssh/flask-key.pem`, which maps to this location.)*

### 4. Create `.env` File
Create a file named `.env` in this current directory (same folder as `docker-compose-ubuntu.yml`). This file is used to pass sensitive variables into the container securely.

**Example contents:**
```env
# Cloudflare Tunnel Token
TUNNEL_TOKEN=eyJhIjoi...<paste_your_token_here>

# Application Secrets
FLASK_SECRET_KEY=super-secret-key-change-me

```

---

## Quick Start

Once the Windows setup above is complete, you can launch the environment.

1. **Launch the deployment environment:**
```bash
docker-compose -f docker-compose-ubuntu.yml up -d --build

```


2. **Enter the container:**
```bash
docker exec -it k8s-deployer bash

```


3. **Clone the repository (inside container):**
```bash
git clone https://github.com/your-repo/itsm-ticket-management.git ~/itsm-ticket-management
```

4. **Run deployment (inside container):**
Your Windows credentials and keys are now available inside the container.
```bash
cd ~/k8s
./deploy_all.sh

```



## Contents

* **`Dockerfile_Ubuntu`**: Multi-stage Dockerfile that builds the Ubuntu image with pre-installed tools.
* **`docker-compose-ubuntu.yml`**: Configuration that builds the container and mounts the following Windows paths to Linux paths:
  - `.:/home/ubuntu` (Syncs project code)
  - `~/.aws:/home/ubuntu/.aws` (Syncs AWS Creds)
  - `~/.ssh:/home/ubuntu/.ssh` (Syncs SSH Keys)
  - `~/.kube:/home/ubuntu/.kube` (Syncs Kubeconfig)
  - `~/.gitconfig:/home/ubuntu/.gitconfig` (Syncs Git Identity)


* **`itsm-ticket-management/`**: Full copy of the ITSM Ticket Management project repository.
* **`k8s/`**: Kubernetes-specific deployment scripts and manifests.

## Troubleshooting

* **Permission Denied (publickey):** Ensure `flask-key.pem` is strictly inside your Windows `C:\Users\<User>\.ssh\` folder.
* **AWS Errors:** Ensure you ran `aws configure` on Windows and the region matches your Terraform scripts.
* **SSH Connection Refused:** This setup disables SSH multiplexing (`ControlMaster=no`) in `ansible.cfg` to prevent socket errors common in Docker/WSL environments.

```

```