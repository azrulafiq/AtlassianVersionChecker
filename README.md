# atlassian version checker
 Grab all atlassian version info from release notes and compare with current running atllasian services.

Please install all the python module from the requirement.txt

confluence.py
jira.py
- grab version, end of life, and LTS status. Output is in json format as a file.

main.py
- get version from the attlasian service via URL and do basic checking on version, EOL, and LTS based on json data produce from above script.