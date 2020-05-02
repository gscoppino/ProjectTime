*** Settings ***
Library             Process

*** Keywords ***
Start The Application On Port "${port}" With Data "${fixture}"
    Start Process    anaconda-project    run    manage.py    testserver
    ...    --addrport    ${port}
    ...    --noinput
    ...    ../test/fixtures/${fixture}
    ...    cwd=${CURDIR}/../../../
    Sleep    1s