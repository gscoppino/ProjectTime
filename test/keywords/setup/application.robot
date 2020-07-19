*** Settings ***
Library             Process
Library             ../../libraries/ProjectTimeLibrary.py
Resource           ../../variables/execution.robot

*** Keywords ***
Start The Application With Data From "${fixture}"
    Run Process      anaconda-project    prepare    --env-spec    application
    Start Process    anaconda-project    run    manage.py    testserver
    ...    --addrport    ${SERVER_PORT}
    ...    --noinput
    ...    ../../test/fixtures/${fixture}
    ...    cwd=${CURDIR}/../../../
    Wait Until Keyword Succeeds    5x    5 seconds
    ...    Check Application Status At URL "${SERVER_PROTOCOL}://${SERVER_HOST}:${SERVER_PORT}${SERVER_PATH}"