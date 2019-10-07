*** Settings ***
Library             SeleniumLibrary
Library             chromedriver_binary

*** Keywords ***
Log Out Of Site
    Click Link          //a[contains(text(), "Log out") and @href="/logout/"]
    Title Should Be     Logged out | ProjectTime
    Close Browser
