from sys import version
from bs4 import BeautifulSoup
import requests
import re
from datetime import date, datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()
base_url = os.getenv('ATLASSIAN_URL')
date_today = datetime.today()
html_doc = requests.get(base_url + '/rest/applinks/1.0/manifest').text
soup = BeautifulSoup(html_doc, 'xml')

running_version = soup.find('version').text

# massage into at least 2 decimal point and convert to float
running_version = re.findall('\d+\.\d+', running_version)[0]
running_version = float(running_version)

# simulate other versions
# running_version = 7.0

conf_file = open('confluence.json', 'r')
content = conf_file.read()
conf_content = json.loads(content)

for a in conf_content:
    if (running_version == a['version']):
        #print('Version ' + str(running_version) + ' is in the records')
        if (a['long term support'] == False):
            #do something like sending alert
            print('Version ' + str(running_version) + ' is not in LTS')
        else:
            print('Version ' + str(running_version) + ' is in LTS')
        if (a['eol'] == 'null'):
            #do something again
            print('No EOL date recorded, assume to exceed EOL date.')
        else:
            #again do something
            #print('EOL record is present')
            getdate = datetime.strptime(a['eol'], '%Y-%m-%d %H:%M:%S')
            if (date_today < getdate):
                print("Not exceed EOL date")
            else:
                print("Exceed EOL date, expired.")