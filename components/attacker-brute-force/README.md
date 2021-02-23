# Docker based python brute force attacker
* `docker run ci.tno.nl/self-healing/attacker-brute-force:master` <params>
    * `docker run ci.tno.nl/self-healing/attacker-brute-force:master --ip <xXx> --port 80 --rps 10 --mode http`
To see the custom configuration options, check the [usage](##usage) section

## Usage
```
usage: brute_forcer.py [-h] [--rps RPS] --ip IP [--port PORT]
                       [--endpoint ENDPOINT] [--mode {ssh,http}]
                       [--username USERNAME]

optional arguments:
  -h, --help           show this help message and exit
  --rps RPS            Number of requests per second that will be fired at the
                       target host
  --ip IP              The IP Address of the host machine that you are
                       targetting
  --port PORT          The L4 port of the host machine that you are
                       targetting, defaults to 80
  --endpoint ENDPOINT  The IP Address of the host machine that you are
                       targetting, defaults to api/v1/user/login
  --mode {ssh,http}    The mode of attack, defaults to ssh
  --username USERNAME  If not passed the system will randomly generate a
                       string, otherwise it will always use this value when
                       doing the attack
```

## Local development
1. The current code base depends on python 3.7, you most likely would want to install this from source.
2. Install the dependencies inside `requirements.txt`, `pip install -r requirements.txt`

Most likely, you want a local server to attack. You can spawn a local docker container from the openssh or nginx images and test against these.
1. `nginx`-> `docker run -P -d nginxdemos/hello`
2. `SSH` -> `docker run --name sshd -p 8022:22 ajoergensen/openssh-server`
