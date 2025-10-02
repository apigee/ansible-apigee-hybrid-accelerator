Role Name
=========

This role applies workarounds for Apigee Hybrid known issues.

Requirements
------------

* `kubectl` should be configured to connect to the Apigee Hybrid cluster.
* The user running the playbook should have cluster-admin privileges.

Role Variables
--------------

* `setup_path`: The path to a directory on the remote host where temporary files will be created. Defaults to `~`.
* `enable_fixes`: A list of fixes to apply. The default list of fixes is:
  * `416634326_delete_crd`
  * `416634326_update_role`
  * `416634326_rollout_restart`

Dependencies
------------

This role has no dependencies on other Ansible roles.

Example Playbook
----------------

Here is an example of how to use this role:

```yaml
- hosts: localhost
  connection: local
  roles:
    - apigee-known-issues
```

License
-------

Apache 2.0

Author Information
------------------

This role was created by the Google Apigee team.
