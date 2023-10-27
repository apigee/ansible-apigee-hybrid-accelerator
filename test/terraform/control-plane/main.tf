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


locals {
  service_accounts = (
    var.deployment_environment == "prod" ?
    var.service_accounts_map : { "apigee-non-prod" : [for k, v in var.service_accounts_map : v[0] if length(v) > 0] }
  )
}

module "service_accounts" {
  for_each   = local.service_accounts
  source     = "terraform-google-modules/service-accounts/google"
  project_id = var.project_id
  prefix     = ""
  names      = [each.key]
  # generate_keys = true
  display_name = "${each.key} Service Account"
  description  = "${each.key} Account"
  project_roles = [
    for k, v in each.value :
    "${var.project_id}=>${v}"
  ]
}


module "apigee" {
  source     = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/apigee?ref=v27.0.0"
  project_id = var.project_id
  organization = {
    display_name     = var.org_display_name
    description      = var.org_description
    runtime_type     = "HYBRID"
    analytics_region = var.ax_region
  }
  envgroups    = var.apigee_envgroups
  environments = var.apigee_environments
}
