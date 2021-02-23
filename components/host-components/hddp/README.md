# SH4CS Docker proxy
This project provides an API meant to be consumer by containers that allows them to stop, pause, kill a container on demand.

You can use the docker-proxy locally by running `docker-compose up`. This will build and then run the container.

After you have built the container once, to update the image run `docker-compose build`

Or, together: `docker-compose up --build`

# Setup
## [Configuring Docker](https://blog.usejournal.com/how-to-enable-docker-remote-api-on-docker-host-7b73bd3278c6?gi=38e6d5534419)
This proxy depends on the Docker API being available. For this to take effect, modify the following file `/lib/systemd/system/docker.service`
Add `-H=tcp://0.0.0.0:2375` to the ExecStart line

Apply changes by running below:
```
sudo systemctl daemon-reload
sudo systemctl restart docker
```

# Usage
## Generated documentation
The server features automatically generated Swagger documentation.
When you visit `/` endpoint you will be automatically redirected to the documentation page.
You can view this while the server is running at http://<server_ip>/api/v1/doc/

## Endpoints
All /docker/ endpoints need a `container_identifier`, see below examples

* /api/v1/docker/kill
    * `curl -X POST "http://<server_ip>/api/v1/docker/kill?container_identifier=abc" -H  "accept: application/json"`
* /api/v1/docker/pause
    * `curl -X POST "http://<server_ip>/api/v1/docker/pause?container_identifier=abc" -H  "accept: application/json"`
* /api/v1/docker/remove
    * `curl -X POST "http://<server_ip>/api/v1/docker/remove?container_identifier=abc" -H  "accept: application/json"`
* /api/v1/docker/stop
    * `curl -X POST "http://<server_ip>/api/v1/docker/stop?container_identifier=abc" -H  "accept: application/json"`
* /api/v1/docker/uptime
    * `curl -X POST "http://<server_ip>/api/v1/docker/uptime?container_identifier=abc" -H  "accept: application/json"`
* /api/v1/docker/status
    * `curl -X POST "http://<server_ip>/api/v1/docker/status?container_identifier=abc" -H  "accept: application/json"`

## Configuration
The HDDP needs the address it can reach the docker daemon on. This is provided by the `DOCKER_HOST` variable. This is set in the `Dockerfile`, which means it can be overwritten, e.g. by the docker-compose file.

