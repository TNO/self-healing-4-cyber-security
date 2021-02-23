 docker pull falcosecurity/falco:latest
docker run --rm -i -t \
    --privileged \
    -e FALCO_BPF_PROBE="" \
    -v /dev:/host/dev \
    -v /proc:/host/proc:ro \
    -v /boot:/host/boot:ro \
    -v /lib/modules:/host/lib/modules:ro \
    -v /usr:/host/usr:ro \
    -v /etc:/host/etc:ro \
    -v /home/ubuntu/detector/falco_docker/falco:/etc/falco \
    falcosecurity/falco:latest
