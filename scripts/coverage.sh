#!/bin/sh

if [ -z "$1" ]; then
    coverage run $@ --source "." --omit="envs/*,*/tests/*" --branch manage.py test --failfast
    exit 0
fi

coverage $@
