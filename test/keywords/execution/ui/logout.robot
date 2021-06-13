*** Settings ***
Library           SeleniumLibrary

*** Keywords ***
Log Out Of UI
    Click Link    Log Out
    Title Should Be    ProjectTime | Login
