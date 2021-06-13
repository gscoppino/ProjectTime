*** Settings ***
Library           SeleniumLibrary

*** Keywords ***
The site prompts the user for a timezone to use during their session
    Page Should Contain    Select a timezone

The site no longer prompts the user for a timezone
    Page Should Not Contain    Select a timezone

The user uses the timezone prompt to set their timezone to "${timezone}"
    Select From List By Label    timezone    ${timezone}
    Click Button    Submit
    Title Should Be    ProjectTime | Dashboard
