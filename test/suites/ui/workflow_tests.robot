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
User Can Create A Project
    The user logs in to the site with username "admin" and password "admin"
    The user goes to the projects list
    The user clicks the "Create" link
    The user types "Test Project (${SUITE_NAME}-${TEST_NAME})" into the "name" text field
    The user clicks the "Submit" button
    The site displays the projects list
    The site displays "Test Project (${SUITE_NAME}-${TEST_NAME})" in the projects list

User Changes The Name Of An Existing Project
    The user logs in to the site with username "admin" and password "admin"
    The user creates a project named "Test Project (${SUITE_NAME}-${TEST_NAME})"
    The user goes to the projects list
    The user clicks the "Test Project (${SUITE_NAME}-${TEST_NAME})" link
    The site displays the text "Update Project \"Test Project (${SUITE_NAME}-${TEST_NAME})\""
    The site displays "Test Project (${SUITE_NAME}-${TEST_NAME})" in the "name" text field
    The site displays the "active" checkbox as checked
    The site displays the "Submit" button
    The user clears the "name" text field
    The user types "New Project (${SUITE_NAME}-${TEST_NAME})" into the "name" text field
    The user clicks the "Submit" button
    The site displays the projects list
    The site displays "New Project (${SUITE_NAME}-${TEST_NAME})" in the projects list
    The site does not display "Test Project (${SUITE_NAME}-${TEST_NAME})" in the projects list

User Can Create A Charge
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

User Adds An End Time To An Existing Charge
    The user logs in to the site with username "admin" and password "admin"
    The user uses the timezone prompt to set their timezone to "America/New_York"
    The user creates a project named "Test Project (${SUITE_NAME}-${TEST_NAME})"
    The user creates a charge for "Test Project (${SUITE_NAME}-${TEST_NAME})" with start date "1970-01-01" and start time "09:00:00"
    The user goes to the charges list
    The user clicks the "Test Project (${SUITE_NAME}-${TEST_NAME})" link
    The user types "1970-01-01" into the "end_time_0" text field
    The user types "17:00:00" into the "end_time_1" text field
    The user clicks the "Submit" button
    The site displays the charges list
