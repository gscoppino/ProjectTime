*** Settings ***
Library             SeleniumLibrary
Library             chromedriver_binary

Resource            ./general.robot

*** Keywords ***
Login To The Site With Username "${username}" And Password "${password}"
    Start Site
    Title Should Be     Log in | ProjectTime
    Input Text          username        ${username}
    Input Text          password        ${password}
    Click Button        Log in
    Title Should Be     ProjectTime Administration | ProjectTime
