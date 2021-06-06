*** Settings ***
Library           SeleniumLibrary
Resource          ../../navigation/ui.robot

*** Keywords ***
The site displays the projects list
    Title Should Be    ProjectTime | Projects
    Page Should Contain    Projects

The site displays "${project name}" in the projects list
    Element Should Contain    tag:table    ${project name}

The user goes to the projects list
    Navigate To The Project List

The user creates a project named "${name}"
    Navigate To The Add Project Page
    Input Text    name    ${name}
    Click Button    Submit
    Title Should Be    ProjectTime | Projects
