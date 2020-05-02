*** Settings ***
Library    OperatingSystem
Library    Process

*** Keywords ***
Archive The Database To "${filename}"
    Run Process    anaconda-project    run    pg_dump    test_postgres
    ...    --clean
    ...    --if-exists
    ...    stdout=./test_dumps/${filename}
    ...    cwd=${CURDIR}/../../

Restore The Database From "${filename}"
    Run Process    anaconda-project    run    psql    -f
    ...    ./test_dumps/${filename}
    ...    test_postgres
    ...    --single-transaction
    ...    cwd=${CURDIR}/../../

Use "${keyword}"
    ${exists} =    Run Keyword And Return Status    File Should Exist
    ...    ./test_dumps/${keyword}
    Run Keyword If    ${exists}    Restore The Database From "${keyword}"
    ...    ELSE    Run Keywords    ${keyword}    Archive The Database To "${keyword}"