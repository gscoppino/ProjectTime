#!/bin/sh

DB_DIRECTORY="./db"
DB_LOCK_FILE="postmaster.pid"

# Create a database cluster if one does not exist
if [ ! -d "$DB_DIRECTORY" ]; then
    pg_ctl -D ./db initdb
fi

# (Re)start the database server
if [ ! -e "$DB_DIRECTORY/$DB_LOCK_FILE" ]; then
    pg_ctl -D ./db start
else
    pg_ctl -D ./db restart
fi

# Ensure the latest schema / fixtures are loaded into to the database.
if [ $1 != "migrate" ]; then
    python -Wa manage.py migrate
fi

# Execute the provided command
python -Wa manage.py $@
