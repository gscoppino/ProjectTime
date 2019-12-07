*** Settings ***
Test Setup        Start Test Server On Port "${SERVER_PORT}" With Data "admin_user.json"
Test Teardown     Run Keywords    Logout Of Site    Stop Test Server
Library           DateTime
Library           ../libraries/ProjectTimeLibrary.py
Resource          ../variables/execution.robot
Resource          ../keywords/login.robot
Resource          ../keywords/logout.robot
Resource          ../keywords/general.robot
Resource          ../keywords/project.robot
Resource          ../keywords/charge.robot

*** Test Cases ***
Admin Logs In To Site
    Login To The Site With Username "admin" And Password "admin"

Admin Creates A New Project
    Login To The Site With Username "admin" And Password "admin"
    Create Project With Name "Test Project"

Admin Changes The Name Of An Existing Project
    Login To The Site With Username "admin" And Password "admin"
    Create Project With Name "Test Project"
    Change Project With Name "Test Project" By Changing Name To "Test Project (Edited)"

Admin Creates A Project Charge
    Login To The Site With Username "admin" And Password "admin"
    Set Timezone To "America/New_York"
    Create Project With Name "Test Project"
    Create Charge For Project "Test Project" With Start Date "1970-01-01" And Time "09:00:00"

Admin Adds An End Time To An Existing Charge
    Login To The Site With Username "admin" And Password "admin"
    Set Timezone To "America/New_York"
    Create Project With Name "Test Project"
    Create Charge For Project "Test Project" With Start Date "1970-01-01" And Time "09:00:00"
    Change Charge With Project "Test Project" By Changing End Date To "1970-01-01" And End Time To "17:00:00"

Admin Views Project Charges On The Dashboard
    ${current_date} =    Get Current Date    result_format=%m/%d/%Y
    Login To The Site With Username "admin" And Password "admin"
    Set Timezone To "America/New_York"
    Create Project With Name "Test Project 1"
    Create Project With Name "Test Project 2"
    Create Charge For Project "Test Project 1" With Start Date "${current_date}" And Time "09:00:00"
    Change Charge With Project "Test Project 1" By Changing End Date To "${current_date}" And End Time To "13:00:00"
    Create Charge For Project "Test Project 2" With Start Date "${current_date}" and Time "13:00:00"
    Change Charge With Project "Test Project 2" By Changing End Date To "${current_date}" And End Time To "17:00:00"
    Go To Dashboard
    Checkbox Should Be Selected    Test Project 1
    Checkbox Should Be Selected    Test Project 2
    Unselect Checkbox    Test Project 1
    Click Button    Filter
    Checkbox Should Not Be Selected    Test Project 1
    Checkbox Should Be Selected    Test Project 2
    Unselect Checkbox    Test Project 2
    Select Checkbox    Test Project 1
    Click Button    Filter
    Checkbox Should Be Selected    Test Project 1
    Checkbox Should Not Be Selected    Test Project 2
