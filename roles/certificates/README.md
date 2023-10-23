Manage Apigee Hybrid Northbould TLS Certificates
=========

This role can generate Self Signed certificates and set them as Kubernetes Secrets. This can be skipped in case of using your own certificates.

Requirements
------------

This role uses the below ansible modules
* [file_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/file_module.html)
* [set_fact_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/set_fact_module.html)
* [openssl_privatekey_module](https://docs.ansible.com/ansible/latest/collections/community/crypto/openssl_privatekey_module.html)
* [openssl_csr_pipe_module](https://docs.ansible.com/ansible/latest/collections/community/crypto/openssl_csr_pipe_module.html)
* [x509_certificate_module](https://docs.ansible.com/ansible/latest/collections/community/crypto/x509_certificate_module.html)
* [slurp_module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/slurp_module.html)
* [k8s_module](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/k8s_module.html)
* [k8s_info_module](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/k8s_info_module.html)

Role Variables
--------------

This takes in the below variables
```
setup_path: "~"
generate_certificates: true
clone_certificates: false
cert_cn: "apigee.com"
tls_namespace: apigee
```

Dependencies
------------

N/A

Example Playbook
----------------

Below is an example of the usage of the role

    - hosts: localhost
      roles:
        - { role: certificates, vars: { generate_certificates: true }, tags: ['certs'] }

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