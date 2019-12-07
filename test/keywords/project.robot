*** Settings ***
Library             SeleniumLibrary
Library             chromedriver_binary

Resource            ./general.robot

*** Keywords ***
Create Project With Name "${name}"
    Click Link          //a[contains(text(), "Add") and @href="/project/project/add/"]
    Title Should Be     Add project | ProjectTime
    Input Text          name    ${name}
    Click Button        Save
    Title Should Be     Select project to change | ProjectTime
    Go To Home Page

Change Project With Name "${name}" By Changing Name To "${new_name}"
    Click Link          //a[contains(text(), "Change") and @href="/project/project/?active__exact=1"]
    Title Should Be     Select project to change | ProjectTime
    Click Link          //table//a[contains(text(), "${name}")]
    Title Should Be     Change project | ProjectTime
    Input Text          name    ${new_name}
    Click Button        Save
    Title Should Be     Select project to change | ProjectTime
    Go To Home Page
