#!/bin/bash
set -e

CERT_FOLDER="${1:-client1}"
CLIENT_CERT_CN="${2:-Test Client}"

openssl req \
    -newkey rsa:2048 \
    -nodes -keyform PEM \
    -keyout "$CERT_FOLDER/client-ca.key" \
    -x509 -days 3650 \
    -outform PEM \
    -out "$CERT_FOLDER/client-ca.crt" \
    -subj "/CN=$CLIENT_CERT_CN CA"

# openssl genrsa -out "$CERT_FOLDER/example-client.key" 2048

# openssl req \
#     -new -key "$CERT_FOLDER/example-client.key" \
#     -out "$CERT_FOLDER/example-client.csr" \
#     -subj "/CN=$CLIENT_CERT_CN"

# openssl x509 \
#     -req -in "$CERT_FOLDER/example-client.csr" \
#     -CA "$CERT_FOLDER/client-ca.crt" \
#     -CAkey "$CERT_FOLDER/client-ca.key" \
#     -set_serial 101 -days 365 \
#     -outform PEM -out "$CERT_FOLDER/example-client.crt"