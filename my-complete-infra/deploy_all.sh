#!/bin/bash

# Exit immediately if a command exits with a non-zero status (error).
set -e

# --- 1. Terraform Deployment ---

echo "Starting Terraform deployment for AWS infrastructure..."

# Navigate to the Terraform directory
cd /home/ubuntu/my-complete-infra/terraform-k8s-project

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
cd /home/ubuntu/my-complete-infra/cluster_setup
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory.ini setup_cluster.yml --extra-vars "confirm=yes"

echo "Ansible cluster setup complete."
echo "Infrastructure and Kubernetes cluster deployed successfully! 🎉"

# --- 3. Kubernetes resources deployment ------------
echo "Starting Kubernetes application and database deployment"

cd /home/ubuntu/my-complete-infra/application_deployment
echo "Deploying appplication and database"

ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ../cluster_setup/inventory.ini deploy_k8s_resources.yaml --extra-vars "confirm=yes"
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ../cluster_setup/inventory.ini validate_cluster.yml --extra-vars "confirm=yes"
echo "Completed!!!!!!"

# --- 4. Observability (Logging + Tracing) ---
echo "Starting logging and tracing deployment..."
cd /home/ubuntu/my-complete-infra/monitoring
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ../cluster_setup/inventory.ini deploy-monitoring.yml --extra-vars "confirm=yes"
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ../cluster_setup/inventory.ini deploy-logging.yaml --extra-vars "confirm=yes"
echo "Logging and tracing deployed successfully."
