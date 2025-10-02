# Terraform Configurations

This directory contains the Terraform configurations for the test environment.

## Subdirectories

- `control-plane`: This directory contains the Terraform configuration for the Apigee control plane. It creates the Apigee organization, service accounts, and other resources required for the control plane.
- `runtime-plane-gke`: This directory contains the Terraform configuration for the GKE cluster that will be used as the Apigee runtime plane. It creates a private GKE cluster with the necessary node pools and other configurations.
