*** Settings ***
Library             SeleniumLibrary

*** Keywords ***
Navigate To A Blank Page
    Go To    about:blank

Navigate To The Site Root
    Go To    ${SERVER_PROTOCOL}://${SERVER_HOST}:${SERVER_PORT}${SERVER_PATH}admin

Navigate To The Home Page
    ${here} =    Run Keyword And Return Status
    ...    Title Should Be    ProjectTime Administration | ProjectTime
    Run Keyword Unless    ${here}
    ...    Click Link          //a[contains(text(), "Home") and @href="/admin/"]
    Title Should Be     ProjectTime Administration | ProjectTime

Navigate To The Project List
    Navigate To The Home Page
    Click Link    Projects

Navigate To The Add Project Page
    Navigate To The Project List
    Click Link    Add project

Navigate To The Charges List
    Navigate To The Home Page
    Click Link    Charges

Navigate To The Add Charge Page
    Navigate To The Charges List
    Click Link         Add charge
    Title Should Be    Add charge | ProjectTime
