Pre Setup Cluster Readiness check for Apigee Hybrid
=========

This role helps to check if your Kubernetes cluster is ready for Apigee hybrid installation.

Kindly refer the [link](https://cloud.google.com/apigee/docs/hybrid/v1.10/install-check-cluster) for more details.

Requirements
------------

This role uses the below ansible modules
* [file_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/file_module.html)
* [template_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/template_module.html)
* [include_role_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/include_role_module.html)

Role Variables
--------------

This takes in the below variables
```
kubeconfig
```

Dependencies
------------

This role depends on below roles
*  [kubectl-ops](../kubectl-ops/)

Example Playbook
----------------

Below is an example of the usage of the role

    - hosts: localhost
      roles:
          - { role: validate-cluster-readiness, tags: ['validate-cluster-readiness'] }


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