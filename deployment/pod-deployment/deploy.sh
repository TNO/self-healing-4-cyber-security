#!/bin/bash

set -x

function apply_descriptors() {
  kubectl apply -f descriptors/redis-deployment.yaml
  kubectl apply -f descriptors/redis-service.yaml

  kubectl apply -f descriptors/php-deployment.yaml
  kubectl apply -f descriptors/php-service.yaml

  kubectl apply -f descriptors/frequency-monitor-deployment.yaml

  kubectl apply -f descriptors/bastion-deployment.yaml
  kubectl apply -f descriptors/bastion-service.yaml

  kubectl apply -f descriptors/lymphocyte-deployment.yaml

  kubectl apply -f descriptors/nginx-deployment.yaml
  kubectl apply -f descriptors/nginx-service.yaml
}

function delete_pods() {
  local NAMES=("nginx" "channel-frequency-monitor" "bastion" "php" "lymphocyte" "redis")
  for name in "${NAMES[@]}"; do
    kubectl delete pods -l app="${name}" --grace-period=0 --force || true
  done
}

function delete_deployments() {
  local NAMES=("nginx-deployment" "channel-frequency-monitor-deployment" "bastion-deployment" "php-deployment" "lymphocyte-deployment" "redis-deployment")
  for name in "${NAMES[@]}"; do
    kubectl delete deployments "${name}" || true
  done
}

function delete_services() {
  local NAMES=("nginx" "bastion" "php" "redis")
  for name in "${NAMES[@]}"; do
    kubectl delete svc "${name}" || true
  done
}

delete_deployments &
delete_services &
wait

delete_pods

apply_descriptors
kubectl get pods
kubectl get svc
