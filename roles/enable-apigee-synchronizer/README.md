Enabling Apigee Synchronizer 
=========

This role helps in enabling Apigee Synchronizer. Refer this [link](https://cloud.google.com/apigee/docs/hybrid/v1.10/install-enable-synchronizer-access) for more details.

When `deployment_environment` is `prod` , `synchronizer_prod_svc_account` variable is used as synchronizer service account else `synchronizer_non_prod_svc_account` is used. 

If [prepare-service-accounts](../prepare-service-accounts/) role is NOT used to create service accounts then service account can be provded by the variables `synchronizer_prod_svc_account` OR `synchronizer_non_prod_svc_account` depending on the environment

Requirements
------------

This role uses the below ansible modules
* [file_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/file_module.html)
* [set_fact_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/set_fact_module.html)
* [uri_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/uri_module.html)
* [debug_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/debug_module.html)

Role Variables
--------------

This takes in the below variables
```
deployment_environment: prod
synchronizer_prod_svc_account: apigee-synchronizer
synchronizer_non_prod_svc_account: apigee-non-prod
```

Dependencies
------------

* [prepare-service-accounts](../prepare-service-accounts/)  -> Soft Dependency

Example Playbook
----------------

Below is an example of the usage of the role

    - hosts: localhost
      roles:
        - { role: enable-apigee-synchronizer, tags: ['enable-synchronizer'] }

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