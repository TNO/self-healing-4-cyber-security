ROOT_DIRECTORY="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

function deploy_pod() {
  cd "${ROOT_DIRECTORY}"/deployment/pod-deployment || false
  bash deploy.sh
}

function deploy_host() {
  cd "${ROOT_DIRECTORY}"/deployment/host-deployment || false
  bash deploy.sh
}

function show_k8s() {
  echo "Deployed pods"
  kubectl get pods

  echo "Deployed services"
  kubectl get svc
}

deploy_host || exit
deploy_pod || exit

echo "Finished deploying self healing proof of concept"
show_k8s
