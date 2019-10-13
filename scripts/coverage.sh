#!/bin/sh

if [ -z "$1" ]; then
    cd src && coverage run $@ --source "." --omit="envs/*,*/tests/*" --branch manage.py test --failfast
    exit 0
fi

cd src && coverage $@
