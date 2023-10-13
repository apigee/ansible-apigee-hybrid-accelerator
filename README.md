# Ansible playbooks to deploy Apigee Hybrid using Helm Charts

This repository contains a set of Ansible roles and playbooks to manage the installation, configuration and maintenance of Apigee Hybrid in your environment. Apigee Hybrid components are managed using helm charts through ansible roles.Apigee Hybrid combines the power of Apigee's API management with the flexibility and control of Kubernetes. With this playbooks, you can automate common Apigee Hybrid management tasks, making it easier to deploy, configure, and maintain your Apigee Hybrid instances.


> Refer the [official doc](https://cloud.google.com/apigee/docs/hybrid/preview/helm-install) for more details on Helm charts for Apigee Hybrid.

## Ansible Apigee Hybrid Accelerator Features
The Ansible playbooks in this repository support a wide range of the installation, configuration and maintenance use cases that are necessary to successfully manage Apigee Hybrid clusters. We describe the uses cases that are supported as follows:

| Feature Name | Feature Description |
| --- | --- |
| Single Region Deployment | Apigee Hybrid single region deployment|
| Multi-Region Deployment | Apigee Hybrid Multi region deployment|
| DC Decomission | Apigee Hybrid single or all region/DC decommission  |
| Apigee Hybrid Component management | Apigee Hybrid component configuration/re-configuration/decommission. |

### Prerequisites

#### Setting up the Apigee Hybrid Control plane
You can use the Apigee terraform [module](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/apigee#all-resources-hybrid-control-plane) to setup the Apigee Hybrid control plane 

#### Install Required packages to run the playbook

##### Manual packages to install
You can follow manual steps  to install the below packages

- `python3 -m pip install requests==2.25.1 jsonschema==4.19.1 jsonschema-specifications==2023.7.1`
- `helm >3.10`  refer https://helm.sh/docs/intro/install/
- `ansible >=2.1`  refer https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html
- `gcloud cli`   refer https://cloud.google.com/sdk/docs/install
- `kubectl`  refer https://cloud.google.com/sdk/docs/components#installing_components

OR

##### Use Ansible to install packages

Install [ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

Use the playbook to deploy.
> NOTE: The `pre-req.yaml` playbook has not been tested on all OS flavours.
> Use with caution

```
sudo ansible-playbook pre-req.yaml -e 'install_helm=true' -e 'install_pip=true' -e 'install_helm=true'
```

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
