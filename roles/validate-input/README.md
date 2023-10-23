Validating User Provided Inputs
=========

This role validates the user provided input against a JSON schema.

This role uses the [schema](./files/input.schema.json) to validate the input. 

Requirements
------------

This role uses the below ansible modules
* [set_fact_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/set_fact_module.html)
* [debug_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/debug_module.html)
* [validate_module](https://docs.ansible.com/ansible/latest/collections/ansible/utils/validate_module.html)

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
          - { role: validate-input, tags: ['validate-input'] }


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