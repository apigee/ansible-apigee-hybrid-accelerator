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

set -x
ANSIBLE_DIR="${1}"
GIT_COMMIT_SHORT_ID="$2"
cd "$ANSIBLE_DIR" || exit

# Function to replace a string from a file
function replace_string() {
  # Get the search and replacement strings from the user
  input_file="$1"
  search_string="$2"
  replacement_string="$3"
  # Replace the string in the file
  sed -i "s/$search_string/$replacement_string/g" "$input_file"
}

replace_string "$ANSIBLE_DIR/vars/test.yaml" "_GCP_PROJECT_ID_" "${GCP_PROJECT_ID}"
replace_string "$ANSIBLE_DIR/vars/test.yaml" "_GCP_REGION_" "${GCP_REGION}"

docker run -v "$ANSIBLE_DIR:/app" \
    -v "$GOOGLE_APPLICATION_CREDENTIALS:/svc_account/account.json" \
    -e GOOGLE_APPLICATION_CREDENTIALS=/svc_account/account.json \
    "$GCP_REGION-docker.pkg.dev/$GCP_PROJECT_ID/$GCP_GAR_REPO/ansible-helm-apigee-hybrid-deployer:$GIT_COMMIT_SHORT_ID" \
    /bin/bash -c "cd /app; PLAYBOOK_STATUS=\"success\";\
      gcloud auth login --cred-file=/svc_account/account.json; \
      gcloud container clusters get-credentials apigee-hybrid-cicd-test --region $GCP_REGION --project $GCP_PROJECT_ID; \
      ansible-playbook playbook.yaml --tags 'dc1' -e @vars/test.yaml || PLAYBOOK_STATUS=\"fail\"; \
      gsutil cp -q -r /tmp/setup gs://$TF_BACKEND_BUCKET/ansible_run_log/$(date +%s) && \
      [[ \"$PLAYBOOK_STATUS\" = 'fail' ]] && exit 1"