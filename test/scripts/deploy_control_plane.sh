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

TF_DIR="${1}"

cd "$TF_DIR" || exit

# Function to replace a string from a file
function replace_string() {
  # Get the search and replacement strings from the user
  input_file="$1"
  search_string="$2"
  replacement_string="$3"
  # Replace the string in the file
  sed -i "s/$search_string/$replacement_string/g" "$input_file"

}

replace_string "backend.tf" "_TF_BACKEND_BUCKET_" "${TF_BACKEND_BUCKET}"
replace_string "terraform.tfvars" "_GCP_PROJECT_ID_" "${GCP_PROJECT_ID}"
replace_string "terraform.tfvars" "_GCP_REGION_" "${GCP_REGION}"


terraform init -upgrade
terraform plan
terraform apply -auto-approve
