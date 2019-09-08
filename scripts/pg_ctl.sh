#!/bin/sh

DB_DIRECTORY="./db"
DB_LOCK_FILE="postmaster.pid"

# Create a database cluster if one does not exist
if [ ! -d "$DB_DIRECTORY" ]; then
    pg_ctl -D ./db initdb
fi

if [ $1 == "initdb" ]; then
    exit 0
else
    pg_ctl -D ./db $@
fi
