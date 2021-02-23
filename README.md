This repository features all the software developed for the self-healing proof-of-concept. Below you can find information on each component and where it is located in the directory structure

# Directory structure
## Components
### Attacker brute force
Sample application that can be used to perform a DoS attack on the [Authentication-bastion](components/web-application/authentication-bastion).

### host-components
#### [HDDP](components/host-components/hddp)
Single point of access to the underlying docker daemon of a host. Used by the lymphocyte to obtain information on running containers and their status.

#### [Syslog-ng](components/host-components/syslog-ng)
Syslog server used by Falco to deliver a log stream. 

#### [Falco](components/host-components/falco)
Pinned version of Falco, used for anomaly detection using eBPF. 

### Pod  Components
#### [Channel Frequency Monitor](components/pod-components/redis-channel-monitor)
Small application that counts the amount of events added in a redis pub/sub channel.
If a certain treshold of messages over minute is exceeded, a message is published on another pub/sub channel.

#### [Lymphocyte](components/pod-components/lymphocyte)
In the PoC setup a lymphocyte is a python docker container that runs together with a job container in a kubernetes pod. The lymphocyte container is inspired by T Killer cells. It decides if and when to send to the Docker Proxy the signal to kill (or pause or restart) the job container.

### Shared
Python library code used by multiple components in the proof of concept.

### Web application
#### [Authentication-bastion](components/web-application/authentication-bastion)
Sample authentication service that can provide tokens and validation of tokens for other services.

#### [Vulnerable php container](components/web-application/vulnerable-php-container)
PHP server that is exploitable to remote code execution. Is not accessed directly but through the [nginx-frontend](components/web-application/nginx-frontend)

#### [NGINX frontend](components/web-application/nginx-frontend)
Web proxy that handles traffic towards [Authentication-bastion](components/web-application/authentication-bastion) and [Vulnerable php container](components/web-application/vulnerable-php-container)

## Deployments
### Host-deployment
Contains descriptors and docker-compose files to start the HDDP, Falco, Mongo and syslog on the host

### Pod-deployment
Contains descriptors to start the self-healing pod, featuring the lymphocyte, frequency monitor, nginx, php, authentication bastion.

## Reports
Features an overview per software component with ran (security) scans and their results for each component listed under `components`

# Usage
Prepare `kubernetes` on a host somewhere, according to normal procedures. `Docker` and `docker-compose` also need to be installed
Build components using `bash build_components.sh`

## PoC
You can either start the components manually yourself by following below options, or run `bash deploy.sh` in the root folder. 

### Host components
Enter [deployment/host-deployment](deployment/host-deployment), run `bash deploy.sh`

This will start the HDDP, Falco, Mongo and Syslog

### Self healing pod
After this is done, go into  [deployment/pod-deployment](deployment/pod-deployment)

Start the deployment `bash deploy.sh`

Show the logs of lymphcyte using ` kubelctl logs <lymphocyte> -f`


### Triggering external anomaly
```
docker exec -it <php-container> bash
touch /dev
```

### Triggering internal anomaly
Run a random container with bash in k8s
```
 kubectl run -it --image debian:latest debian-bash
```

Attach to it, e.g.:
``` 
docker exec -it <k8s-debian-container> bash
```

Send login attempts with bad password, 10+ times:
```
curl -k -X POST  https://nginx:443/api/v1/user/login -H  "accept: application/json" --data 'username=sample_username&password=xyz'
```