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
Resource          ../../keywords/execution/ui/timezone.robot
Resource          ../../keywords/execution/ui/project.robot
Resource          ../../keywords/execution/ui/charge.robot
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
User Logs In To Site
    The site displays the "username" text field
    The site displays the "password" text field
    The site displays the "Log In" button
    The user logs in to the site with username "admin" and password "admin"
    The site displays the text "Active Projects"
    The site displays the text "Open Charges"
    The site displays the text "Current Month Summary"
    The site displays the "Log Out" link

User Is Prompted To Set Timezone
    The user logs in to the site with username "admin" and password "admin"
    The site prompts the user for a timezone to use during their session
    The user uses the timezone prompt to set their timezone to "America/New_York"
    The site no longer prompts the user for a timezone

User Can View The Project List
    The user logs in to the site with username "admin" and password "admin"
    The site displays the "Projects" link
    The user clicks the "Projects" link
    The site displays the text "Projects"

User Can View The Add Project Page
    The user logs in to the site with username "admin" and password "admin"
    The user goes to the projects list
    The user clicks the "Create" link
    The site displays the text "Create Project"
    The site displays the "name" text field
    The site displays the "active" checkbox
    The site displays the "Submit" button

User Can View The Charge List
    The user logs in to the site with username "admin" and password "admin"
    The site displays the "Charges" link
    The user clicks the "Charges" link
    The site displays the text "Charges"

User Can View The Add Charge Page
    The user logs in to the site with username "admin" and password "admin"
    The user goes to the charges list
    The user clicks the "Create" link
    The site displays the text "Create Charge"
    The site displays the "project" selection field
    The site displays the "start_time_0" text field
    The site displays the "start_time_1" text field
    The site displays the "end_time_0" text field
    The site displays the "end_time_1" text field
    The site displays the "closed" checkbox
    The site displays the "Submit" button

User Can Navigate To And From The UI And Admin Site
    The user logs in to the site with username "admin" and password "admin"
    The user clicks the "Administration" link
    The site displays the text "ProjectTime Administration"
    The user clicks the "View site" link
    The site displays the text "Active Projects"
    The site displays the text "Open Charges"
    The site displays the text "Current Month Summary"

User Can Access The Add Project Page From The Dashboard
    The user logs in to the site with username "admin" and password "admin"
    The user clicks the "+ Create Project" link
    The site displays the text "Create Project"
    The site displays the "name" text field
    The site displays the "active" checkbox
    The site displays the "Submit" button

User Can Access The Add Charge Page From The Dashboard
    The user logs in to the site with username "admin" and password "admin"
    The user clicks the "+ Create Charge" link
    The site displays the text "Create Charge"
    The site displays the "project" selection field
    The site displays the "start_time_0" text field
    The site displays the "start_time_1" text field
    The site displays the "end_time_0" text field
    The site displays the "end_time_1" text field
    The site displays the "closed" checkbox
    The site displays the "Submit" button
