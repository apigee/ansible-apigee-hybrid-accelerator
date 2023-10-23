Helm Release Management using Helm Ops
=========

This role helps in creating/updating/uninstalling a helm release.

Requirements
------------

This role uses the below ansible modules
* [file_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/file_module.html)
* [helm_module](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/helm_module.html)

Role Variables
--------------

This takes in the below variables
```
setup_path: "~"
custom_values: false
loop_values: false
set_values: []
release_namespace: apigee
create_namespace: false
release_state: present
```

Dependencies
------------

N/A

Example Playbook
----------------

Below is an example of the usage of the role

    - hosts: localhost
      roles:
        - { role: helm-ops, vars: { release_name: 'datastore', chart_ref: 'apigee-datastore'}, tags: ['ds', 'apigeeds'] }



Below is an example of the usage of the role with custom values

      - name: deploy environment-group
        include_role: {name: helm-ops, apply: { tags: apigee-virtualhost }}
        vars:
          release_name: "{{ item.name }}"
          chart_ref: 'apigee-virtualhost'
          custom_values: true
          set_values: 
          - value: "envgroup={{ item.name }}"
            value_type: string
        loop: "{{ overrides.virtualhosts }}"
        tags: ['apigee-virtualhost']



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