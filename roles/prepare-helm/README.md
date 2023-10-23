Helm Release Management using Helm Ops
=========

This role helps in pulling the required helm charts needed for Apigee Hybrid deployment

Requirements
------------

This role uses the below ansible modules
* [file_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/file_module.html)
* [find_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/find_module.html)
* [set_fact_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/set_fact_module.html)
* [debug_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/debug_module.html)
* [helm_module](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/helm_pull_module.html)

Role Variables
--------------

This takes in the below variables
```
setup_path: "~"
helm_chart_repo: oci://us-docker.pkg.dev/apigee-release/apigee-hybrid-helm-charts
helm_chart_version: 1.10.3
helm_charts:
- apigee-operator
- apigee-datastore
- apigee-env
- apigee-ingress-manager
- apigee-org
- apigee-redis
- apigee-telemetry
- apigee-virtualhost
```

Dependencies
------------

N/A

Example Playbook
----------------

Below is an example of the usage of the role

    - hosts: localhost
      roles:
          - { role: prepare-helm, tags: ['prepare-helm'] }


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