*** Settings ***
Library           SeleniumLibrary

*** Keywords ***
Navigate To The UI
    Go To    ${SERVER_PROTOCOL}://${SERVER_HOST}:${SERVER_PORT}${SERVER_PATH}

Navigate To The Home Page
    ${here} =    Run Keyword And Return Status
    ...    Title Should Be    ProjectTime | Dashboard
    Run Keyword Unless    ${here}
    ...    Click Link    Dashboard
    Title Should Be    ProjectTime | Dashboard

Navigate To The Project List
    Navigate To The Home Page
    Click Link    Projects

Navigate To The Add Project Page
    Navigate To The Project List
    Click Link    Create

Navigate To The Charges List
    Navigate To The Home Page
    Click Link    Time Increments

Navigate To The Add Charge Page
    Navigate To The Charges List
    Click Link    Create
