#!/bin/bash

# Exit immediately if a command exits with a non-zero status (error).
set -e
PROJECT_ROOT=$(pwd)

echo "Current Project Root set to: $PROJECT_ROOT"

# 1. Load secrets from .env if it exists (for Local Dev)
if [ -f .env ]; then
  set -a  # Automatically export all variables
  source .env
  set +a
fi

# 2. Safety Check: Stop if token is missing
if [ -z "$TUNNEL_TOKEN" ]; then
  echo "ERROR: TUNNEL_TOKEN is not set. Please set it or create a .env file."
  exit 1
fi

# --- 1. Terraform Deployment ---

echo "Starting Terraform deployment for AWS infrastructure..."

# Navigate to the Terraform directory
cd "$PROJECT_ROOT/terraform-k8s-project"

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
cd "$PROJECT_ROOT/cluster_setup"
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory.ini setup_cluster.yml --extra-vars "confirm=yes"

echo "Ansible cluster setup complete."
echo "Infrastructure and Kubernetes cluster deployed successfully! 🎉"

# --- 3. Kubernetes resources deployment ------------

echo "----------------------------------------------------"
echo "PHASE 1: Deploy Controllers and Operators..."
echo "----------------------------------------------------"
cd "$PROJECT_ROOT/application_deployment"
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ../cluster_setup/inventory.ini deploy_controllers_and_operators.yaml --extra-vars "confirm=yes"

echo "----------------------------------------------------"
echo "PHASE 2: Installing Argo CD & Deploying App..."
echo "----------------------------------------------------"
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ../cluster_setup/inventory.ini install_argocd.yaml --extra-vars "confirm=yes"

echo "Waiting 45 seconds for Argo CD to initialize resources..."
sleep 45

echo "----------------------------------------------------"
echo "PHASE 3: Post-Deployment Configuration (DB & Secrets)..."
echo "----------------------------------------------------"
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ../cluster_setup/inventory.ini deploy_secrets_and_dbbackup.yaml --extra-vars "confirm=yes"


echo "----------------------------------------------------"
echo "PHASE 4: Installing Observability Stack..."
echo "----------------------------------------------------"
cd "$PROJECT_ROOT/observability"
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ../cluster_setup/inventory.ini install_observability.yaml --extra-vars "confirm=yes"

echo "Waiting 60 seconds for Monitoring/Logging pods to start..."
sleep 60

echo "----------------------------------------------------"
echo "PHASE 5: Configuring Observability (Secrets & Glue)..."
echo "----------------------------------------------------"
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ../cluster_setup/inventory.ini configure_observability.yaml --extra-vars "confirm=yes"

echo "🎉 DEPLOYMENT COMPLETE!"

cd "$PROJECT_ROOT/application_deployment"

ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ../cluster_setup/inventory.ini validate_cluster.yml --extra-vars "confirm=yes"

echo "🎉 VALIDATION COMPLETE!"