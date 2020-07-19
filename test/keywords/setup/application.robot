*** Settings ***
Library             Process
Resource           ../../variables/execution.robot

*** Keywords ***
Start The Application With Data From "${fixture}"
    Run Process      anaconda-project    prepare    --env-spec    application
    Start Process    anaconda-project    run    manage.py    testserver
    ...    --addrport    ${SERVER_PORT}
    ...    --noinput
    ...    ../../test/fixtures/${fixture}
    ...    cwd=${CURDIR}/../../../
    Run Process    curl    -4    --retry-delay    2    --retry    5    --retry-connrefused
    ...    ${SERVER_PROTOCOL}://${SERVER_HOST}:${SERVER_PORT}${SERVER_PATH}