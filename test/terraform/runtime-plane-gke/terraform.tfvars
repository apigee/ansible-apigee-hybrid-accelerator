/**
 * Copyright 2023 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

project_id             = "_GCP_PROJECT_ID_"
cluster_name           = "apigee-hybrid-cicd-test"
region                 = "_GCP_REGION_"
network                = "default"
subnetwork             = "default"
ip_range_pods          = "pods"
ip_range_services      = "svc"
service_account_name   = "apigee-gke-svc-account"
kubernetes_version     = "1.26.7-gke.500"
master_ipv4_cidr_block = "10.220.0.0/28"
master_authorized_networks = [
  { cidr_block = "10.132.0.0/20", display_name = "europe-west1-subnet" },
  { cidr_block = "172.17.0.0/16", display_name = "docker-gh-runner" },
]

cluster_resource_labels = {
  "env" = "apigee-hybrid-cicd"
}

node_pools = [
  {
    name         = "runtime-nodepool"
    machine_type = "e2-standard-8"
    min_count    = 1
    max_count    = 2
    disk_size_gb = 100
    disk_type    = "pd-standard"
    auto_upgrade = true
    auto_repair  = false
  },
  {
    name         = "data-nodepool"
    machine_type = "e2-standard-8"
    min_count    = 1
    max_count    = 1
    disk_size_gb = 100
    disk_type    = "pd-standard"
    auto_upgrade = true
    auto_repair  = false
  },
]

node_pools_labels = {
  runtime-nodepool = {
    "apigee-nodepool" = "apigee-runtime"
  },
  data-nodepool = {
    "apigee-nodepool" = "apigee-data"
  },
}

node_pools_tags = {
  all = [
    "apigee-hybrid-ext"
  ]
}
