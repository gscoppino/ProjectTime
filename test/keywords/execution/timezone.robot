*** Settings ***
Library             SeleniumLibrary

*** Keywords ***
The site prompts the user for a timezone to use during their session
    Element Should Be Visible   //ul[@class="messagelist"]//li[@class="no_timezone_msg warning"]

The site no longer prompts the user for a timezone
    Element Should Not Be Visible    //ul[@class="messagelist"]//li[@class="no_timezone_msg warning"]

The user uses the "${name}" link to set their timezone to "${timezone}"
    Click Link                  //div[@id="header"]//a[text()="${name}"]
    Title Should Be             Change Timezone | Django site admin
    Select From List By Label   timezone    ${timezone}
    Click Button                Submit
    Title Should Be             ProjectTime Administration | ProjectTime

The user uses the timezone prompt to set their timezone to "${timezone}"
    Click Link                  //ul[@class="messagelist"]//li[@class="no_timezone_msg warning"]//a[contains(text(), "Change Timezone") and @href="/timezone"]
    Title Should Be             Change Timezone | Django site admin
    Select From List By Label   timezone    ${timezone}
    Click Button                Submit
    Title Should Be             ProjectTime Administration | ProjectTime
