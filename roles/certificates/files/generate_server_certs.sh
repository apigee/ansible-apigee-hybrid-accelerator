#!/bin/bash
set -e -x

CERT_FOLDER="${1}"
CERT_CN="${2}"
CERT_SAN_CN="${3}"
CERT_SAN_CN=$(awk -F',' '{ for( i=1; i<=NF; i++ ) print $i }' <<<"$CERT_SAN_CN")

SAN=""
for dns in $CERT_SAN_CN
do 
    SAN+="DNS:$dns, "
done

SAN=$(echo $SAN | sed 's/,*$//g')
echo $SAN

openssl req  \
    -nodes \
    -new \
    -x509 \
    -keyout "$CERT_FOLDER/server.key" \
    -out "$CERT_FOLDER/server.crt" \
    -subj "/CN=$CERT_CN" \
    -addext "subjectAltName=$SAN" \
    -days 3650
