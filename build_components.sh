ROOT_DIRECTORY="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

ATTACKER_IMAGE="ci.tno.nl/self-healing/attacker-brute-force:master"
PYTHON_SHARED_COMMON="ci.tno.nl/self-healing/common/python:master"

HDDP_IMAGE="ci.tno.nl/self-healing/host/hddp:master"
SYSLOG_IMAGE="ci.tno.nl/self-healing/host/syslog-ng:master"
FALCO_IMAGE="ci.tno.nl/self-healing/host/falco:master"

CHANNEL_MONITOR_IMAGE="ci.tno.nl/self-healing/pod/channel-frequency-monitor:master"
LYMPHOCYTE_IMAGE="ci.tno.nl/self-healing/pod/lymphocyte:master"

BASTION_IMAGE="ci.tno.nl/self-healing/web-application/authentication-bastion:master"
PHP_IMAGE="ci.tno.nl/self-healing/web-application/vulnerable-php-container:master"
NGINX_IMAGE="ci.tno.nl/self-healing/web-application/nginx-frontend:master"

function build_attacker() {
  cd "${ROOT_DIRECTORY}"/components/attacker-brute-force || false
  docker build -t ${ATTACKER_IMAGE} .
}

function build_python_shared() {
  cd "${ROOT_DIRECTORY}"/components/shared || false
  docker build -t ${PYTHON_SHARED_COMMON} .
}

function build_hddp() {
  cd "${ROOT_DIRECTORY}"/components/host-components/hddp || false
  docker build -t ${HDDP_IMAGE} .
}

function build_syslog_ng() {
  cd "${ROOT_DIRECTORY}"/components/host-components/syslog-ng || false
  docker build -t ${SYSLOG_IMAGE} .
}

function build_falco() {
  cd "${ROOT_DIRECTORY}"/components/host-components/falco || false
  docker build -t ${FALCO_IMAGE} .
}

function build_redis_channel_monitor() {
  cd "${ROOT_DIRECTORY}"/components/pod-components/redis-channel-monitor || false
  docker build -t ${CHANNEL_MONITOR_IMAGE} .
}

function build_lymphocyte() {
  cd "${ROOT_DIRECTORY}"/components/pod-components/lymphocyte || false
  docker build -t ${LYMPHOCYTE_IMAGE} .
}

function build_authentication_bastion() {
  cd "${ROOT_DIRECTORY}"/components/web-application/authentication_bastion || false
  docker build -t ${BASTION_IMAGE} .
}

function build_php_image() {
  cd "${ROOT_DIRECTORY}"/components/web-application/vulnerable-php-container || false
  docker build -t ${PHP_IMAGE} .
}

function build_nginx_frontend() {
  cd "${ROOT_DIRECTORY}"/components/web-application/nginx-frontend || false
  docker build -t ${NGINX_IMAGE} .
}

# Build attacker component
build_attacker || exit

# Build shared component
build_python_shared || exit

# Build host components
build_hddp || exit
build_syslog_ng || exit
build_falco || exit

# Build pod components
build_redis_channel_monitor || exit
build_lymphocyte || exit

# Build web application components
build_authentication_bastion || exit
build_php_image || exit
build_nginx_frontend || exit
