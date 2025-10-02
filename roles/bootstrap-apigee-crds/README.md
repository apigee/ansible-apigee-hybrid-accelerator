Bootstrap Apigee Custom Resource Definitions
=========

This role applies the Apigee Custom Resource Definitions.Refer [this](https://cloud.google.com/apigee/docs/hybrid/kubernetes-resources#apigee:) to check the list of CRDs. This role first performs a dry-run to validate the changes before applying them.

Requirements
------------

This role uses the below ansible modules
* [file_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/file_module.html)
* [shell_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/shell_module.html)
* [async_status_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/async_status_module.html)
* [debug_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/debug_module.html)

Role Variables
--------------

This takes in all the variables as given in the [vars](../../vars/vars.yaml)

Dependencies
------------

This role depends on below roles
*  [prepare-helm](../prepare-helm/)

Example Playbook
----------------

Below is an example of the usage of the role

    - hosts: localhost
      roles:
          - { role: prepare-helm, tags: ['prepare-helm'] }
          - { role: bootstrap-apigee-crds, tags: ['bootstrap-apigee-crds'] }

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