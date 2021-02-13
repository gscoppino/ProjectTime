*** Settings ***
Library             SeleniumLibrary

*** Keywords ***
The user goes to the dashboard page
    Click Link          //a[contains(text(), "View Dashboard") and @href="/admin/dashboard"]
    Title Should Be     Dashboard | ProjectTime

The site displays the visualization canvas
    Page Should Contain           Monthly Summary
    Page Should Contain           Select Project(s):
    Page Should Contain Button    Filter
