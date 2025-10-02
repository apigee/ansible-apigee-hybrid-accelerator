# Test Scripts

This directory contains scripts for testing the Ansible Apigee Hybrid Accelerator.

## Scripts

- `deploy_terraform.sh`: This script deploys the Terraform configurations for the control plane and runtime plane. It initializes Terraform with a backend bucket and then applies the configurations in the `terraform/control-plane` and `terraform/runtime-plane-gke` directories.
- `run_playbook.sh`: This script runs an Ansible playbook in a Docker container to test the deployment. It replaces placeholder values in the `vars/test.yaml` file with environment variables, and then executes the playbook. It also handles logging and error reporting by copying the logs to a GCS bucket.
- `setup_workload_identity.sh`: This script sets up a GCP Workload Identity pool and provider for GitHub Actions. It creates a service account, assigns it the necessary roles, and configures the Workload Identity pool to allow GitHub Actions to impersonate the service account. This allows the GitHub Actions workflows to authenticate with GCP and run the tests.
