CI_URL="ci.tno.nl"

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

docker build -t  ${CI_URL}/self-healing/host/mongo:master -f "${SCRIPT_DIR}"/Dockerfile "${SCRIPT_DIR}"

#unable to prepare context: unable to evaluate symlinks in Dockerfile path: lstat /home/ubuntu/ssh-based-clone/host-components/Dockerfile: no such file or directory
