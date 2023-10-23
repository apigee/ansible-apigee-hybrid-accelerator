Manage Apigee Hybrid Service Account Secrets
=========

This role can download GCP Service Account JSON Keys and set them as Kubernetes Secrets. This can be skipped in case of using your own service account secrets.

Requirements
------------

This role uses the below ansible modules
* [file_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/file_module.html)
* [copy_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/copy_module.html)
* [shell_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/shell_module.html)
* [set_fact_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/set_fact_module.html)
* [slurp_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/slurp_module.html)
* [k8s_module](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/k8s_module.html)
* [k8s_info_module](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/k8s_info_module.html)

Role Variables
--------------

This takes in the below variables
```
setup_path: "~"
create_service_account: false
clone_secret: false
deployment_environment: prod
svc_account_script_path: helm/apigee-operator/etc/tools/create-service-account
apigee_empty_secrets: []
missing_svc_account_files: []
svc_account_prod:
- apigee-logger
- apigee-metrics
- apigee-cassandra
- apigee-udca
- apigee-synchronizer
- apigee-mart
- apigee-watcher
- apigee-runtime

svc_account_non_prod:
- apigee-non-prod

```

Dependencies
------------

N/A

Example Playbook
----------------

Below is an example of the usage of the role

    - hosts: localhost
      roles:
        - { role: prepare-service-accounts, vars: { clone_secret: true, kubeconfig: "{{ kubeconfigs.primary }}" }, tags: ['prepare-service-accounts'] }


License
-------

Apache 2.0

Author Information
------------------

Ashwin Kumar Naik
<!-- BEGIN Google How To Contribute -->
# How to Contribute

We'd love to accept your patches and contributions to this project. Please review our [guidelines](../../CONTRIBUTING.md).
<!-- END Google How To Contribute -->
<!-- BEGIN Google Required Disclaimer -->

# Not Google Product Clause

This is not an officially supported Google product.
<!-- END Google Required Disclaimer -->