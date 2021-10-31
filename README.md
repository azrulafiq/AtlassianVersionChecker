# atlassian version checker
Grab all Atlassian version info from release notes and compare with current running Atlassian services.

## Setup
- Python 2.7.x is required
- Clone the repo
  ```
  git clone https://github.com/azrulafiq/AtlassianVersionChecker.git && cd AtlassianVersionChecker
  ```
- Install requirements
  ```
  pip install -r requirement.txt
  ```

## Usage
- Grab version, end of life, and LTS status. Output is in json format as a files `confluence.json` and `jira.json`.
  ```
  python baseline/confluence.py
  python baseline/jira.py
  ```
- Get version from the Atlassian service via URL and do basic checking on version, EOL, and LTS based on json data produce from above script.
  ```
  python run/main.py
  ```
