#!/bin/sh

DB_DIRECTORY="./db"

# Create a database cluster if one does not exist
if [ ! -d "$DB_DIRECTORY" ]; then
    pg_ctl -D "$DB_DIRECTORY" initdb
fi


postgres -D "$DB_DIRECTORY" $@
