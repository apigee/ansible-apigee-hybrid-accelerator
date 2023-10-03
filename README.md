# Ansible Playbooks to deploy Apigee Hybrid

To run the ansible playbook follow the below steps


### Pre-Requistes

#### Manual packages to install
Install the below packages

- `python3 -m pip install requests==2.25.1`
- helm >3.10 
- ansible >=2.1
- gcloud cli
- kubectl

OR

#### Use Ansible to install packages
Use the playbook to deploy.
> NOTE: The `pre-req.yaml` playbook has not been tested on all OS flavours.
> Use with caution

```
sudo ansible-playbook pre-req.yaml -e 'install_helm=true' -e 'install_pip=true' -e 'install_helm=true'
```

### Configure Ansible Variables

Please fill in the `vars.yaml`.

Here is an [Example Vars](vars/vars.yaml)


### Run Ansible playbook
To run the run the ansible playbook run the below command

```
ansible-playbook playbook.yaml -e @vars/vars.yaml
```

Provide your kubeconfig paths in `kubeconfigs` parameter in `vars.yaml` files.
Refer [Example Vars](vars/vars.yaml)

```yaml
# Kubeconfigs
kubeconfigs:
  primary: /tmp/dc1.config
  secondary: /tmp/dc2.config
  ```


## Ansible tags
The playbook exposes tags to selectively run tasks depending on the need.

Below are the tags that are exposed in the playbook

tag | function
--- | ---
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
validate | Validate Apigee Hybrid By deploying & invoking mock API

To run the run the ansible playbook with a specific tag , run the below command

```
ansible-playbook playbook.yaml -e @vars/vars.yaml  --tags "validate"
```
