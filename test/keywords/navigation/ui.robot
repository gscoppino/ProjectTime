*** Settings ***
Library           SeleniumLibrary

*** Keywords ***
Navigate To The UI
    Go To    ${SERVER_PROTOCOL}://${SERVER_HOST}:${SERVER_PORT}${SERVER_PATH}
