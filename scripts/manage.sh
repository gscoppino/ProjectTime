#!/bin/sh

DB_DIRECTORY="./db"
DB_LOCK_FILE="postmaster.pid"

# Ensure the database exists
if [ ! -d "$DB_DIRECTORY" ]; then
    echo "The database does not exist."
    exit 1
fi

# Ensure the database is running
if [ ! -e "$DB_DIRECTORY/$DB_LOCK_FILE" ]; then
    echo "The database is not running."
    exit 1
fi

if [ "$1" == "runserver" ]; then
    # Ensure there are no Django model changes that require a database migration
    python -Wa manage.py makemigrations --check

    if [ "$?" != 0 ]; then
        exit 1
    fi

    # Ensure the latest schema / fixtures are loaded into the database
    python -Wa manage.py migrate
fi

# Run the given management command
python -Wa manage.py $@
