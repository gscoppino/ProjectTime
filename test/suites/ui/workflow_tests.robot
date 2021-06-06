*** Settings ***
Library           SeleniumLibrary
Library           chromedriver_binary
Resource          ../../keywords/setup/application.robot
Resource          ../../keywords/setup/browser.robot
Resource          ../../keywords/navigation/general.robot
Resource          ../../keywords/navigation/ui.robot
Resource          ../../keywords/execution/ui/login.robot
Resource          ../../keywords/execution/ui/logout.robot
Resource          ../../keywords/execution/ui/timezone.robot
Resource          ../../keywords/execution/ui/project.robot
Resource          ../../keywords/execution/ui/charge.robot
Resource          ../../keywords/execution/general.robot
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
Admin Can Create A Project
    The user logs in to the site with username "admin" and password "admin"
    The user goes to the projects list
    The user clicks the "Create" link
    The user types "Test Project (${SUITE_NAME}-${TEST_NAME})" into the "name" text field
    The user clicks the "Submit" button
    The site displays the projects list
    The site displays "Test Project (${SUITE_NAME}-${TEST_NAME})" in the projects list

Admin Can Create A Charge
    The user logs in to the site with username "admin" and password "admin"
    The user uses the timezone prompt to set their timezone to "America/New_York"
    The user creates a project named "Test Project (${SUITE_NAME}-${TEST_NAME})"
    The user goes to the charges list
    The user clicks the "Create" link
    The user selects "Test Project (${SUITE_NAME}-${TEST_NAME})" from the "project" selection field
    The user types "1970-01-01" into the "start_time_0" text field
    The user types "09:00:00" into the "start_time_1" text field
    The user clicks the "Submit" button
    The site displays the charges list
    The site displays "Test Project (${SUITE_NAME}-${TEST_NAME})" in the charges list
