#!/bin/sh

if [ -f "kernel.json" ]; then
    exit 0
fi

ipython kernel install --prefix /tmp
cp /tmp/share/jupyter/kernels/python3/kernel.json ./kernel.json
