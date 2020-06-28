*** Settings ***
Library           DateTime
Library           Process
Library           SeleniumLibrary
Library           chromedriver_binary

Resource          ../variables/execution.robot
Resource          ../keywords/setup/application.robot
Resource          ../keywords/setup/browser.robot
Resource          ../keywords/execution/login.robot
Resource          ../keywords/execution/logout.robot
Resource          ../keywords/execution/timezone.robot
Resource          ../keywords/execution/general.robot
Resource          ../keywords/execution/project.robot
Resource          ../keywords/execution/charge.robot
Resource          ../keywords/execution/dashboard.robot

Test Setup        Run Keywords    Start The Application On Port "${SERVER_PORT}" With Data "admin_user.json"    Start The Browser At The Site Root
Test Teardown     Run Keywords    Logout Of Site    Close All Browsers    Terminate All Processes

*** Test Cases ***
Admin Can Create A Project
    The user logs in to the site with username "admin" and password "admin"
    The user goes to the projects list
    The user clicks the "Add project" link
    The user types "Test Project" into the "name" text field
    The user clicks the "Save" button
    The site displays the projects list
    The site displays "Test Project" in the projects list

Admin Changes The Name Of An Existing Project
    The user logs in to the site with username "admin" and password "admin"
    The user creates a project named "Test Project"
    The user goes to the projects list
    The user clicks the "Test Project" link
    The site displays the text "Change project"
    The site displays "Test Project" in the "name" text field
    The site displays the "active" checkbox as checked
    The site displays the "Save" button
    The user clears the "name" text field
    The user types "New Project" into the "name" text field
    The user clicks the "Save" button
    The site displays the projects list
    The site displays "New Project" in the projects list
    The site does not display "Test Project" in the projects list

Admin Can Create A Charge
    The user logs in to the site with username "admin" and password "admin"
    The user uses the timezone prompt to set their timezone to "America/New_York"
    The user creates a project named "Test Project"
    The user goes to the charges list
    The user clicks the "Add charge" link
    The user selects "Test Project" from the "project" selection field
    The user types "1970-01-01" into the "start_time_0" text field
    The user types "09:00:00" into the "start_time_1" text field
    The user clicks the "Save" button
    The site displays the charges list
    The site displays "Test Project" in the charges list

Admin Adds An End Time To An Existing Charge
    The user logs in to the site with username "admin" and password "admin"
    The user uses the timezone prompt to set their timezone to "America/New_York"
    The user creates a project named "Test Project"
    The user creates a charge for "Test Project" with start date "1970-01-01" and start time "09:00:00"
    The user goes to the charges list
    The user clicks the "Test Project" link
    The site displays the text "Change charge"
    The user types "1970-01-01" into the "end_time_0" text field
    The user types "17:00:00" into the "end_time_1" text field
    The user clicks the "Save" button
    The site displays the charges list

Admin Views Project Charges On The Dashboard
    ${current_date} =    Get Current Date    result_format=%m/%d/%Y
    The user logs in to the site with username "admin" and password "admin"
    The user uses the timezone prompt to set their timezone to "America/New_York"
    The user creates a project named "Test Project 1"
    The user creates a project named "Test Project 2"
    The user creates a charge for "Test Project 1" with start date "${current_date}", a start time of "09:00:00", and an end time of "13:00:00"
    The user creates a charge for "Test Project 2" with start date "${current_date}", a start time of "13:00:00", and an end time of "17:00:00"
    The user goes to the dashboard page
    The site displays the "Test Project 1" checkbox as checked
    The site displays the "Test Project 2" checkbox as checked
    The site displays the visualization canvas
    The user unchecks the "Test Project 1" checkbox
    The user clicks the "Filter" button
    The site displays the "Test Project 1" checkbox as unchecked
    The site displays the "Test Project 2" checkbox as checked
    The site displays the visualization canvas
    The user checks the "Test Project 1" checkbox
    The user unchecks the "Test Project 2" checkbox
    The user clicks the "Filter" button
    The site displays the "Test Project 1" checkbox as checked
    The site displays the "Test Project 2" checkbox as unchecked
    The site displays the visualization canvas
