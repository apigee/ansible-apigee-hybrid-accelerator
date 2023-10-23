Deploy & Validate Certificate Manager
=========

This role deploys and validates the Certificate Manager. Refer [link](https://cloud.google.com/apigee/docs/hybrid/v1.10/install-cert-manager) for details.

Requirements
------------

This role uses the below ansible modules
* [file_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/file_module.html)
* [uri_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/uri_module.html)
* [k8s_module](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/k8s_module.html)
* [k8s_info_module](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/k8s_info_module.html)

Role Variables
--------------

This takes in the below variables
```
setup_path: "~"
install_cert_manager: true
cert_manager_version: v1.7.2
cert_manager_status: present
```

Dependencies
------------

N/A

Example Playbook
----------------

Below is an example of the usage of the role

    - hosts: localhost
      roles:
          - { role: cert-manager, tags: ['cert-manager'] }

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