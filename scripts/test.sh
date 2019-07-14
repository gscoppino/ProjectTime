#!/bin/sh

# (Re)start the database server
if [ ! -e "$DB_DIRECTORY/$DB_LOCK_FILE" ]; then
    pg_ctl -D ./db start
else
    pg_ctl -D ./db restart
fi

# Execute tests in parallel, displaying warnings, fail suite on first failed test.
python -Wa manage.py test --parallel --failfast
