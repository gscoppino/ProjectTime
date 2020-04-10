#!/bin/sh

PKG_DIR="./src/ProjectTime"
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

# Run the given management command
cd $PKG_DIR && python -Wa manage.py $@
