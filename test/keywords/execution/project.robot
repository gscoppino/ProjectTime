*** Settings ***
Library             SeleniumLibrary

Resource            ../navigation/navigation.robot

*** Keywords ***
The site displays the projects list
    Title Should Be       Select project to change | ProjectTime
    Page Should Contain         Select project to change

The site displays "${project name}" in the projects list
    Element Should Contain    css:#result_list    ${project name}

The site does not display "${project name}" in the projects list
    Element Should Not Contain    css:#result_list    ${project name}

The user goes to the projects list
    Navigate To The Project List

The user creates a project named "${name}"
    Navigate To The Add Project Page
    Input Text          name    ${name}
    Click Button        Save
    Title Should Be     Select project to change | ProjectTime
