*** Settings ***
Library             Process

*** Keywords ***
Start Test Server On Port "${port}" With Data "${fixture}"
    Start Process    python    manage.py    testserver
    ...    --addrport    ${port}
    ...    --noinput
    ...    ../test/fixtures/${fixture}
    ...    cwd=${CURDIR}/../../src
