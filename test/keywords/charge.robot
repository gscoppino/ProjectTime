*** Settings ***
Library             SeleniumLibrary
Library             chromedriver_binary

Resource            ./general.robot

*** Keywords ***
Create Charge For Project "${name}" With Start Date "${start_date}" and Time "${start_time}"
    Click Link                  //a[contains(text(), "Add") and @href="/project/charge/add/"]
    Title Should Be             Add charge | ProjectTime
    Select From List By Label   project         ${name}
    Input Text                  start_time_0    ${start_date}
    Input Text                  start_time_1    ${start_time}
    Click Button                Save
    Title Should Be             Select charge to change | ProjectTime
    Go To Home Page

Change Charge With Project "${name}" By Changing End Date To "${end_date}" And End Time To "${end_time}"
    Click Link                  //a[contains(text(), "Change") and @href="/project/charge/?closed__exact=0"]
    Title Should Be             Select charge to change | ProjectTime
    Click Link                  //table//a[contains(text(), "${name}")]
    Title Should Be             Change charge | ProjectTime
    Input Text                  end_time_0      ${end_date}
    Input Text                  end_time_1      ${end_time}
    Click Button                Save
    Title Should Be             Select charge to change | ProjectTime
    Go To Home Page
