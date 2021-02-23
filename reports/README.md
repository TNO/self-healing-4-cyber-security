# Components
## Attacker brute force
Trivy:
```
ci.tno.nl:4567/self-healing/attacker-brute-force:master (alpine 3.10.2)
=======================================================================
Total: 4 (HIGH: 4, CRITICAL: 0)
+-------------+------------------+----------+-------------------+---------------+---------------------------------------+
|   LIBRARY   | VULNERABILITY ID | SEVERITY | INSTALLED VERSION | FIXED VERSION |                 TITLE                 |
+-------------+------------------+----------+-------------------+---------------+---------------------------------------+
| expat       | CVE-2019-15903   | HIGH     | 2.2.7-r0          | 2.2.7-r1      | expat: heap-based buffer              |
|             |                  |          |                   |               | over-read via crafted XML input       |
|             |                  |          |                   |               | -->avd.aquasec.com/nvd/cve-2019-15903 |
+-------------+------------------+          +-------------------+---------------+---------------------------------------+
| krb5-libs   | CVE-2020-28196   |          | 1.17-r0           | 1.17.2-r0     | krb5: unbounded recursion via an      |
|             |                  |          |                   |               | ASN.1-encoded Kerberos message        |
|             |                  |          |                   |               | in lib/krb5/asn.1/asn1_encode.c       |
|             |                  |          |                   |               | may lead...                           |
|             |                  |          |                   |               | -->avd.aquasec.com/nvd/cve-2020-28196 |
+-------------+------------------+          +-------------------+---------------+---------------------------------------+
| sqlite-libs | CVE-2019-19244   |          | 3.28.0-r0         | 3.28.0-r2     | sqlite: allows a crash                |
|             |                  |          |                   |               | if a sub-select uses both             |
|             |                  |          |                   |               | DISTINCT and window...                |
|             |                  |          |                   |               | -->avd.aquasec.com/nvd/cve-2019-19244 |
+             +------------------+          +                   +---------------+---------------------------------------+
|             | CVE-2020-11655   |          |                   | 3.28.0-r3     | sqlite: malformed window-function     |
|             |                  |          |                   |               | query leads to DoS                    |
|             |                  |          |                   |               | -->avd.aquasec.com/nvd/cve-2020-11655 |
+-------------+------------------+----------+-------------------+---------------+---------------------------------------+
```

piprot:
```
$ piprot requirements.txt
aiodns (2.0.0) is up to date
aiohttp (3.5.4) is 676 days out of date. Latest is 3.7.3
asyncssh (1.17.0) is 571 days out of date. Latest is 2.5.0
cchardet (2.1.4) is 761 days out of date. Latest is 2.1.7
Your requirements are 2008 days out of date
```

## Host components
### HDDP
Trivy
```
2021-01-20T14:08:14.231Z	INFO	Detecting Debian vulnerabilities...
2021-01-20T14:08:14.290Z	INFO	Trivy skips scanning programming language libraries because no supported file was detected
ci.tno.nl:4567/self-healing/host/hddp:master (debian 10.7)
==========================================================
Total: 2 (HIGH: 2, CRITICAL: 0)
+-------------+------------------+----------+-------------------+-------------------+---------------------------------------+
|   LIBRARY   | VULNERABILITY ID | SEVERITY | INSTALLED VERSION |   FIXED VERSION   |                 TITLE                 |
+-------------+------------------+----------+-------------------+-------------------+---------------------------------------+
| libp11-kit0 | CVE-2020-29361   | HIGH     | 0.23.15-2         | 0.23.15-2+deb10u1 | p11-kit: integer overflow when        |
|             |                  |          |                   |                   | allocating memory for arrays          |
|             |                  |          |                   |                   | or attributes and object...           |
|             |                  |          |                   |                   | -->avd.aquasec.com/nvd/cve-2020-29361 |
+             +------------------+          +                   +                   +---------------------------------------+
|             | CVE-2020-29363   |          |                   |                   | p11-kit: out-of-bounds write in       |
|             |                  |          |                   |                   | p11_rpc_buffer_get_byte_array_value   |
|             |                  |          |                   |                   | function in rpc-message.c             |
|             |                  |          |                   |                   | -->avd.aquasec.com/nvd/cve-2020-29363 |
+-------------+------------------+----------+-------------------+-------------------+---------------------------------------+
```

piprot:
```
$ piprot requirements.txt
aniso8601 (8.0.0) is 445 days out of date. Latest is 8.1.0
attrs (20.3.0) is up to date
certifi (2020.11.8) is 26 days out of date. Latest is 2020.12.5
cffi (1.14.4) is up to date
chardet (3.0.4) is 1281 days out of date. Latest is 4.0.0
click (7.1.2) is up to date
cryptography (3.2.1) is 42 days out of date. Latest is 3.3.1
docker (4.4.0) is 29 days out of date. Latest is 4.4.1
Flask (1.1.2) is up to date
Flask-Cors (3.0.9) is 128 days out of date. Latest is 3.0.10
flask-restx (0.2.0) is up to date
idna (2.10) is 190 days out of date. Latest is 3.1
itsdangerous (1.1.0) is up to date
Jinja2 (2.11.2) is up to date
jsonschema (3.2.0) is up to date
MarkupSafe (1.1.1) is up to date
pycparser (2.20) is up to date
pyOpenSSL (19.1.0) is 393 days out of date. Latest is 20.0.1
pyrsistent (0.17.3) is up to date
python-dateutil (2.8.1) is up to date
pytz (2020.4) is 52 days out of date. Latest is 2020.5
requests (2.23.0) is 182 days out of date. Latest is 2.25.1
six (1.15.0) is up to date
urllib3 (1.25.11) is 24 days out of date. Latest is 1.26.2
websocket-client (0.57.0) is up to date
Werkzeug (1.0.1) is up to date
Your requirements are 2792 days out of date
```

safety:
```
$ safety check
+==============================================================================+
|                                                                              |
|                               /$$$$$$            /$$                         |
|                              /$$__  $$          | $$                         |
|           /$$$$$$$  /$$$$$$ | $$  \__//$$$$$$  /$$$$$$   /$$   /$$           |
|          /$$_____/ |____  $$| $$$$   /$$__  $$|_  $$_/  | $$  | $$           |
|         |  $$$$$$   /$$$$$$$| $$_/  | $$$$$$$$  | $$    | $$  | $$           |
|          \____  $$ /$$__  $$| $$    | $$_____/  | $$ /$$| $$  | $$           |
|          /$$$$$$$/|  $$$$$$$| $$    |  $$$$$$$  |  $$$$/|  $$$$$$$           |
|         |_______/  \_______/|__/     \_______/   \___/   \____  $$           |
|                                                          /$$  | $$           |
|                                                         |  $$$$$$/           |
|  by pyup.io                                              \______/            |
|                                                                              |
+==============================================================================+
| REPORT                                                                       |
| checked 35 packages, using free DB (updated once a month)                    |
+============================+===========+==========================+==========+
| package                    | installed | affected                 | ID       |
+============================+===========+==========================+==========+
| cryptography               | 3.2.1     | <3.3                     | 39252    |
+==============================================================================+
```

### Syslog-ng
Trivy:
```
2021-01-20T14:22:31.981Z	INFO	Trivy skips scanning programming language libraries because no supported file was detected
ci.tno.nl:4567/self-healing/host/syslog-ng:master (debian 9.13)
===============================================================
Total: 0 (HIGH: 0, CRITICAL: 0)
```

### Falco
Trivy:
```
ci.tno.nl:4567/self-healing/host/falco:master (debian 10.5)
===========================================================
Total: 24 (HIGH: 24, CRITICAL: 0)
+------------------+------------------+----------+-----------------------+-----------------------+---------------------------------------+
|     LIBRARY      | VULNERABILITY ID | SEVERITY |   INSTALLED VERSION   |     FIXED VERSION     |                 TITLE                 |
+------------------+------------------+----------+-----------------------+-----------------------+---------------------------------------+
| libgssapi-krb5-2 | CVE-2020-28196   | HIGH     | 1.17-3                | 1.17-3+deb10u1        | krb5: unbounded recursion via an      |
|                  |                  |          |                       |                       | ASN.1-encoded Kerberos message        |
|                  |                  |          |                       |                       | in lib/krb5/asn.1/asn1_encode.c       |
|                  |                  |          |                       |                       | may lead...                           |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2020-28196 |
+------------------+                  +          +                       +                       +                                       +
| libk5crypto3     |                  |          |                       |                       |                                       |
|                  |                  |          |                       |                       |                                       |
|                  |                  |          |                       |                       |                                       |
|                  |                  |          |                       |                       |                                       |
|                  |                  |          |                       |                       |                                       |
+------------------+                  +          +                       +                       +                                       +
| libkrb5-3        |                  |          |                       |                       |                                       |
|                  |                  |          |                       |                       |                                       |
|                  |                  |          |                       |                       |                                       |
|                  |                  |          |                       |                       |                                       |
|                  |                  |          |                       |                       |                                       |
+------------------+                  +          +                       +                       +                                       +
| libkrb5support0  |                  |          |                       |                       |                                       |
|                  |                  |          |                       |                       |                                       |
|                  |                  |          |                       |                       |                                       |
|                  |                  |          |                       |                       |                                       |
|                  |                  |          |                       |                       |                                       |
+------------------+------------------+          +-----------------------+-----------------------+---------------------------------------+
| libldap-2.4-2    | CVE-2020-25692   |          | 2.4.47+dfsg-3+deb10u2 | 2.4.47+dfsg-3+deb10u3 | openldap: NULL pointer dereference    |
|                  |                  |          |                       |                       | for unauthenticated packet in slapd   |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2020-25692 |
+                  +------------------+          +                       +-----------------------+---------------------------------------+
|                  | CVE-2020-25709   |          |                       | 2.4.47+dfsg-3+deb10u4 | openldap: assertion failure in        |
|                  |                  |          |                       |                       | Certificate List syntax validation    |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2020-25709 |
+                  +------------------+          +                       +                       +---------------------------------------+
|                  | CVE-2020-25710   |          |                       |                       | openldap: assertion failure in CSN    |
|                  |                  |          |                       |                       | normalization with invalid input      |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2020-25710 |
+------------------+------------------+          +                       +-----------------------+---------------------------------------+
| libldap-common   | CVE-2020-25692   |          |                       | 2.4.47+dfsg-3+deb10u3 | openldap: NULL pointer dereference    |
|                  |                  |          |                       |                       | for unauthenticated packet in slapd   |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2020-25692 |
+                  +------------------+          +                       +-----------------------+---------------------------------------+
|                  | CVE-2020-25709   |          |                       | 2.4.47+dfsg-3+deb10u4 | openldap: assertion failure in        |
|                  |                  |          |                       |                       | Certificate List syntax validation    |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2020-25709 |
+                  +------------------+          +                       +                       +---------------------------------------+
|                  | CVE-2020-25710   |          |                       |                       | openldap: assertion failure in CSN    |
|                  |                  |          |                       |                       | normalization with invalid input      |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2020-25710 |
+------------------+------------------+          +-----------------------+-----------------------+---------------------------------------+
| libp11-kit0      | CVE-2020-29361   |          | 0.23.15-2             | 0.23.15-2+deb10u1     | p11-kit: integer overflow when        |
|                  |                  |          |                       |                       | allocating memory for arrays          |
|                  |                  |          |                       |                       | or attributes and object...           |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2020-29361 |
+                  +------------------+          +                       +                       +---------------------------------------+
|                  | CVE-2020-29363   |          |                       |                       | p11-kit: out-of-bounds write in       |
|                  |                  |          |                       |                       | p11_rpc_buffer_get_byte_array_value   |
|                  |                  |          |                       |                       | function in rpc-message.c             |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2020-29363 |
+------------------+------------------+          +-----------------------+-----------------------+---------------------------------------+
| libsqlite3-0     | CVE-2019-19959   |          | 3.27.2-3              | 3.27.2-3+deb10u1      | sqlite: mishandles certain uses       |
|                  |                  |          |                       |                       | of INSERT INTO in situations          |
|                  |                  |          |                       |                       | involving embedded '\0'...            |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2019-19959 |
+                  +------------------+          +                       +                       +---------------------------------------+
|                  | CVE-2019-20218   |          |                       |                       | sqlite: selectExpander in             |
|                  |                  |          |                       |                       | select.c proceeds with WITH           |
|                  |                  |          |                       |                       | stack unwinding even after a...       |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2019-20218 |
+                  +------------------+          +                       +                       +---------------------------------------+
|                  | CVE-2020-13630   |          |                       |                       | sqlite: Use-after-free in             |
|                  |                  |          |                       |                       | fts3EvalNextRow in ext/fts3/fts3.c    |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2020-13630 |
+------------------+------------------+          +-----------------------+-----------------------+---------------------------------------+
| linux-libc-dev   | CVE-2019-19377   |          | 4.19.146-1            | 4.19.160-1            | kernel: use-after-free                |
|                  |                  |          |                       |                       | in btrfs_queue_work in                |
|                  |                  |          |                       |                       | fs/btrfs/async-thread.c               |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2019-19377 |
+                  +------------------+          +                       +                       +---------------------------------------+
|                  | CVE-2019-19770   |          |                       |                       | kernel: use-after-free in             |
|                  |                  |          |                       |                       | debugfs_remove in fs/debugfs/inode.c  |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2019-19770 |
+                  +------------------+          +                       +                       +---------------------------------------+
|                  | CVE-2019-19816   |          |                       |                       | kernel: out-of-bounds                 |
|                  |                  |          |                       |                       | write in __btrfs_map_block            |
|                  |                  |          |                       |                       | in fs/btrfs/volumes.c                 |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2019-19816 |
+                  +------------------+          +                       +                       +---------------------------------------+
|                  | CVE-2020-0423    |          |                       |                       | In binder_release_work of             |
|                  |                  |          |                       |                       | binder.c, there is a possible         |
|                  |                  |          |                       |                       | use-after-free due to improper...     |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2020-0423  |
+                  +------------------+          +                       +-----------------------+---------------------------------------+
|                  | CVE-2020-12351   |          |                       | 4.19.152-1            | kernel: net: bluetooth:               |
|                  |                  |          |                       |                       | type confusion while                  |
|                  |                  |          |                       |                       | processing AMP packets                |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2020-12351 |
+                  +------------------+          +                       +-----------------------+---------------------------------------+
|                  | CVE-2020-14351   |          |                       | 4.19.160-1            | kernel: performance counters          |
|                  |                  |          |                       |                       | race condition use-after-free         |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2020-14351 |
+                  +------------------+          +                       +-----------------------+---------------------------------------+
|                  | CVE-2020-25643   |          |                       | 4.19.152-1            | kernel: improper input validation     |
|                  |                  |          |                       |                       | in ppp_cp_parse_cr function           |
|                  |                  |          |                       |                       | leads to memory corruption and...     |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2020-25643 |
+                  +------------------+          +                       +                       +---------------------------------------+
|                  | CVE-2020-25645   |          |                       |                       | kernel: Geneve/IPsec                  |
|                  |                  |          |                       |                       | traffic may be unencrypted            |
|                  |                  |          |                       |                       | between two Geneve endpoints          |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2020-25645 |
+                  +------------------+          +                       +-----------------------+---------------------------------------+
|                  | CVE-2020-25705   |          |                       | 4.19.160-1            | kernel: ICMP rate limiting can        |
|                  |                  |          |                       |                       | be used for DNS poisoning attack      |
|                  |                  |          |                       |                       | -->avd.aquasec.com/nvd/cve-2020-25705 |
+------------------+------------------+----------+-----------------------+-----------------------+---------------------------------------+
```

## Pod Components
### Channel frequency monitor
Trivy:
```
ci.tno.nl:4567/self-healing/pod/channel-frequency-monitor:master (alpine 3.12.3)
================================================================================
Total: 0 (HIGH: 0, CRITICAL: 0)
```

piprot:
```
$ piprot requirements.txt
redis (3.5.3) is up to date
Looks like you've been keeping up to date, time for a delicious beverage!
```
### Lymphocyte
piprot:
```
$ piprot requirements.txt
requests (2.24.0) is 182 days out of date. Latest is 2.25.1
redis (3.5.3) is up to date
pymongo (3.11.1) is 15 days out of date. Latest is 3.11.2
```

Trivy:
```
ci.tno.nl:4567/self-healing/pod/lymphocyte:master (debian 10.7)
===============================================================
Total: 0 (HIGH: 0, CRITICAL: 0)
```

safety:
```
$ pip show safety
Name: safety
Version: 1.10.3
$ safety check
+==============================================================================+
|                                                                              |
|                               /$$$$$$            /$$                         |
|                              /$$__  $$          | $$                         |
|           /$$$$$$$  /$$$$$$ | $$  \__//$$$$$$  /$$$$$$   /$$   /$$           |
|          /$$_____/ |____  $$| $$$$   /$$__  $$|_  $$_/  | $$  | $$           |
|         |  $$$$$$   /$$$$$$$| $$_/  | $$$$$$$$  | $$    | $$  | $$           |
|          \____  $$ /$$__  $$| $$    | $$_____/  | $$ /$$| $$  | $$           |
|          /$$$$$$$/|  $$$$$$$| $$    |  $$$$$$$  |  $$$$/|  $$$$$$$           |
|         |_______/  \_______/|__/     \_______/   \___/   \____  $$           |
|                                                          /$$  | $$           |
|                                                         |  $$$$$$/           |
|  by pyup.io                                              \______/            |
|                                                                              |
+==============================================================================+
| REPORT                                                                       |
| checked 20 packages, using free DB (updated once a month)                    |
+==============================================================================+
| No known security vulnerabilities found.                                     |
+==============================================================================+
```

## Shared
### Python shared common
Trivy:
```
ci.tno.nl:4567/self-healing/web-application/python-shared:master (debian 10.7)
==============================================================================
Total: 0 (HIGH: 0, CRITICAL: 0)
```

Safety:
```
$ pip show safety
Name: safety
Version: 1.10.3
$ safety check
+==============================================================================+
|                                                                              |
|                               /$$$$$$            /$$                         |
|                              /$$__  $$          | $$                         |
|           /$$$$$$$  /$$$$$$ | $$  \__//$$$$$$  /$$$$$$   /$$   /$$           |
|          /$$_____/ |____  $$| $$$$   /$$__  $$|_  $$_/  | $$  | $$           |
|         |  $$$$$$   /$$$$$$$| $$_/  | $$$$$$$$  | $$    | $$  | $$           |
|          \____  $$ /$$__  $$| $$    | $$_____/  | $$ /$$| $$  | $$           |
|          /$$$$$$$/|  $$$$$$$| $$    |  $$$$$$$  |  $$$$/|  $$$$$$$           |
|         |_______/  \_______/|__/     \_______/   \___/   \____  $$           |
|                                                          /$$  | $$           |
|                                                         |  $$$$$$/           |
|  by pyup.io                                              \______/            |
|                                                                              |
+==============================================================================+
| REPORT                                                                       |
| checked 15 packages, using free DB (updated once a month)                    |
+==============================================================================+
| No known security vulnerabilities found.                                     |
+==============================================================================+
```

## Web application
#### Authentication bastion
Trivy:
```
ci.tno.nl:4567/self-healing/web-application/authentication-bastion:master (alpine 3.10.2)
=========================================================================================
Total: 4 (HIGH: 4, CRITICAL: 0)
+-------------+------------------+----------+-------------------+---------------+---------------------------------------+
|   LIBRARY   | VULNERABILITY ID | SEVERITY | INSTALLED VERSION | FIXED VERSION |                 TITLE                 |
+-------------+------------------+----------+-------------------+---------------+---------------------------------------+
| expat       | CVE-2019-15903   | HIGH     | 2.2.7-r0          | 2.2.7-r1      | expat: heap-based buffer              |
|             |                  |          |                   |               | over-read via crafted XML input       |
|             |                  |          |                   |               | -->avd.aquasec.com/nvd/cve-2019-15903 |
+-------------+------------------+          +-------------------+---------------+---------------------------------------+
| krb5-libs   | CVE-2020-28196   |          | 1.17-r0           | 1.17.2-r0     | krb5: unbounded recursion via an      |
|             |                  |          |                   |               | ASN.1-encoded Kerberos message        |
|             |                  |          |                   |               | in lib/krb5/asn.1/asn1_encode.c       |
|             |                  |          |                   |               | may lead...                           |
|             |                  |          |                   |               | -->avd.aquasec.com/nvd/cve-2020-28196 |
+-------------+------------------+          +-------------------+---------------+---------------------------------------+
| sqlite-libs | CVE-2019-19244   |          | 3.28.0-r0         | 3.28.0-r2     | sqlite: allows a crash                |
|             |                  |          |                   |               | if a sub-select uses both             |
|             |                  |          |                   |               | DISTINCT and window...                |
|             |                  |          |                   |               | -->avd.aquasec.com/nvd/cve-2019-19244 |
+             +------------------+          +                   +---------------+---------------------------------------+
|             | CVE-2020-11655   |          |                   | 3.28.0-r3     | sqlite: malformed window-function     |
|             |                  |          |                   |               | query leads to DoS                    |
|             |                  |          |                   |               | -->avd.aquasec.com/nvd/cve-2020-11655 |
+-------------+------------------+----------+-------------------+---------------+---------------------------------------+
```

#### Vulnerable php container
Trivy:
```
ci.tno.nl:4567/self-healing/web-application/vulnerable-php-container:master (debian 10.7)
=========================================================================================
Total: 0 (HIGH: 0, CRITICAL: 0)
```

piprot:
```
$ piprot requirements.txt
Looks like you've been keeping up to date, time for a delicious beverage!
```

#### Nginx frontend
Trivy:
```
ci.tno.nl:4567/self-healing/web-application/nginx-frontend:master (debian 10.3)
===============================================================================
Total: 18 (HIGH: 18, CRITICAL: 0)
+-----------------+------------------+----------+-------------------+-----------------------+---------------------------------------+
|     LIBRARY     | VULNERABILITY ID | SEVERITY | INSTALLED VERSION |     FIXED VERSION     |                 TITLE                 |
+-----------------+------------------+----------+-------------------+-----------------------+---------------------------------------+
| libgnutls30     | CVE-2020-11501   | HIGH     | 3.6.7-4+deb10u2   | 3.6.7-4+deb10u3       | gnutls: DTLS client hello contains    |
|                 |                  |          |                   |                       | a random value of all zeroes          |
|                 |                  |          |                   |                       | -->avd.aquasec.com/nvd/cve-2020-11501 |
+                 +------------------+          +                   +-----------------------+---------------------------------------+
|                 | CVE-2020-13777   |          |                   | 3.6.7-4+deb10u4       | gnutls: session resumption works      |
|                 |                  |          |                   |                       | without master key allowing MITM      |
|                 |                  |          |                   |                       | -->avd.aquasec.com/nvd/cve-2020-13777 |
+-----------------+------------------+          +-------------------+-----------------------+---------------------------------------+
| libicu63        | CVE-2020-10531   |          | 63.1-6            | 63.1-6+deb10u1        | ICU: Integer overflow in              |
|                 |                  |          |                   |                       | UnicodeString::doAppend()             |
|                 |                  |          |                   |                       | -->avd.aquasec.com/nvd/cve-2020-10531 |
+-----------------+------------------+          +-------------------+-----------------------+---------------------------------------+
| libjpeg62-turbo | CVE-2020-13790   |          | 1:1.5.2-2         | 1:1.5.2-2+deb10u1     | libjpeg-turbo: heap-based buffer      |
|                 |                  |          |                   |                       | over-read in get_rgb_row() in rdppm.c |
|                 |                  |          |                   |                       | -->avd.aquasec.com/nvd/cve-2020-13790 |
+-----------------+------------------+          +-------------------+-----------------------+---------------------------------------+
| libp11-kit0     | CVE-2020-29361   |          | 0.23.15-2         | 0.23.15-2+deb10u1     | p11-kit: integer overflow when        |
|                 |                  |          |                   |                       | allocating memory for arrays          |
|                 |                  |          |                   |                       | or attributes and object...           |
|                 |                  |          |                   |                       | -->avd.aquasec.com/nvd/cve-2020-29361 |
+                 +------------------+          +                   +                       +---------------------------------------+
|                 | CVE-2020-29363   |          |                   |                       | p11-kit: out-of-bounds write in       |
|                 |                  |          |                   |                       | p11_rpc_buffer_get_byte_array_value   |
|                 |                  |          |                   |                       | function in rpc-message.c             |
|                 |                  |          |                   |                       | -->avd.aquasec.com/nvd/cve-2020-29363 |
+-----------------+------------------+          +-------------------+-----------------------+---------------------------------------+
| libssl1.1       | CVE-2020-1967    |          | 1.1.1d-0+deb10u2  | 1.1.1d-0+deb10u3      | openssl: Segmentation                 |
|                 |                  |          |                   |                       | fault in SSL_check_chain              |
|                 |                  |          |                   |                       | causes denial of service              |
|                 |                  |          |                   |                       | -->avd.aquasec.com/nvd/cve-2020-1967  |
+-----------------+------------------+          +-------------------+-----------------------+---------------------------------------+
| libsystemd0     | CVE-2020-1712    |          | 241-7~deb10u3     | 241-7~deb10u4         | systemd: use-after-free               |
|                 |                  |          |                   |                       | when asynchronous polkit              |
|                 |                  |          |                   |                       | queries are performed                 |
|                 |                  |          |                   |                       | -->avd.aquasec.com/nvd/cve-2020-1712  |
+-----------------+                  +          +                   +                       +                                       +
| libudev1        |                  |          |                   |                       |                                       |
|                 |                  |          |                   |                       |                                       |
|                 |                  |          |                   |                       |                                       |
|                 |                  |          |                   |                       |                                       |
+-----------------+------------------+          +-------------------+-----------------------+---------------------------------------+
| libx11-6        | CVE-2020-14363   |          | 2:1.6.7-1         | 2:1.6.7-1+deb10u1     | libX11: integer overflow leads        |
|                 |                  |          |                   |                       | to double free in locale handling     |
|                 |                  |          |                   |                       | -->avd.aquasec.com/nvd/cve-2020-14363 |
+-----------------+                  +          +                   +                       +                                       +
| libx11-data     |                  |          |                   |                       |                                       |
|                 |                  |          |                   |                       |                                       |
|                 |                  |          |                   |                       |                                       |
+-----------------+------------------+          +-------------------+-----------------------+---------------------------------------+
| libxml2         | CVE-2018-14404   |          | 2.9.4+dfsg1-7     | 2.9.4+dfsg1-7+deb10u1 | libxml2: NULL pointer dereference     |
|                 |                  |          |                   |                       | in xmlXPathCompOpEval()               |
|                 |                  |          |                   |                       | function in xpath.c                   |
|                 |                  |          |                   |                       | -->avd.aquasec.com/nvd/cve-2018-14404 |
+                 +------------------+          +                   +                       +---------------------------------------+
|                 | CVE-2019-19956   |          |                   |                       | libxml2: memory leak in               |
|                 |                  |          |                   |                       | xmlParseBalancedChunkMemoryRecover    |
|                 |                  |          |                   |                       | in parser.c                           |
|                 |                  |          |                   |                       | -->avd.aquasec.com/nvd/cve-2019-19956 |
+                 +------------------+          +                   +                       +---------------------------------------+
|                 | CVE-2019-20388   |          |                   |                       | libxml2: memory leak in               |
|                 |                  |          |                   |                       | xmlSchemaPreRun in xmlschemas.c       |
|                 |                  |          |                   |                       | -->avd.aquasec.com/nvd/cve-2019-20388 |
+                 +------------------+          +                   +                       +---------------------------------------+
|                 | CVE-2020-7595    |          |                   |                       | libxml2: infinite loop in             |
|                 |                  |          |                   |                       | xmlStringLenDecodeEntities in         |
|                 |                  |          |                   |                       | some end-of-file situations           |
|                 |                  |          |                   |                       | -->avd.aquasec.com/nvd/cve-2020-7595  |
+-----------------+------------------+          +-------------------+-----------------------+---------------------------------------+
| perl-base       | CVE-2020-10543   |          | 5.28.1-6          | 5.28.1-6+deb10u1      | perl: heap-based buffer               |
|                 |                  |          |                   |                       | overflow in regular expression        |
|                 |                  |          |                   |                       | compiler leads to DoS                 |
|                 |                  |          |                   |                       | -->avd.aquasec.com/nvd/cve-2020-10543 |
+                 +------------------+          +                   +                       +---------------------------------------+
|                 | CVE-2020-10878   |          |                   |                       | perl: corruption of intermediate      |
|                 |                  |          |                   |                       | language state of compiled            |
|                 |                  |          |                   |                       | regular expression due to...          |
|                 |                  |          |                   |                       | -->avd.aquasec.com/nvd/cve-2020-10878 |
+                 +------------------+          +                   +                       +---------------------------------------+
|                 | CVE-2020-12723   |          |                   |                       | perl: corruption of intermediate      |
|                 |                  |          |                   |                       | language state of compiled            |
|                 |                  |          |                   |                       | regular expression due to...          |
|                 |                  |          |                   |                       | -->avd.aquasec.com/nvd/cve-2020-12723 |
+-----------------+------------------+----------+-------------------+-----------------------+---------------------------------------+
```