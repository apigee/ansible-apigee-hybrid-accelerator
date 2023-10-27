/**
 * Copyright 2021 Google LLC
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

variable "project_id" {
  description = "Project id (also used for the Apigee Organization)."
  type        = string
}

variable "deployment_environment" {
  description = "Apigee Deployment Env. prod OR non-prod"
  type        = string
  default     = "prod"
}
variable "org_display_name" {
  description = "Apigee org display name"
  type        = string
  default     = null
}

variable "org_description" {
  description = "Apigee org description"
  type        = string
  default     = "Apigee org created in TF"
}

variable "ax_region" {
  description = "GCP region for storing Apigee analytics data (see https://cloud.google.com/apigee/docs/api-platform/get-started/install-cli)."
  type        = string
}

variable "apigee_envgroups" {
  description = "Apigee Environment Groups."
  type        = map(list(string))
  default     = {}
}

variable "apigee_environments" {
  description = "Apigee Environments."
  type = map(object({
    display_name = optional(string)
    description  = optional(string)
    node_config = optional(object({
      min_node_count = optional(number)
      max_node_count = optional(number)
    }))
    iam       = optional(map(list(string)))
    envgroups = list(string)
  }))
  default = null
}


variable "service_accounts_map" {
  description = "Apigee Hybrid Service Accounts."
  type        = map(list(string))
  default = {
    "apigee-cassandra"    = ["roles/storage.objectAdmin"],
    "apigee-logger"       = ["roles/logging.logWriter"],
    "apigee-mart"         = ["roles/apigeeconnect.Agent"],
    "apigee-metrics"      = ["roles/monitoring.metricWriter"],
    "apigee-runtime"      = [],
    "apigee-synchronizer" = ["roles/apigee.synchronizerManager"],
    "apigee-udca"         = ["roles/apigee.analyticsAgent"],
    "apigee-watcher" : ["roles/apigee.runtimeAgent"]
  }
}
