#!/bin/sh

PKG_DIR="./src/ProjectTime"

if [ -z "$1" ]; then
    cd $PKG_DIR && coverage run $@ --source "." --omit="envs/*,*/tests/*" --branch manage.py test --failfast
    exit 0
fi

cd $PKG_DIR && coverage $@
