*** Settings ***
Library             Process
Library             ../../libraries/ProjectTimeLibrary.py
Resource            ../../variables/execution.robot

*** Keywords ***
Check Application Status
    Wait Until Keyword Succeeds    5x    2 seconds
    ...    Check Application Status At URL "${SERVER_PROTOCOL}://${SERVER_HOST}:${SERVER_PORT}${SERVER_PATH}"