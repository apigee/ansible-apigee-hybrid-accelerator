#!/bin/bash

# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
