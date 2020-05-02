*** Settings ***
Library    SeleniumLibrary

*** Keywords ***

The user clicks the "${locator}" link
    Click Link    ${locator}

The user clicks the "${locator}" button
    Click Button    ${locator}

The user types "${text}" into the "${locator}" text field
    Input Text    ${locator}    ${text}

The user selects "${option}" from the "${locator}" selection field
    Select From List By Label    ${locator}    ${option}

The user checks the "${locator}" checkbox
    Select Checkbox    ${locator}

The user unchecks the "${locator}" checkbox
    Unselect Checkbox    ${locator}

The user clears the "${locator}" text field
    Clear Element Text    ${locator}

The site displays the "${locator}" link
    Page Should Contain Link    ${locator}

The site displays the "${locator}" button
    Page Should Contain Button    ${locator}

The site displays the text "${text}"
    Page Should Contain    ${text}

The site displays the text "${text}" in the "${section}" section
    Element Should Contain    css:#${section}    ${text}    ignore_case=True

The site displays the "${locator}" text field
    Page Should Contain Textfield    ${locator}

The site displays the "${locator}" selection field
    Page Should Contain List    ${locator}

The site displays the "${locator}" checkbox
    Page Should Contain Checkbox    ${locator}

The site displays "${text}" in the "${locator}" text field
    Textfield Value Should Be    ${locator}    ${text}

The site displays the "${locator}" checkbox as checked
    Checkbox Should Be Selected    ${locator}

The site displays the "${locator}" checkbox as unchecked
    Checkbox Should Not Be Selected    ${locator}
