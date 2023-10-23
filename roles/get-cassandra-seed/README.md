Get Cassandra Seed
=========

This role helps in fetching Cassandra Seed IP for Apigee Hybrid Multi-region deployments.

Requirements
------------

This role uses the below ansible modules
* [fail_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/fail_module.html)
* [debug_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/debug_module.html)
* [k8s_info_module](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/k8s_info_module.html)

Role Variables
--------------

This takes in the below variables
```
kubeconfig
```

Dependencies
------------

N/A

Example Playbook
----------------

Below is an example of the usage of the role

    - hosts: localhost
      roles:
          - { role: get-cassandra-seed, vars: { kubeconfig: "{{ kubeconfigs.primary }}" }, tags: ['cass-seed'] }


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