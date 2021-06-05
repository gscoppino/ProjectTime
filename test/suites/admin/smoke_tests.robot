*** Settings ***
Library           Process
Library           SeleniumLibrary
Library           chromedriver_binary
Resource          ../../variables/execution.robot
Resource          ../../keywords/setup/application.robot
Resource          ../../keywords/setup/browser.robot
Resource          ../../keywords/navigation/general.robot
Resource          ../../keywords/navigation/admin.robot
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
Test Setup        Navigate To The Site Root
Test Teardown     Run Keywords
...               Log Out Of Site
...               Navigate To A Blank Page
Suite Teardown    Run Keywords
...               Close All Browsers

*** Test Cases ***
Admin Logs In To Site
    The site displays the "username" text field
    The site displays the "password" text field
    The site displays the "Log in" button
    The user logs in to the site with username "admin" and password "admin"
    The site displays the text "Welcome, admin" in the "header" section
    The site displays the "Log out" link

Admin Is Prompted To Set Timezone
    The user logs in to the site with username "admin" and password "admin"
    The site prompts the user for a timezone to use during their session
    The user uses the timezone prompt to set their timezone to "America/New_York"
    The site no longer prompts the user for a timezone

Admin Changes Timezone
    The user logs in to the site with username "admin" and password "admin"
    The site displays the "Change Timezone" link
    The user uses the "Change Timezone" link to set their timezone to "America/New_York"
    The site no longer prompts the user for a timezone

Admin Can View The Project List
    The user logs in to the site with username "admin" and password "admin"
    The site displays the "Projects" link
    The user clicks the "Projects" link
    The site displays the text "Select project to change"

Admin Can View The Add Project Page
    The user logs in to the site with username "admin" and password "admin"
    The user goes to the projects list
    The user clicks the "Add project" link
    The site displays the text "Add project"
    The site displays the "name" text field
    The site displays the "active" checkbox
    The site displays the "Save" button

Admin Can View The Charge List
    The user logs in to the site with username "admin" and password "admin"
    The site displays the "Charges" link
    The user clicks the "Charges" link
    The site displays the text "Select charge to change"

Admin Can View The Add Charge Page
    The user logs in to the site with username "admin" and password "admin"
    The user goes to the charges list
    The user clicks the "Add charge" link
    The site displays the text "Add charge"
    The site displays the "project" selection field
    The site displays the "start_time_0" text field
    The site displays the "start_time_1" text field
    The site displays the "end_time_0" text field
    The site displays the "end_time_1" text field
    The site displays the "closed" checkbox
    The site displays the "Save" button

Admin Can View The Dashboard
    The user logs in to the site with username "admin" and password "admin"
    The site displays the "View Dashboard" link
    The user clicks the "View Dashboard" link
    The site displays the text "Monthly Summary"
    The site displays the text "Select Project(s)"
    The site displays the "Filter" button
