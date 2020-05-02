#!/bin/sh
set -ex

TOOLBOX_HOME="$PWD/toolbox"

# Create toolbox if not already done
if [ ! -d "$TOOLBOX_HOME"]; then
    mkdir "$TOOLBOX_HOME"
    cp -ruv "$HOME/.gitconfig" \
            "$HOME/.ssh" \
            "$HOME/.bash_profile" \
            "$HOME/.bashrc" \
            "$TOOLBOX_HOME/"

    HOME="$TOOLBOX_HOME" toolbox create
fi

# Ensure user configuration in toolbox is up to date
# with base system
cp -ruv "$HOME/.gitconfig" \
        "$HOME/.ssh" \
        "$HOME/.bash_profile" \
        "$HOME/.bashrc" \
        "$TOOLBOX_HOME/"

# Ensure miniconda is installed in toolbox directory
if [ ! -d "$TOOLBOX_HOME/miniconda" ]; then
    # TODO: Add miniconda installation
fi

# TODO: Ensure conda in toolbox is up to date

# TODO: Ensure anaconda-project is installed in toolbox

