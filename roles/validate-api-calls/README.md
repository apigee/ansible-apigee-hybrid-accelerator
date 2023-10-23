Post Setup Validation of Apigee Hybrid
=========

This role verify the Apigee Hybrid setup by deploying sample API proxies.

This role deploys the APIs into Apigee Hybrid using the [script](./files/deploy_api.py) and fetches the Apigee ingress IP deploy and uses curl to invoke an API. 

Requirements
------------

This role uses the below ansible modules
* [file_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/file_module.html)
* [uri_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/uri_module.html)
* [script_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/script_module.html)
* [shell_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/shell_module.html)
* [debug_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/debug_module.html)
* [set_fact_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/set_fact_module.html)

Role Variables
--------------

This takes in the below variables
```
setup_path: "~"
internet_access: true
validate_api_redeploy: false
internet_apis:
- mock
- mock-internal
internal_apis:
- mock-internal
```

Dependencies
------------

N/A

Example Playbook
----------------

Below is an example of the usage of the role

    - hosts: localhost
      roles:
        - { role: validate-api-calls, tags: ['validate'] }


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