#!/usr/bin/env python3

# Copyright 2022 Google LLC
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

import argparse
import collections
import json
import sys

import requests


class Apigee:
    def __init__(
        self,
        apigee_type="x",
        base_url="https://apigee.googleapis.com/v1",
        auth_type="oauth",
        org="validate",
        access_token='',
    ):
        self.org = org
        self.baseurl = f"{base_url}/organizations/{org}"
        self.apigee_type = apigee_type
        self.auth_type = auth_type
        access_token = self.get_access_token(access_token)
        self.auth_header = {
            "Authorization": "Bearer {}".format(access_token)
            if self.auth_type == "oauth"
            else "Basic {}".format(access_token)  # noqa
        }

    def get_token_user(self, token):
        url = f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={token}"  # noqa
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['email']
        return ''

    def is_token_valid(self, token):
        url = f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={token}"  # noqa
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Token Validated for user {response.json()['email']}")
            return True
        return False

    def get_access_token(self, access_token):
        token = access_token
        if token is not None:
            if self.apigee_type == "x":
                if self.is_token_valid(token):
                    return token
                else:
                    print(
                        'please run "export APIGEE_ACCESS_TOKEN=$(gcloud auth print-access-token)" first !! '  # noqa pylint: disable=line-too-long
                    )
                    sys.exit(1)
            else:
                return token
        else:
            if self.apigee_type == "x":
                print(
                    'please run "export APIGEE_ACCESS_TOKEN=$(gcloud auth print-access-token)" first !! '  # noqa pylint: disable=line-too-long
                )
            else:
                print("please export APIGEE_OPDK_ACCESS_TOKEN")
            sys.exit(1)

    def set_auth_header(self):
        access_token = self.get_access_token()
        self.auth_header = {
            "Authorization": "Bearer {}".format(access_token)
            if self.auth_type == "oauth"
            else "Basic {}".format(access_token)
        }

    def get_org(self):
        url = f"{self.baseurl}"
        headers = self.auth_header.copy()
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False

    def get_environment(self, env):
        url = f"{self.baseurl}/environments/{env}"
        headers = self.auth_header.copy()
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False

    def get_env_group(self, env_group):
        url = f"{self.baseurl}/envgroups/{env_group}"
        headers = self.auth_header.copy()
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, None


def compare_lists(l1, l2):
    if collections.Counter(l1) == collections.Counter(l2):
        return True
    else:
        return False


def main():
    parser = argparse.ArgumentParser(description='Validates Apigee Objects')
    parser.add_argument('--input_data', help='Apigee Input data')
    parser.add_argument('--access_token', help='GCP OAuth Access Token')
    args = parser.parse_args()
    input_data = json.loads(args.input_data)
    apigee_org = input_data['gcp']['projectID']
    apigee_envs = input_data['envs']
    apigee_vhosts = input_data['virtualhosts']
    TargetApigee = Apigee(
        "x",
        "https://apigee.googleapis.com/v1",
        "oauth",
        apigee_org,
        args.access_token,
    )
    validations = []
    authenticated_user = TargetApigee.get_token_user(args.access_token)
    if not TargetApigee.get_org():
        validations.append(f"Apigee Organization : {apigee_org} doesnt exist OR user {authenticated_user} doesnt have permissions ")  # noqa pylint: disable=line-too-long

    for apigee_env in apigee_envs:
        if not TargetApigee.get_environment(apigee_env['name']):
            validations.append(f"Apigee Environment : {apigee_env['name']} doesnt exist OR user {authenticated_user} doesnt have permissions ")  # noqa pylint: disable=line-too-long

    for apigee_vhost in apigee_vhosts:
        apigee_vhost_status, apigee_vhost_info = TargetApigee.get_env_group(apigee_vhost['name'])  # noqa pylint: disable=line-too-long
        if not apigee_vhost_status:
            validations.append(f"Apigee Environment Group : {apigee_vhost['name']} doesnt exist OR user {authenticated_user} doesnt have permissions ")  # noqa pylint: disable=line-too-long

        if apigee_vhost_status:
            apigee_vhost_hostname = apigee_vhost.get('hostnames', [])
            apigee_vhost_info_hostname = apigee_vhost_info.get('hostnames', []) # noqa pylint: disable=line-too-long
            if not compare_lists(apigee_vhost_hostname, apigee_vhost_info_hostname):  # noqa pylint: disable=line-too-long
                validations.append(f"Apigee Environmrnt Group {apigee_vhost['name']} hostnames {apigee_vhost_hostname} dont match the hostnames in Apigee Management API: {apigee_vhost_info_hostname}")  # noqa pylint: disable=line-too-long

    if len(validations) > 0:
        print('Validation Errors found !')
        print("\n".join(validations))
        sys.exit(1)
    print('Apigee Control plane validations successfull')


if __name__ == '__main__':
    main()
