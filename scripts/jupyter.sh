#!/bin/sh

if [ ! -f "kernel.json" ]; then
    echo "Could not find development kernel. Did you do anaconda-project run setup?"
    exit 1
fi

cp kernel.json envs/notebook/share/jupyter/kernels/python3/kernel.json
jupyter $@
