*** Settings ***
Library           Process
Library           SeleniumLibrary
Library           chromedriver_binary
Resource          ../../variables/execution.robot
Resource          ../../keywords/setup/application.robot
Resource          ../../keywords/setup/browser.robot
Resource          ../../keywords/navigation/general.robot
Resource          ../../keywords/navigation/ui.robot
Resource          ../../keywords/execution/general.robot
Resource          ../../keywords/execution/ui/login.robot
Resource          ../../keywords/execution/ui/logout.robot
Suite Setup       Run Keywords
...               Check Application Status
...               Start The Browser
Test Setup        Navigate To The UI
Test Teardown     Run Keywords
...               Log Out Of UI
...               Navigate To A Blank Page
Suite Teardown    Run Keywords
...               Close All Browsers

*** Test Cases ***
Admin Logs In To Site
    The site displays the "username" text field
    The site displays the "password" text field
    The site displays the "Log In" button
    The user logs in to the site with username "admin" and password "admin"
    The site displays the text "Active Projects"
    The site displays the text "Open Charges"
    The site displays the text "Current Month Summary"
    The site displays the "Log Out" link
