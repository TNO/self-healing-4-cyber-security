#!/bin/bash

python3 /redis4php.py || exit

php-fpm
