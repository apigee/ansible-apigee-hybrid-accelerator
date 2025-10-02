# Ansible Playbooks for Apigee Hybrid Deployment using Helm Charts

[![E2E Testing](https://github.com/apigee/ansible-apigee-hybrid-accelerator/actions/workflows/testing.yml/badge.svg)](https://github.com/apigee/ansible-apigee-hybrid-accelerator/actions/workflows/testing.yml)

This repository provides a comprehensive set of Ansible roles and playbooks to automate the installation, configuration, and maintenance of Apigee Hybrid. The playbooks leverage Helm charts to manage Apigee Hybrid components, simplifying the deployment process and operational tasks.

> For more details on Helm charts for Apigee Hybrid, refer to the [official documentation](https://cloud.google.com/apigee/docs/hybrid/preview/helm-install).

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [1. Configure Ansible Variables](#1-configure-ansible-variables)
  - [2. Authenticate with gcloud and Helm](#2-authenticate-with-gcloud-and-helm)
- [Usage](#usage)
  - [Installation](#installation)
  - [Decommissioning](#decommissioning)
  - [Component Management](#component-management)
- [Ansible Tags](#ansible-tags)
- [Known Issues](#known-issues)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

## Features

The Ansible playbooks in this repository support a wide range of use cases for managing Apigee Hybrid clusters:

| Feature Name | Feature Description |
| --- | --- |
| Single Region Deployment | Deploy Apigee Hybrid in a single region. |
| Multi-Region Deployment | Deploy Apigee Hybrid across multiple regions. |
| DC Decommission | Decommission a single or all regions/DCs of Apigee Hybrid. |
| Component Management | Configure, re-configure, or decommission individual Apigee Hybrid components. |
| Apigee Upgrade | Perform in-place or blue-green upgrades for versions 1.12.x to 1.15.x. |

## Prerequisites

Before you begin, ensure you have the following prerequisites in place:

### Apigee Hybrid Control Plane

Set up the Apigee Hybrid control plane using the official Apigee Terraform [module](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/apigee#all-resources-hybrid-control-plane).

### Required Tools

You can install the necessary tools manually or use the provided Docker image.

#### Manual Installation

1.  **Python Packages:**
    ```bash
    python3 -m pip install --no-cache-dir \
        requests==2.25.1 \
        jsonschema==4.19.1 \
        jsonschema-specifications==2023.7.1 \
        jmespath==1.0.1 \
        kubernetes==27.2.0 \
        ansible-core==2.15.5 \
        ansible==8.5.0
    ```

2.  **Helm:**
    Install Helm `>3.14.2`. Refer to the [Helm installation guide](https://helm.sh/docs/intro/install/).
    > **Note:** The required Helm version may change with new Apigee Hybrid releases. Always consult the [official documentation](https://cloud.google.com/apigee/docs/hybrid/supported-platforms) for the correct version.

3.  **gcloud CLI:**
    Install the Google Cloud CLI. Refer to the [gcloud installation guide](https://cloud.google.com/sdk/docs/install).

4.  **kubectl:**
    Install `kubectl`. Refer to the [kubectl installation guide](https://cloud.google.com/sdk/docs/components#installing_components).

#### Docker Image

1.  **Install Docker:**
    Follow the instructions at [docker.com](https://docs.docker.com/engine/install/) to install Docker.

2.  **Build the Docker Image:**
    ```bash
    docker build -t <image_name>:<image_tag> .
    ```

3.  **Run the Docker Container:**
    ```bash
    docker run -it -v $(pwd):/app <image_name>:<image_tag> /bin/bash
    cd /app
    ```

## Getting Started

### 1. Configure Ansible Variables

Before running the playbooks, you need to configure the necessary variables. Modify the variable files in the `vars/` directory to match your environment.

Refer to the [example vars file](vars/vars.yaml) for guidance.

### 2. Authenticate with gcloud and Helm

#### gcloud Authentication

Authenticate the gcloud CLI. The user or service account must have the `roles/apigee.admin` role.

```bash
gcloud auth application-default login
```

#### Helm Registry Authentication (Optional)

If you are using a self-hosted or private Helm registry, authenticate as follows:

```bash
gcloud auth application-default print-access-token | helm registry login -u oauth2accesstoken \
--password-stdin https://<artifact-registry-region>-docker.pkg.dev
```

## Usage

Here are some common usage patterns for the playbooks.

### Installation

-   **Single DC Installation:**
    To deploy Apigee Hybrid in a single region, run:
    ```bash
    ansible-playbook playbook.yaml -e @vars/vars.yaml --tags "dc1"
    ```

-   **Multi-DC Installation:**
    To deploy Apigee Hybrid in two regions, run:
    ```bash
    ansible-playbook playbook.yaml -e @vars/vars.yaml
    ```

### Decommissioning

-   **Single DC Decommission:**
    To decommission Apigee Hybrid in the first region, run:
    ```bash
    ansible-playbook decommission.yaml -e @vars/vars.yaml --tags "dc1"
    ```

-   **Multi-DC Decommission:**
    To decommission Apigee Hybrid from both regions, run:
    ```bash
    ansible-playbook decommission.yaml -e @vars/vars.yaml
    ```

### Component Management

You can manage individual components by using specific Ansible tags.

-   **Validate Inputs:**
    To validate the inputs provided to Ansible, run:
    ```bash
    ansible-playbook playbook.yaml -e @vars/vars.yaml --tags "validate-input"
    ```

-   **Validate Setup:**
    To validate a running setup by deploying and invoking mock APIs, run:
    ```bash
    ansible-playbook playbook.yaml -e @vars/vars.yaml --tags "validate"
    ```

-   **Update Apigee VirtualHost:**
    To update the Apigee Virtual Hosts, run:
    ```bash
    ansible-playbook playbook.yaml -e @vars/vars.yaml --tags "validate-input,generte-overrides,apigee-virtualhost,wait_virtualhost,validate"
    ```

### Cassandra Custom Storage Classes

To use custom storage classes for Cassandra statefulsets, populate the `storageClass` parameter in your vars file. You will also need to specify the `provisionerType` and `parameters`. The following provisioners are supported:

-   `gke`
-   `aks`
-   `eks`
-   `anthos-vsphere-csi`

*Note: If you encounter issues with any of the provisioners, please open a GitHub issue in this repository.*

## Ansible Tags

The playbook exposes tags to selectively run tasks.

| Ansible Tag | Functionality |
| --- | --- |
| `dc1` | Deploy Apigee Hybrid on the primary kubeconfig. |
| `dc2` | Deploy Apigee Hybrid on the secondary kubeconfig. |
| `ao` | Deploy the `apigee-operator` Helm chart. |
| `apigee-virtualhost` | Deploy the `apigee-virtualhost` Helm chart. |
| `apigeeds` | Deploy the `apigee-datastore` Helm chart. |
| `apigeeenv` | Deploy the `apigee-env` Helm chart. |
| `apigeeingress` | Deploy the `apigee-ingress-manager` Helm chart. |
| `apigeeorg` | Deploy the `apigee-org` Helm chart. |
| `apigeeredis` | Deploy the `apigee-redis` Helm chart. |
| `apigeetelem` | Deploy the `apigee-telemetry` Helm chart. |
| `bootstrap-apigee-crds` | Deploy Apigee CRDs. |
| `cert-manager` | Deploy Cert Manager. |
| `certs` | Create certificates for the VirtualHost. |
| `enable-synchronizer` | Enable the Apigee Synchronizer. |
| `generate-overrides` | Generate Apigee overrides. |
| `prepare-helm` | Download Apigee Hybrid Helm charts. |
| `prepare-service-accounts` | Create service account keys and Kubernetes secrets. |
| `validate-input` | Validate the inputs given to the playbook. |
| `validate-input-apigee` | Validate the existence of Apigee objects using the `apigee.googleapis.com` API. |
| `validate-input-k8s` | Validate the existence of Kubernetes objects using the given kubeconfig. |
| `validate` | Validate Apigee Hybrid by deploying and invoking a mock API. |
| `wait_ao` | Wait for the `apigee-operator` to be up. |
| `wait_apigeeenv` | Wait for the Apigee environment custom resource to be running. |
| `wait_apigeeingress` | Wait for the Apigee ingress to be up. |
| `wait_apigeeorg` | Wait for the `apigee-org` custom resource to be running. |
| `wait_apigeeredis` | Wait for `apigee-redis` to be up. |
| `wait_at` | Wait for `apigee-telemetry` to be up. |
| `wait_ds` | Wait for `apigee-datastore` (Cassandra) to be up. |
| `wait_virtualhost` | Wait for the `apigee-route-config` custom resource to be running. |


## Known Issues

To run fixes for known issues, use the `known_issues.yaml` playbook.

> **Note:** In a multi-DC setup, this needs to be run against each DC. Ensure the relevant Kubernetes context is configured.

```bash
ansible-playbook known_issues.yaml
```

Currently, a fix for the following issue is supported:
-   [#416634326](https://cloud.google.com/apigee/docs/release/known-issues#416634326)

## Limitations

Refer to the [official documentation](https://cloud.google.com/apigee/docs/hybrid/preview/helm-install#limitations) for limitations.

## Contributing

We welcome contributions from the community. Please see our [Contribution Guidelines](./CONTRIBUTING.md) for more information.

## License

All solutions within this repository are provided under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). Please see the [LICENSE](./LICENSE) file for more details.

## Disclaimer

This repository and its contents are not an official Google product.
