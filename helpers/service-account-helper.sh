#!/bin/bash

NAMESPACE="apigee"
PROJECT_ID="$1" || exit 1
SVC_DIR="${2:-SERVICE_ACCOUNT_DIR}"

kubectl create ns "$NAMESPACE" 

SUPPORTED_PROFILES=("apigee-logger" "apigee-metrics" "apigee-cassandra" "apigee-udca" "apigee-synchronizer" "apigee-mart" "apigee-watcher" "apigee-runtime")
echo "---"
for PROF in "${SUPPORTED_PROFILES[@]}"; do
    SA_NAME="$PROJECT_ID-$PROF.json"
    kubectl create secret \
        generic $PROF-custom-secret \
        -n "$NAMESPACE" \
        --from-file=client_secret.json="$SVC_DIR/$SA_NAME" \
        --dry-run=client \
        -o yaml
    echo "---"
done
