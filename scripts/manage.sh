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
fi

if [ $1 == "makemigrations" ] || [ $1 == "squashmigrations" ]; then
    # Create the migration, then ensure the latest schema / fixtures are loaded
    # into the database
    python -Wa manage.py $@
    python -Wa manage.py migrate
elif [ $1 == "migrate" ] || [ $1 == "test" ]; then
    # Run the given management command
    python -Wa manage.py $@
else
    # Ensure the latest schema / fixtures are loaded into the database,
    # then run the given management command.
    python -Wa manage.py migrate
    python -Wa manage.py $@
fi

pg_ctl -D ./db stop
