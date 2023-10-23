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

import os
import sys
import requests
from time import sleep
import argparse


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
                        'please run "export APIGEE_ACCESS_TOKEN=$(gcloud auth print-access-token)" first !! '  # noqa type: ignore
                    )
                    sys.exit(1)
            else:
                return token
        else:
            if self.apigee_type == "x":
                print(
                    'please run "export APIGEE_ACCESS_TOKEN=$(gcloud auth print-access-token)" first !! '  # noqa
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

    def get_api(self, api_name):
        url = f"{self.baseurl}/apis/{api_name}"
        headers = self.auth_header.copy()
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            revision = response.json().get('revision', ['1'])
            return True, revision
        else:
            return False, None

    def create_api(self, api_name, proxy_bundle_path):
        url = f"{self.baseurl}/apis?action=import&name={api_name}&validate=true"  # noqa
        proxy_bundle_name = os.path.basename(proxy_bundle_path)
        files = [
            (
                "data",
                (proxy_bundle_name, open(proxy_bundle_path, "rb"), "application/zip"),  # noqa
            )
        ]
        headers = self.auth_header.copy()
        response = requests.request(
            "POST", url, headers=headers, data={}, files=files
        )
        if response.status_code == 200:
            revision = response.json().get('revision', "1")
            return True, revision
        print(response.text)
        return False, None

    def get_api_revisions_deployment(self, env, api_name, api_rev):  # noqa
        url = (
            url
        ) = f"{self.baseurl}/environments/{env}/apis/{api_name}/revisions/{api_rev}/deployments"  # noqa
        headers = self.auth_header.copy()
        response = requests.request("GET", url, headers=headers, data={})
        if response.status_code == 200:
            resp = response.json()
            api_deployment_status = resp.get("state", "")
            if self.apigee_type == "x":
                if api_deployment_status == "READY":
                    return True
            if self.apigee_type == "opdk":
                if api_deployment_status == "deployed":
                    return True
            print(f"API {api_name} is in Status: {api_deployment_status} !")  # noqa
            return False
        else:
            print(response.text)
            return False

    def deploy_api(self, env, api_name, api_rev):
        url = (
            url
        ) = f"{self.baseurl}/environments/{env}/apis/{api_name}/revisions/{api_rev}/deployments?override=true"  # noqa
        headers = self.auth_header.copy()
        response = requests.request("POST", url, headers=headers, data={})
        if response.status_code == 200:
            return True
        else:
            resp = response.json()
            if "already deployed" in resp["error"]["message"]:
                print("Proxy {} is already Deployed".format(api_name))
                return True
            print(response.text)
            return False

    def deploy_api_bundle(self, env, api_name, proxy_bundle_path, api_force_redeploy=False):  # noqa
        api_deployment_retry = 60
        api_deployment_sleep = 5
        api_deployment_retry_count = 0
        api_exists = False
        get_api_status, api_revs = self.get_api(api_name)
        if get_api_status:
            api_exists = True
            api_rev = api_revs[-1]
            print(
                f"Proxy with name {api_name} with revision {api_rev} already exists in Apigee Org {self.org}"  # noqa
            )
            if api_force_redeploy:
                api_exists = False
        if not api_exists:
            api_created, api_rev = self.create_api(api_name, proxy_bundle_path)
            if api_created:
                print(
                    f"Proxy has been imported with name {api_name} in Apigee Org {self.org}"  # noqa
                )
                api_exists = True
            else:
                print(f"ERROR : Proxy {api_name} import failed !!! ")
                return False
        if api_exists:
            if self.get_api_revisions_deployment(
                        env, api_name, api_rev
                    ):
                print(f"INFO : Proxy {api_name} already active in to {env} in Apigee Org {self.org} !")  # noqa
                return True
            else:
                if self.deploy_api(env, api_name, api_rev):
                    print(
                        f"Proxy with name {api_name} has been deployed  to {env} in Apigee Org {self.org}"  # noqa
                    )
                    while api_deployment_retry_count < api_deployment_retry:
                        if self.get_api_revisions_deployment(
                            env, api_name, api_rev
                        ):
                            print(
                                f"Proxy {api_name} active in runtime after {api_deployment_retry_count*api_deployment_sleep} seconds "  # noqa
                            )
                            return True
                        else:
                            print(
                                f"Checking API deployment status in {api_deployment_sleep} seconds"  # noqa
                            )
                            sleep(api_deployment_sleep)
                            api_deployment_retry_count += 1
                else:
                    print(
                        f"ERROR : Proxy deployment  to {env} in Apigee Org {self.org} Failed !!"  # noqa
                    )
                    return False

    def list_apis(self, api_type):
        url = f"{self.baseurl}/{api_type}"
        headers = self.auth_header.copy()
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            if self.apigee_type == "x":
                if len(response.json()) == 0:
                    return []
                return [
                    p["name"]
                    for p in response.json()[
                        "proxies" if api_type == "apis" else "sharedFlows"
                    ]
                ]  # noqa
            return response.json()
        else:
            return []

    def list_api_revisions(self, api_type, api_name):
        url = f"{self.baseurl}/{api_type}/{api_name}/revisions"
        headers = self.auth_header.copy()
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return []

    def fetch_api_revision(self, api_type, api_name, revision, export_dir):  # noqa
        url = f"{self.baseurl}/{api_type}/{api_name}/revisions/{revision}?format=bundle"  # noqa
        headers = self.auth_header.copy()
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            self.write_proxy_bundle(export_dir, api_name, response.raw)
            return True
        return False


def main():
    parser = argparse.ArgumentParser(description='Deploy Apigee API proxy bundle')  # noqa
    parser.add_argument('--project_id', help='GCP Project ID')
    parser.add_argument('--env', help='Apigee Environment Name')
    parser.add_argument('--api_name', help='Apigee API Name')
    parser.add_argument('--api_bundle_path', help='Apigee API Proxy bundle path')  # noqa
    parser.add_argument('--access_token', help='GCP OAuth Access Token')
    parser.add_argument('--api_redeploy', help='Redploy API',action="store_true")  # noqa
    args = parser.parse_args()
    TargetApigee = Apigee(
        "x",
        "https://apigee.googleapis.com/v1",
        "oauth",
        args.project_id,
        args.access_token,
    )
    if not TargetApigee.deploy_api_bundle(
        args.env,
        args.api_name,
        args.api_bundle_path,
        args.api_redeploy
    ):
        print(f"Proxy: {args.api_name} deployment failed.")
        sys.exit(1)


if __name__ == '__main__':
    main()
