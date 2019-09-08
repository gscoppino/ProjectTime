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
