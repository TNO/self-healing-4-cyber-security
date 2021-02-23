#!/bin/bash

set -x

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

function apply_pods() {
  kubectl apply -f "${SCRIPT_DIR}"/descriptors/
}

function delete_pods() {
  local NAMES=("mongo")
  for name in "${NAMES[@]}"; do
    kubectl delete pods -l app="${name}" --grace-period=0 --force || true
  done
}

function delete_deployments() {
  local NAMES=("mongo-deployment")
  for name in "${NAMES[@]}"; do
    kubectl delete deployments "${name}" || true
  done
}

function delete_services() {
  local NAMES=("mongo")
  for name in "${NAMES[@]}"; do
    kubectl delete svc "${name}" || true
  done
}

delete_deployments &
delete_services &
wait
delete_pods &
wait
apply_pods

kubectl get pods
kubectl get svc
