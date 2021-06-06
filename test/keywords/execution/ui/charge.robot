*** Settings ***
Library           SeleniumLibrary
Resource          ../../navigation/ui.robot

*** Keywords ***
The site displays the charges list
    Title Should Be    ProjectTime | Charges
    Page Should Contain    Charges

The site displays "${charge name}" in the charges list
    Element Should Contain    tag:table    ${charge name}

The user goes to the charges list
    Navigate To The Charges List
