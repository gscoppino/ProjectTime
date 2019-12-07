*** Settings ***
Library             SeleniumLibrary
Library             chromedriver_binary

Resource           ../variables/execution.robot

*** Keywords ***
Start Site
    Set Selenium Speed  ${DRIVER_SPEED_SECS} seconds
    Open Browser        ${SERVER_PROTOCOL}://${SERVER_HOST}:${SERVER_PORT}${SERVER_PATH}   ${BROWSER}

Go To Home Page
    Click Link          //a[contains(text(), "Home") and @href="/"]
    Title Should Be     ProjectTime Administration | ProjectTime

Go To Dashboard
    Click Link          //a[contains(text(), "View Dashboard") and @href="/dashboard"]
    Title Should Be     | ProjectTime

Set Timezone To "${timezone}"
    Click Link                  //a[contains(text(), "Change Timezone") and @href="/timezone"]
    Title Should Be             | Django site admin
    Select From List By Label   timezone    ${timezone}
    Click Button                Submit
    Title Should Be             ProjectTime Administration | ProjectTime
