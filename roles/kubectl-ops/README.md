Manage Kubectl operations
=========

This role helps in interacting with kuberntes cluster using kubectl cli.

Requirements
------------

This role uses the below ansible modules
* [debug_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/debug_module.html)
* [set_fact_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/set_fact_module.html)
* [k8s_info_module](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/k8s_info_module.html)
* [shell_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/shell_module.html)


Role Variables
--------------

This takes in the below variables
```
k8s_namespace: default
k8s_resource_type: ''
k8s_resource: ''
kubectl_args: ''
check_ns: ''
check_ns_flag: false
```

Dependencies
------------

N/A

Example Playbook
----------------

Below is an example of the usage of the role

    - hosts: localhost
      roles:
        - { role: kubectl-ops, vars: { operation: get, k8s_resource_type: namespace, k8s_resource: apigee, kubectl_args: '--kubeconfig {{ kubeconfigs.primary }} -o yaml > {{ setup_path }}/apigee-namespace.yaml'}, tags: ['dc2-prereq'] }


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