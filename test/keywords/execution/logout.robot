*** Settings ***
Library             SeleniumLibrary

*** Keywords ***
Log Out Of Site
    Click Link          Log out
    Title Should Be     Logged out | ProjectTime