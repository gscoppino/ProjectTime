*** Settings ***
Library           DateTime
Library           Process
Library           SeleniumLibrary
Library           chromedriver_binary
Resource          ../../variables/execution.robot
Resource          ../../keywords/setup/application.robot
Resource          ../../keywords/setup/browser.robot
Resource          ../../keywords/setup/random.robot
Resource          ../../keywords/navigation/general.robot
Resource          ../../keywords/execution/general.robot
Resource          ../../keywords/execution/admin/login.robot
Resource          ../../keywords/execution/admin/logout.robot
Resource          ../../keywords/execution/admin/timezone.robot
Resource          ../../keywords/execution/admin/project.robot
Resource          ../../keywords/execution/admin/charge.robot
Resource          ../../keywords/execution/admin/dashboard.robot
Suite Setup       Run Keywords
...               Check Application Status
...               Start The Browser
Test Setup        Run Keywords
...               Navigate To The Site Root
...               Initialize Random Variables For Test
Test Teardown     Run Keywords
...               Log Out Of Site
...               Navigate To A Blank Page
Suite Teardown    Run Keywords
...               Close All Browsers

*** Test Cases ***
Admin Can Create A Project
    The user logs in to the site with username "admin" and password "admin"
    The user goes to the projects list
    The user clicks the "Add project" link
    The user types "${RANDOM_NAME}" into the "name" text field
    The user clicks the "Save" button
    The site displays the projects list
    The site displays "${RANDOM_NAME}" in the projects list

Admin Changes The Name Of An Existing Project
    The user logs in to the site with username "admin" and password "admin"
    The user creates a project named "${RANDOM_NAME}"
    The user goes to the projects list
    The user clicks the "${RANDOM_NAME}" link
    The site displays the text "Change project"
    The site displays "${RANDOM_NAME}" in the "name" text field
    The site displays the "active" checkbox as checked
    The site displays the "Save" button
    The user clears the "name" text field
    The user types "${RANDOM_NAME} (edited)" into the "name" text field
    The user clicks the "Save" button
    The site displays the projects list
    The site displays "${RANDOM_NAME} (edited)" in the projects list

Admin Can Create A Charge
    The user logs in to the site with username "admin" and password "admin"
    The user uses the timezone prompt to set their timezone to "America/New_York"
    The user creates a project named "${RANDOM_NAME}"
    The user goes to the charges list
    The user clicks the "Add time increment" link
    The user selects "${RANDOM_NAME}" from the "project" selection field
    The user types "1970-01-01" into the "start_time_0" text field
    The user types "09:00:00" into the "start_time_1" text field
    The user clicks the "Save" button
    The site displays the charges list
    The site displays "${RANDOM_NAME}" in the charges list

Admin Adds An End Time To An Existing Charge
    The user logs in to the site with username "admin" and password "admin"
    The user uses the timezone prompt to set their timezone to "America/New_York"
    The user creates a project named "${RANDOM_NAME}"
    The user creates a charge for "${RANDOM_NAME}" with start date "1970-01-01" and start time "09:00:00"
    The user goes to the charges list
    The user clicks the "${RANDOM_NAME}" link in the charges list
    The site displays the text "Change time increment"
    The user types "1970-01-01" into the "end_time_0" text field
    The user types "17:00:00" into the "end_time_1" text field
    The user clicks the "Save" button
    The site displays the charges list

Admin Views Project Charges On The Dashboard
    ${current_date} =    Get Current Date    result_format=%m/%d/%Y
    The user logs in to the site with username "admin" and password "admin"
    The user uses the timezone prompt to set their timezone to "America/New_York"
    The user creates a project named "${RANDOM_NAME} 1"
    The user creates a project named "${RANDOM_NAME} 2"
    The user creates a charge for "${RANDOM_NAME} 1" with start date "${current_date}", a start time of "09:00:00", and an end time of "13:00:00"
    The user creates a charge for "${RANDOM_NAME} 2" with start date "${current_date}", a start time of "13:00:00", and an end time of "17:00:00"
    The user goes to the dashboard page
    The site displays the "${RANDOM_NAME} 1" checkbox as checked
    The site displays the "${RANDOM_NAME} 2" checkbox as checked
    The site displays the visualization canvas
    The user unchecks the "${RANDOM_NAME} 1" checkbox
    The user clicks the "Filter" button
    The site displays the "${RANDOM_NAME} 1" checkbox as unchecked
    The site displays the "${RANDOM_NAME} 2" checkbox as checked
    The site displays the visualization canvas
    The user checks the "${RANDOM_NAME} 1" checkbox
    The user unchecks the "${RANDOM_NAME} 2" checkbox
    The user clicks the "Filter" button
    The site displays the "${RANDOM_NAME} 1" checkbox as checked
    The site displays the "${RANDOM_NAME} 2" checkbox as unchecked
    The site displays the visualization canvas
