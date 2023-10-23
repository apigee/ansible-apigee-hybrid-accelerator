Validating User Provided Inputs against Apigee Control Plane
=========

This role validates the user provided input against Apigee Control Plane (https://apigee.googleapis.com)

This role uses the [script](./files/validate_apigee_objects.py) to validate.

Requirements
------------

This role uses the below ansible modules
* [set_fact_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/set_fact_module.html)
* [debug_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/debug_module.html)
* [fail_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/fail_module.html)
* [shell_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/shell_module.html)
* [script_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/script_module.html)

Role Variables
--------------

This takes in all the variables as given in the [vars](../../vars/vars.yaml)

and 

```
control_plane_validation_status: true
```

Dependencies
------------

N/A

Example Playbook
----------------

Below is an example of the usage of the role

    - hosts: localhost
      roles:
          - { role: validate-input-apigee-control-plane, tags: ['validate-input','validate-input-apigee'] }


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