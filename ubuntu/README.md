# 🚀 Automated Kubernetes DevOps Pipeline on AWS

![Project Status](https://img.shields.io/badge/Status-Complete-success) ![Terraform](https://img.shields.io/badge/IaC-Terraform-purple) ![Ansible](https://img.shields.io/badge/Config-Ansible-red) ![Kubernetes](https://img.shields.io/badge/Orchestration-Kubernetes-blue) ![Prometheus](https://img.shields.io/badge/Monitoring-Prometheus-orange) ![Elastic](https://img.shields.io/badge/Logging-EFK-green)

## 📋 Table of Contents

- [📖 Project Overview](#-project-overview)
- [🏗️ Architecture](#️-architecture)
- [📂 Repository Structure](#-repository-structure)
- [✅ Prerequisites & Setup Guide](#-prerequisites--setup-guide)
- [🚀 Getting Started](#-getting-started)
- [🔗 Access Points & Domain URLs](#-access-points--domain-urls)
- [🛠️ Key Technical Implementations & Fixes](#️-key-technical-implementations--fixes)
- [📊 Verification](#-verification)
- [🧹 Cleanup](#-cleanup)
- [🆘 Troubleshooting](#-troubleshooting)

## 📖 Project Overview

This repository contains a complete, end-to-end DevOps automation pipeline. It provisions a highly available **Kubernetes Cluster on AWS** using **Terraform**, configures the cluster and worker nodes using **Ansible**, deploys a microservices application (Ticketing System), and sets up a comprehensive **Observability & CD Stack**.

To ensure consistency and eliminate "it works on my machine" issues, this project runs entirely inside a custom **Dockerized Control Node**.

---

## 🏗️ Architecture

The pipeline automates the following architecture:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Terraform     │────▶│   AWS Cloud     │────▶│  3 EC2 Instances│
│                 │     │                 │     │                 │
│ Creates Servers │     │ Infrastructure  │     │ • 1 Master     │
└─────────────────┘     └─────────────────┘     │ • 2 Workers     │
                                                └─────────────────┘
                                                       │
                                                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Ansible      │────▶│   Kubernetes    │────▶│     Cluster     │
│                 │     │                 │     │                 │
│ Deploys K8s     │     │ Kubeadm Setup   │     │ • 1 Master Node │
└─────────────────┘     │ CNI (Calico)    │     │ • 2 Worker Nodes│
                        └─────────────────┘     └─────────────────┘
                                                       │
                                                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Deployments via Ansible                       │
├─────────────────────────────────────────────────────────────────┤
│ • ArgoCD (GitOps)                                               │
│ • Ticketing App (Python/Flask) + Postgres DB                    │
│ • Monitoring: Prometheus + Grafana                              │
│ • Logging: EFK (Elasticsearch + Fluentbit + Kibana)             │
│ • Tracing: Elasticsearch + Jaeger                               │
└─────────────────────────────────────────────────────────────────┘
                                                       │
                                                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Endpoints                                │
├─────────────────────────────────────────────────────────────────┤
│ • Application: aniljaiswar.pp.ua                                │
│ • ArgoCD: argocd.aniljaiswar.pp.ua                              │
│ • Grafana: monitor.aniljaiswar.pp.ua                            │
│ • Kibana: kibana.aniljaiswar.pp.ua                              │
│ • Jaeger: jaeger.aniljaiswar.pp.ua                              │
└─────────────────────────────────────────────────────────────────┘
```

* **Infrastructure:** AWS EC2 Instances (Master & Worker Nodes) via Terraform.
* **Configuration:** Ansible Playbooks for Kubeadm setup, CNI (Calico/Flannel), and joining nodes.
* **Application:** Python/Flask Ticketing App deployed via Kubernetes Manifests (Nginx Ingress).
* **Continuous Delivery:** **ArgoCD** for GitOps-based deployment.
* **Observability Stack:**
    * **Monitoring:** Prometheus + Grafana.
    * **Logging:** EFK Stack (Elasticsearch, **Fluentbit**, Kibana).
    * **Tracing:** Elasticsearch + Jaeger.

---

## 📂 Repository Structure

```text
├── Dockerfile_Ubuntu        # Custom Control Node image (Terraform, Ansible, K8s tools installed)
├── docker-compose-ubuntu.yml# Configuration to mount local code into the container
├── deploy_all.sh            # Master orchestration script
├── terraform-k8s-project/   # Terraform scripts for AWS Infrastructure
├── cluster_setup/           # Ansible playbooks for K8s Cluster bootstrapping
├── application_deployment/  # Deployment manifests for the Ticketing App
└── observability/           # Prometheus, Grafana, EFK, Jaeger & ArgoCD setups

```

---

## ✅ Prerequisites & Setup Guide

Before running the pipeline, follow these setup steps on your host machine.

### 0. Install Docker and Docker Compose

This project requires Docker to run the control node container. Install Docker Desktop (for Windows/Mac) or Docker Engine (for Linux) from the official [Docker website](https://docs.docker.com/get-docker/).

Verify installation:
```bash
docker --version
docker-compose --version
```

### 1. AWS Configuration (`aws configure`)

You need to connect your environment to your AWS account.

1. Open your terminal (or the container terminal).
2. Run the configuration command:
```bash
aws configure

```


3. Enter your details when prompted:
* **AWS Access Key ID:** `Paste Your Key ID`
* **AWS Secret Access Key:** `Paste Your Secret Key`
* **Default region name:** `us-east-1` (or your preferred region like `ap-south-1`)
* **Default output format:** `json`



### 2. SSH Key Pair Setup (GitHub & EC2)

#### **Part A: Create GitHub Access Key (To clone/push code)**

If you haven't set up SSH for GitHub yet:

1. Generate a key pair: `ssh-keygen -t ed25519 -C "your_email@example.com"`
2. Start the agent: `eval "$(ssh-agent -s)"` and add the key: `ssh-add ~/.ssh/id_ed25519`
3. Copy the public key: `cat ~/.ssh/id_ed25519.pub`
4. Go to **GitHub Settings** -> **SSH and GPG Keys** -> **New SSH Key**.
5. Paste the key and save.

#### **Part B: Create EC2 Access Key (For Ansible)**

This key is required for Ansible to log in to your AWS servers.

1. Log in to the **AWS Console** -> **EC2** -> **Key Pairs**.
2. Click **Create key pair**.
3. Name it: `flask-key`
4. Select Format: `.pem` (for OpenSSH).
5. Download the file and **move it** to the `cluster_setup/` `application_deployment/` and `observability/`folder in this project:
```bash
chmod 600 ./cluster_setup/flask-key.pem
chmod 600 ./application_deployment/flask-key.pem
chmod 600 ./observability/flask-key.pem

```



---

## 🚀 Getting Started

### Phase 1: Build the Control Node

We do not install tools locally. We build a standardized Ubuntu container that has all specific versions of Terraform and Ansible pre-installed.

1. **Clone the Repository:**
```bash
git clone https://github.com/jaiswaranil8387/itsm-ticket-management.git
cd ubuntu

```


2. **Launch the Environment:**
This builds the image, creates the `ubuntu` user, and applies global fixes for WSL/Docker compatibility.
```bash
docker-compose -f docker-compose-ubuntu.yml up -d --build

```


3. **Enter the Control Node:**
```bash
docker exec -it k8s-deployer bash

```



### Phase 2: Deploy the Pipeline

Once inside the container (`ubuntu@container-id`), run the deployment:

1. **Initialize Permissions (First Run):**
Ensure the `ubuntu` user owns the workspace to prevent Terraform lock errors.
```bash
sudo chown -R ubuntu:ubuntu ~/k8s
chmod 0755 ~/k8s/deploy_all.sh

```


2. **Run the Master Script:**
This script runs Terraform apply, updates the Ansible inventory dynamically, and triggers the playbooks.
```bash
cd ~/k8s
./deploy_all.sh

```



---

## 🔗 Access Points & Domain URLs

This project uses **Nginx Ingress** to route traffic. We do not use AWS LoadBalancers; traffic is routed directly via the Public IP of the worker nodes mapped to the following domains.

| Service | Protocol | Access URL (Domain) | Credentials (Default) |
| --- | --- | --- | --- |
| **Ticketing App** | HTTP | [aniljaiswar.pp.ua](https://aniljaiswar.pp.ua/) | N/A |
| **Kibana** | HTTPS | [kibana.aniljaiswar.pp.ua](https://kibana.aniljaiswar.pp.ua/) | N/A |
| **Grafana** | HTTPS | [monitor.aniljaiswar.pp.ua](https://monitor.aniljaiswar.pp.ua/) | `admin` / `admin` |
| **ArgoCD** | HTTPS | [argocd.aniljaiswar.pp.ua](https://argocd.aniljaiswar.pp.ua/) | `admin` / *(See below)* |
| **Jaeger UI** | HTTPS | [jaeger.aniljaiswar.pp.ua](https://jaeger.aniljaiswar.pp.ua/) | N/A |

> **DNS Note:** Ensure your DNS provider (`aniljaiswar.pp.ua`) points these subdomains to the **Public IP** of your Kubernetes Worker Node. You can find this IP by running `terraform output` or checking the AWS Console..
>
> **Alternative Access:** If DNS is not configured, you can access the services directly using the Public IP and default ports:
> - Ticketing App: `http://<PublicIP>:80`
> - Kibana: `https://<PublicIP>:443`
> - Grafana: `https://<PublicIP>:443`
> - ArgoCD: `https://<PublicIP>:443`
> - Jaeger UI: `https://<PublicIP>:443`

**To retrieve the initial ArgoCD password:**

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

```

---

## 🛠️ Key Technical Implementations & Fixes

This project includes advanced configurations to solve common DevOps challenges:

### 1. Docker & Ansible Compatibility (The Multiplexing Fix)

* **Problem:** Ansible often fails inside Docker containers on Windows/WSL due to "Control Socket" errors (`Connection refused`).
* **Solution:** We baked a global configuration into `/etc/ansible/ansible.cfg` to disable SSH Multiplexing:
```ini
[ssh_connection]
ssh_args = -o ControlMaster=no -o ControlPath=none

```



### 2. Automated Kibana Configuration

* **Problem:** Kibana deployments usually require manual GUI clicks to set up Index Patterns.
* **Solution:** The pipeline includes a "Wait & Configure" task. It polls the Kibana API until it returns `200 OK`, then uses `curl` to automatically create the `logstash-*` index pattern and set it as default.

### 3. Terraform State Locking Fix

* **Problem:** Running Terraform as root locks state files, making them unreadable by other users.
* **Solution:** The Dockerfile creates a non-root `ubuntu` user (UID 1000) and the pipeline enforces correct ownership (`chown`) before execution.

---

## 📊 Verification

After the script completes (`🎉 DEPLOYMENT COMPLETE!`), verify the setup:

1. **Check Nodes:**
```bash
kubectl get nodes

```


2. **Check Ingress Rules:**
```bash
kubectl get ingress -A

```


3. **Check Logs:**
Visit the **Kibana** URL to see centralized logs from all pods flowing through Fluentbit and Elasticsearch.
4. **Check Traces:**
Visit **Jaeger** to visualize request tracing across the application microservices.

---

## 🧹 Cleanup

To destroy the entire infrastructure and avoid ongoing AWS charges, follow these steps:

### 1. Destroy Kubernetes Resources

Inside the container, run:
```bash
cd ~/k8s
./destroy_all.sh  # If available, or manually delete resources
```

### 2. Destroy Terraform Infrastructure

```bash
cd ~/k8s/terraform-k8s-project
terraform destroy -auto-approve
```

### 3. Stop and Remove Docker Container

On your host machine:
```bash
docker-compose -f ubuntu/docker-compose-ubuntu.yml down
```

> **Warning:** This will permanently delete all resources, including EC2 instances, Kubernetes cluster, and data. Ensure you have backups if needed.

---

## 🆘 Troubleshooting

| Error | Fix |
| --- | --- |
| **Permission Denied (Terraform)** | Run `sudo chown -R ubuntu:ubuntu ~/k8s` inside the container. |
| **SSH Connection Refused** | Ensure `flask-key.pem` is in `cluster_setup/` and permissions are `600`. |
| **Kibana Index Failed** | The script retries automatically. If it fails, check if the Kibana pod is `Running`. |

---

**Author:** Anil Jaiswar
**License:** MIT

```

```