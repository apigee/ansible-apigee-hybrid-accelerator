Apigee Hybrid Overrides/Values Generator
=========

This role generates a Apigee Hybrid Overrides file , which be used as a input to all the helm releases.
For more details about overrides file refer [link](https://cloud.google.com/apigee/docs/hybrid/v1.10/install-configure-cluster#prod)

Requirements
------------

This role uses the below ansible modules
* [file_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/file_module.html)
* [template_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/template_module.html)

Role Variables
--------------

This takes in all the variables as given in the [vars](../../vars/vars.yaml)

Dependencies
------------

N/A

Example Playbook
----------------

Below is an example of the usage of the role

    - hosts: localhost
      roles:
           - { role: apigee-hybrid-overrides, tags: ['generate-overrides'] }

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