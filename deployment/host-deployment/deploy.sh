#!/bin/bash
set -x

function deploy_hddp() {
  bash hddp/deploy.sh
}

function deploy_mongo() {
  bash mongodb/build-images.sh
  bash mongodb/deploy.sh
  sleep 20 # wait for mongo to finish, takes like 20 seconds
}

function deploy_falco_and_syslog() {
  docker-compose up -d --force-recreate --remove-orphans
}

deploy_hddp
deploy_mongo
deploy_falco_and_syslog
