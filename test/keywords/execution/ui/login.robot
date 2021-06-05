*** Settings ***
Library           SeleniumLibrary

*** Keywords ***
The user logs in to the site with username "${username}" and password "${password}"
    Title Should Be    ProjectTime | Login
    Input Text    username    ${username}
    Input Text    password    ${password}
    Click Button    Log In
    Title Should Be    ProjectTime | Dashboard
