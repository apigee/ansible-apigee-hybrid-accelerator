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

DATE_EPOCH=$(date +%s)
CONTAINER_NAME="ansible-run-${DATE_EPOCH}"

docker run --name "${CONTAINER_NAME}"\
    -v "$ANSIBLE_DIR:/app" \
    -v "$GOOGLE_APPLICATION_CREDENTIALS:/svc_account/account.json" \
    -e GOOGLE_APPLICATION_CREDENTIALS=/svc_account/account.json \
    "$GCP_REGION-docker.pkg.dev/$GCP_PROJECT_ID/$GCP_GAR_REPO/ansible-helm-apigee-hybrid-deployer:latest" \
    /bin/bash -c "cd /app; \
      PIPELINE_STATUS=\"success\"; \
      mkdir -p /tmp/setup; echo \"started\" > /tmp/setup/start.log; \
      gcloud auth login --cred-file=/svc_account/account.json; \
      gcloud container clusters get-credentials apigee-hybrid-cicd-test --region $GCP_REGION --project $GCP_PROJECT_ID; \
      ansible-playbook playbook.yaml --tags 'dc1' -e @vars/test.yaml"

CONTAINER_EXIT_CODE=$(docker inspect "$CONTAINER_NAME" --format='{{.State.ExitCode}}')
if [ "$CONTAINER_EXIT_CODE" -ne 0 ]; then
  LOG_DUMP=$(mktemp -d)
  docker cp "$CONTAINER_NAME:/tmp/setup" "$LOG_DUMP"
  gsutil -m cp -r "$LOG_DUMP" "gs://$TF_BACKEND_BUCKET/ansible_run_log/$GIT_COMMIT_SHORT_ID"
  exit 1
fi
