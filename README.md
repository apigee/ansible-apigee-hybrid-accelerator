# Ansible playbooks to deploy Apigee Hybrid using Helm Charts

[![E2E Testing](https://github.com/apigee/ansible-apigee-hybrid-accelerator/actions/workflows/testing.yml/badge.svg)](https://github.com/apigee/ansible-apigee-hybrid-accelerator/actions/workflows/testing.yml)

This repository contains a set of Ansible roles and playbooks to manage the installation, configuration and maintenance of Apigee Hybrid in your environment. Apigee Hybrid components are managed using helm charts through ansible roles.Apigee Hybrid combines the power of Apigee's API management with the flexibility and control of Kubernetes. With this playbooks, you can automate common Apigee Hybrid management tasks, making it easier to deploy, configure, and maintain your Apigee Hybrid clusters.


> Refer the [official doc](https://cloud.google.com/apigee/docs/hybrid/preview/helm-install) for more details on Helm charts for Apigee Hybrid.

## Ansible Apigee Hybrid Accelerator Features
The Ansible playbooks in this repository support a wide range of the installation, configuration and maintenance use cases that are necessary to successfully manage Apigee Hybrid clusters. We describe the uses cases that are supported as follows:

| Feature Name | Feature Description |
| --- | --- |
| Single Region Deployment | Apigee Hybrid single region deployment|
| Multi-Region Deployment | Apigee Hybrid Multi region deployment|
| DC Decomission | Apigee Hybrid single or all region/DC decommission  |
| Apigee Hybrid Component management | Apigee Hybrid component configuration/re-configuration/decommission. |
| Apigee Upgrade | Apigee Hybrid In-place/Blue-Green Upgrade 1.10.x to 1.11.x |
| Apigee Upgrade | Apigee Hybrid In-place/Blue-Green Upgrade 1.11.x to 1.12.x |

### Prerequisites

#### Setting up the Apigee Hybrid Control plane
You can use the Apigee terraform [module](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/apigee#all-resources-hybrid-control-plane) to setup the Apigee Hybrid control plane 

#### Install Required packages to run the playbook

##### Manual packages to install
You can follow manual steps  to install the below packages

-  ```
    python3 -m pip install --no-cache-dir \
        requests==2.25.1 \
        jsonschema==4.19.1 \
        jsonschema-specifications==2023.7.1 \
        jmespath==1.0.1 \
        kubernetes==27.2.0 \
        ansible-core==2.15.5 \
        ansible==8.5.0
   ```
- `helm >3.14.2`  refer https://helm.sh/docs/intro/install/
    > Note: The version of helm keeps changing as apigee hybrid versions keep getting updated.
    > Refer the official [documentation](https://cloud.google.com/apigee/docs/hybrid/supported-platforms) for the right  helm version to be used.
- `gcloud cli`   refer https://cloud.google.com/sdk/docs/install
- `kubectl`  refer https://cloud.google.com/sdk/docs/components#installing_components

    To continue to install follow the [steps](#configure-ansible-variables)

OR

##### Use Docker Image

Install [docker](https://docs.docker.com/engine/install/)

Run the below command to build the docker image
```
docker build -t <image_name>:<image_tag> .
```

To run the playbooks using docker

```
docker run -it  -v $(pwd):/app <image_name>:<image_tag> /bin/bash
cd /app
```

To continue to install follow the [steps](#configure-ansible-variables)


### Configure Ansible Variables

Before using the Ansible playbooks you need to configure the necessary variables. 
Modify the variable files located in the [vars](./vars) directory to match your environment.

Refer [Example Vars](vars/vars.yaml)

## Ansible tags
The playbook exposes tags to selectively run tasks depending on the need.

Below are the tags that are exposed in the playbook

Ansible tag | Functionality
--- | ---
dc1 | Deploy Apigee Hybrid on Primary Kubeconfig
dc2 | Deploy Apigee Hybrid on Secondary Kubeconfig
ao | Deploy apigee-operator Helm Chart
apigee-virtualhost | Deploy apigee-virtualhost  Helm Chart
apigeeds | Deploy apigee-datastore Helm Chart
apigeeenv | Deploy apigee-env Helm Chart
apigeeingress | Deploy apigee-ingress-manager Helm Chart
apigeeorg | Deploy apigee-org Helm Chart
apigeeorgs | Deploy apigee-org Helm Chart
apigeeredis | Deploy apigee-redis Helm Chart
apigeetelem | Deploy apigee-telemetry Helm Chart
at | Deploy apigee-telemetry Helm Chart
bootstrap-apigee-crds | Deploy Apigee CRDS
cert-manager | Deploy Cert Manager
certs | Create Certificates for VirtualHost
ds | Deploy apigee-datastore Helm Chart
enable-synchronizer | Enable Apigee Synchronizer
generate-overrides | Generate Apigee Overrides
prepare-helm | Download Apigee Hybrid Helm charts
prepare-service-accounts | Create Service Keys & K8s Secrets
validate-input | Validates the inputs given to the playbook
validate-input-apigee | Validates the existence of apigee objects using the apigee.googleapis.com API
validate-input-k8s | Validates the existence of kubernetes objects using given kubeconfig
validate | Validate Apigee Hybrid By deploying & invoking mock API
wait_ao | Wait for apigee-operator to be up
wait_apigeeenv | Wait for apigee enviornment custom resource to be running
wait_apigeeingress | Wait for apigee ingress to be up
wait_apigeeorg | Wait for apigee-org custom resource to be running
wait_apigeeredis | Wait for apigee-redis to be up
wait_at | Wait for apigee-telemetry to be up
wait_ds | Wait for apigee-datastore (cassadra) to be up
wait_virtualhost | Wait for apigee-route-config custom resource to be running

## Authenticate gcloud and helm

### Authenticate to gcloud cli as shown below
> Ensure the Authenticating user OR service account has `roles/apigee.admin` role.

```
gcloud auth application-default login
```

### [Optional] Authenticate to helm registry if using self hosted or private registry

```
gcloud auth application-default print-access-token | helm registry login -u oauth2accesstoken \
--password-stdin https://<artifact-registry-region>-docker.pkg.dev
```

## Usage

Below are some of the usage patterns.

### Primary DC  Installation Only

To deploy Apigee Hybrid in 1 Region only run the ansible playbook as shown below

```
ansible-playbook playbook.yaml -e @vars/vars.yaml  --tags "dc1"
```

### Primary & Secondary DC  Installation Only

To deploy Apigee Hybrid in 2 Regions run the ansible playbook as shown below

```
ansible-playbook playbook.yaml -e @vars/vars.yaml
```

### Decommission Primary DC  Only

To decommission Apigee Hybrid in the first region run the ansible playbook as shown below

```
ansible-playbook decommission.yaml -e @vars/vars.yaml --tags dc1
```

### Decommission Primary & Secondary DC  

To decommission Apigee Hybrid from both Regions run the ansible playbook as shown below

```
ansible-playbook decommission.yaml -e @vars/vars.yaml
```

### Apigee Hybrid Component management
To manage components via playbook you need to run playbook while passing the selective ansible tag.Some scenarios are listed below

#### Validate the provided inputs
To validate the inputs given to ansible
```
ansible-playbook playbook.yaml -e @vars/vars.yaml  --tags "validate-input" 
```

#### Validate the current setup
To validate a running setup by executing mock APIs.
```
ansible-playbook playbook.yaml -e @vars/vars.yaml  --tags "validate"
```

#### To Update Apigee VirtualHost
To update the Apigee Virtual Hosts.
```
ansible-playbook playbook.yaml -e @vars/vars.yaml  --tags "validate-input,generte-overrides,apigee-virtualhost,wait_virtualhost,validate"
```

#### Cassandra Custom Storage Classes
To use custom storage classes for cassandra statefulsets, you can populate the `storageClass` parameter in the vars file that you are using. By defining a custom storage class, it will first be created in your cluster and then set as the storage class of the cassandra statefulsets. You will also need to specify the `provisionerType` and the `parameters`. You can use the following provisioners:
- gke 
- aks
- eks
- anthos-vsphere-csi
*Note: If you face any issues with any of the provisioners, please create a github issue in this repository*


#### Running Known Issue fixes.
> Note: In case of multi-dc , this needs to be run against each DC.
> Ensure the relevant kubernetes context is configured.

To run the fixes for known issues.
```
ansible-playbook known_issues.yaml
```


> Note: Currently fix for following issues are supported.
> * https://cloud.google.com/apigee/docs/release/known-issues#416634326

## Limitations
* Refer [link](https://cloud.google.com/apigee/docs/hybrid/preview/helm-install#limitations)


## Contributing
We welcome contributions from the community. If you would like to contribute to this project, please see our [Contribution Guidelines](./CONTRIBUTING.md).

## License

All solutions within this repository are provided under the
[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) license.
Please see the [LICENSE](./LICENSE) file for more detailed terms and conditions.

## Disclaimer

This repository and its contents are not an official Google product.
