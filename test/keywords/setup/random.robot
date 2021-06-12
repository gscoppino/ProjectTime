*** Settings ***
Library    String

*** Keywords ***
Initialize Random Variables For Test
    ${RANDOM_STRING}     Generate Random String
    ${RANDOM_NAME}       Catenate    SEPARATOR=-    ${SUITE_NAME}    ${TEST_NAME}    ${RANDOM_STRING}
    Set Test Variable    ${RANDOM_NAME}
