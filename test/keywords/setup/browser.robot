*** Settings ***
Library             SeleniumLibrary

Resource           ../../variables/execution.robot

*** Keywords ***
Start The Browser
    Set Selenium Speed    ${DRIVER_SPEED_SECS} seconds
    Open Browser    about:blank    ${BROWSER}

Start The Browser At The Site Root
    Set Selenium Speed    ${DRIVER_SPEED_SECS} seconds
    Open Browser    ${SERVER_PROTOCOL}://${SERVER_HOST}:${SERVER_PORT}${SERVER_PATH}   ${BROWSER}