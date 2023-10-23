Wait for Kubernetes Objects to reach a specific state
=========

This role waits until a kubernetes objects reaches a runnning OR a certain user provided state.

Requirements
------------

This role uses the below ansible modules
* [k8s_info_module](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/k8s_info_module.html)

Role Variables
--------------

This takes in below variables.

```
label_selectors: []
custom_wait: false
custom_state: running
```

Dependencies
------------

N/A

Example Playbook
----------------

Below is an example of the usage of the role

    - hosts: localhost
      roles:
          - { role: wait-for-k8s-resource, vars: { k8s_api_version: apps/v1, k8s_kind: StatefulSet, k8s_namespace: apigee, k8s_resource_name: apigee-cassandra-default }, tags: ['ds', 'apigeeds','wait_ds'] }



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