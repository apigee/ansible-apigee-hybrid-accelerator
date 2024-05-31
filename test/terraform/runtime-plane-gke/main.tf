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

module "gke" {
  source                     = "terraform-google-modules/kubernetes-engine/google//modules/beta-private-cluster-update-variant"
  version                    = "31.0.0"
  project_id                 = var.project_id
  name                       = var.cluster_name
  region                     = var.region
  zones                      = var.zones
  network                    = var.network
  subnetwork                 = var.subnetwork
  ip_range_pods              = var.ip_range_pods
  ip_range_services          = var.ip_range_services
  http_load_balancing        = false
  network_policy             = false
  horizontal_pod_autoscaling = true
  filestore_csi_driver       = false
  enable_private_endpoint    = true
  enable_private_nodes       = true
  master_ipv4_cidr_block     = var.master_ipv4_cidr_block
  istio                      = false
  cloudrun                   = false
  dns_cache                  = false
  remove_default_node_pool   = true
  service_account_name       = var.service_account_name
  node_pools                 = var.node_pools
  cluster_resource_labels    = var.cluster_resource_labels
  master_authorized_networks = var.master_authorized_networks
  kubernetes_version         = var.kubernetes_version
  node_pools_oauth_scopes = {
    all = [
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]
  }
  node_pools_labels   = var.node_pools_labels
  node_pools_metadata = {}
  node_pools_taints   = {}
  node_pools_tags     = var.node_pools_tags
}