*** Settings ***
Library             SeleniumLibrary

*** Keywords ***
The user logs in to the site with username "${username}" and password "${password}"
    Title Should Be        Log in | ProjectTime
    Input Text             username        ${username}
    Input Text             password        ${password}
    Click Button           Log in
    Title Should Be        ProjectTime Administration | ProjectTime
