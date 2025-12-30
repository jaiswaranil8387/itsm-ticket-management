#!/bin/bash

# Exit immediately if a command exits with a non-zero status (error).
set -e

# --- 1. Terraform Deployment ---

echo "Starting Terraform deployment for AWS infrastructure..."

# Navigate to the Terraform directory
cd /home/ubuntu/k8s/terraform-k8s-project

# Initialize Terraform (downloads providers and modules)
terraform init

# Show the execution plan
terraform plan

# Apply the Terraform configuration without prompting for confirmation
# The -auto-approve flag is critical for non-interactive execution.
terraform apply -auto-approve

echo "Terraform deployment complete."

# --- 2. Ansible Cluster Setup ---

echo "Starting Ansible playbook for Kubernetes cluster setup..."

# Navigate to the Ansible directory
cd /home/ubuntu/k8s/cluster_setup
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory.ini setup_cluster.yml --extra-vars "confirm=yes"

echo "Ansible cluster setup complete."
echo "Infrastructure and Kubernetes cluster deployed successfully! 🎉"

# --- 3. Kubernetes resources deployment ------------

echo "----------------------------------------------------"
echo "PHASE 1: Deploy Controllers and Operators..."
echo "----------------------------------------------------"
cd /home/ubuntu/k8s/application_deployment
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ../cluster_setup/inventory.ini deploy_controllers_and_operators.yaml

echo "----------------------------------------------------"
echo "PHASE 2: Installing Argo CD & Deploying App..."
echo "----------------------------------------------------"
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ../cluster_setup/inventory.ini install_argocd.yaml

echo "Waiting 45 seconds for Argo CD to initialize resources..."
sleep 45

echo "----------------------------------------------------"
echo "PHASE 3: Post-Deployment Configuration (DB & Secrets)..."
echo "----------------------------------------------------"
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ../cluster_setup/inventory.ini deploy_secrets_and_dbbackup.yaml

echo "----------------------------------------------------"
echo "PHASE 4: Installing Observability Stack..."
echo "----------------------------------------------------"
cd /home/ubuntu/k8s/observability
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ../cluster_setup/inventory.ini install_observability.yaml

echo "Waiting 60 seconds for Monitoring/Logging pods to start..."
sleep 60

echo "----------------------------------------------------"
echo "PHASE 5: Configuring Observability (Secrets & Glue)..."
echo "----------------------------------------------------"
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ../cluster_setup/inventory.ini configure_observability.yaml

echo "🎉 DEPLOYMENT COMPLETE!"