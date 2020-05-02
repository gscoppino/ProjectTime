*** Settings ***
Library             SeleniumLibrary

Resource            ../navigation/navigation.robot

*** Keywords ***
The site displays the charges list
    Title Should Be       Select charge to change | ProjectTime
    Page Should Contain         Select charge to change

The site displays "${charge name}" in the charges list
    Element Should Contain    css:#result_list    ${charge name}

The user goes to the charges list
    Navigate To The Charges List

The user creates a charge for "${name}" with start date "${start_date}" and start time "${start_time}"
    Navigate To The Add Charge Page
    Select From List By Label   project         ${name}
    Input Text                  start_time_0    ${start_date}
    Input Text                  start_time_1    ${start_time}
    Click Button                Save
    Title Should Be             Select charge to change | ProjectTime

The user creates a charge for "${name}" with start date "${start_date}", a start time of "${start_time}", and an end time of "${end_time}"
    Navigate To The Add Charge Page
    Select From List By Label   project         ${name}
    Input Text                  start_time_0    ${start_date}
    Input Text                  start_time_1    ${start_time}
    Input Text                  end_time_0      ${start_date}
    Input Text                  end_time_1      ${end_time}
    Click Button                Save
    Title Should Be             Select charge to change | ProjectTime

