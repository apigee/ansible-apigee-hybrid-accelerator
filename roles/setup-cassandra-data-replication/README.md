Setting up Apigee Hybrid Cassandra Data Replication
=========

This role helps you to configure cassandra data replication in Apigee Hybrid. Refer [link](https://cloud.google.com/apigee/docs/hybrid/v1.10/multi-region#gke_1:~:text=Set%20up%20Cassandra%20on%20all%20the%20pods%20in%20the%20new%20data%20centers) for more details

Requirements
------------

This role uses the below ansible modules
* [file_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/file_module.html)
* [fail_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/fail_module.html)
* [debug_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/debug_module.html)
* [k8s_module](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/k8s_module.html)
* [k8s_info_module](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/k8s_info_module.html)
* [template_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/template_module.html)

Role Variables
--------------

This takes in the below variables
```
apigee_org_crd_api_version: apigee.cloud.google.com/v1alpha2
apigee_ds_crd_api_version: apigee.cloud.google.com/v1alpha1
apigee_source_dc: dc-1
apigee_org_cr_name: ''
cassandra_data_replication_resource: cassandra-data-replication
cassandra_data_replication_yaml: datareplication.yaml
```

Dependencies
------------

N/A

Example Playbook
----------------

Below is an example of the usage of the role

    - hosts: localhost
      roles:
        - { role: setup-cassandra-data-replication, vars: { kubeconfig: "{{ kubeconfigs.primary }}" }, tags: ['cassandra-dr']}



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