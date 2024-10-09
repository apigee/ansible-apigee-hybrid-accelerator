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
import os
import sys
from time import sleep
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
        self.auth_header = self._generate_auth_header(access_token)

    def _generate_auth_header(self, access_token):
        token = self.get_access_token(access_token)
        return {
            "Authorization": f"Bearer {token}" if self.auth_type == "oauth" else f"Basic {token}"
        }

    def is_token_valid(self, token):
        url = f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={token}"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Token Validated for user {response.json()['email']}")
            return True
        return False

    def get_access_token(self, access_token):
        if access_token and self.is_token_valid(access_token):
            return access_token
        print('Please run "export APIGEE_ACCESS_TOKEN=$(gcloud auth print-access-token)" first !!')
        sys.exit(1)

    def get_api(self, api_name):
        url = f"{self.baseurl}/apis/{api_name}"
        response = requests.get(url, headers=self.auth_header)
        if response.status_code == 200:
            revision = response.json().get('revision', ['1'])
            return True, revision
        return False, None

    def create_api(self, api_name, proxy_bundle_path):
        url = f"{self.baseurl}/apis?action=import&name={api_name}&validate=true"
        proxy_bundle_name = os.path.basename(proxy_bundle_path)
        with open(proxy_bundle_path, "rb") as proxy_bundle_file:
            files = [("data", (proxy_bundle_name, proxy_bundle_file, "application/zip"))]
            response = requests.post(url, headers=self.auth_header, files=files)
        if response.status_code == 200:
            revision = response.json().get('revision', "1")
            return True, revision
        print(response.text)
        return False, None

    def get_api_revisions_deployment(self, env, api_name, api_rev):
        url = f"{self.baseurl}/environments/{env}/apis/{api_name}/revisions/{api_rev}/deployments"
        response = requests.get(url, headers=self.auth_header)
        if response.status_code == 200:
            api_deployment_status = response.json().get("state", "")
            if (self.apigee_type == "x" and api_deployment_status == "READY") or \
               (self.apigee_type == "opdk" and api_deployment_status == "deployed"):
                return True
            print(f"API {api_name} is in Status: {api_deployment_status} !")
        else:
            print(response.text)
        return False

    def deploy_api(self, env, api_name, api_rev):
        url = f"{self.baseurl}/environments/{env}/apis/{api_name}/revisions/{api_rev}/deployments?override=true"
        response = requests.post(url, headers=self.auth_header)
        if response.status_code == 200:
            return True
        if "already deployed" in response.json().get("error", {}).get("message", ""):
            print(f"Proxy {api_name} is already Deployed")
            return True
        print(response.text)
        return False

    def deploy_api_bundle(self, env, api_name, proxy_bundle_path, api_force_redeploy=False):
        api_deployment_retry = 60
        api_deployment_sleep = 5
        api_deployment_retry_count = 0

        get_api_status, api_revs = self.get_api(api_name)
        api_rev = api_revs[-1] if get_api_status else None

        if get_api_status:
            print(f"Proxy with name {api_name} with revision {api_rev} already exists in Apigee Org {self.org}")
            if api_force_redeploy:
                api_rev = None

        if not api_rev:
            api_created, api_rev = self.create_api(api_name, proxy_bundle_path)
            if not api_created:
                print(f"ERROR : Proxy {api_name} import failed !!!")
                return False
            print(f"Proxy has been imported with name {api_name} in Apigee Org {self.org}")

        if self.get_api_revisions_deployment(env, api_name, api_rev):
            print(f"INFO : Proxy {api_name} already active in {env} in Apigee Org {self.org}!")
            return True

        if self.deploy_api(env, api_name, api_rev):
            print(f"Proxy with name {api_name} has been deployed to {env} in Apigee Org {self.org}")
            while api_deployment_retry_count < api_deployment_retry:
                if self.get_api_revisions_deployment(env, api_name, api_rev):
                    print(f"Proxy {api_name} active in runtime after {api_deployment_retry_count * api_deployment_sleep} seconds")
                    return True
                print(f"Checking API deployment status in {api_deployment_sleep} seconds")
                sleep(api_deployment_sleep)
                api_deployment_retry_count += 1
        print(f"ERROR : Proxy deployment to {env} in Apigee Org {self.org} Failed !!")
        return False

    def list_apis(self, api_type):
        url = f"{self.baseurl}/{api_type}"
        response = requests.get(url, headers=self.auth_header)
        if response.status_code == 200:
            if self.apigee_type == "x":
                proxies = response.json().get("proxies" if api_type == "apis" else "sharedFlows", [])
                return [p["name"] for p in proxies]
            return response.json()
        return []

    def list_api_revisions(self, api_type, api_name):
        url = f"{self.baseurl}/{api_type}/{api_name}/revisions"
        response = requests.get(url, headers=self.auth_header)
        if response.status_code == 200:
            return response.json()
        return []

    def fetch_api_revision(self, api_type, api_name, revision, export_dir):
        url = f"{self.baseurl}/{api_type}/{api_name}/revisions/{revision}?format=bundle"
        response = requests.get(url, headers=self.auth_header, stream=True)
        if response.status_code == 200:
            self.write_proxy_bundle(export_dir, api_name, response.raw)
            return True
        return False


def main():
    parser = argparse.ArgumentParser(description='Deploy Apigee API proxy bundle')
    parser.add_argument('--project_id', help='GCP Project ID')
    parser.add_argument('--env', help='Apigee Environment Name')
    parser.add_argument('--api_name', help='Apigee API Name')
    parser.add_argument('--api_bundle_path', help='Apigee API Proxy bundle path')
    parser.add_argument('--access_token', help='GCP OAuth Access Token')
    parser.add_argument('--api_redeploy', help='Redploy API', action="store_true")
    args = parser.parse_args()

    target_apigee = Apigee(
        "x",
        "https://apigee.googleapis.com/v1",
        "oauth",
        args.project_id,
        args.access_token,
    )

    if not target_apigee.deploy_api_bundle(
        args.env,
        args.api_name,
        args.api_bundle_path,
        args.api_redeploy
    ):
        print(f"Proxy: {args.api_name} deployment failed.")
        sys.exit(1)


if __name__ == '__main__':
    main()