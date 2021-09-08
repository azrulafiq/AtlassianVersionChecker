from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import json

maindata1 = []
maindata2 = []
finaldata = []

base_url1 = 'https://confluence.atlassian.com/jirasoftware/jira-software-release-notes-776821069.html'
base_url2 = 'https://confluence.atlassian.com/support/atlassian-support-end-of-life-policy-201851003.html'

html_doc1 = requests.get(base_url1).text
soup1 = BeautifulSoup(html_doc1, 'html5lib')

html_doc2 = requests.get(base_url2).text
soup2 = BeautifulSoup(html_doc2, 'html5lib')

raw_data8 = soup1.find('h2', {"id": lambda L: L and L.startswith(
    'JiraSoftwarereleasenotes-JiraSoftware8')}).next_sibling
collection_data8 = raw_data8.find_all('li')

raw_data7 = soup1.find('h2', {"id": lambda L: L and L.startswith(
    'JiraSoftwarereleasenotes-JiraSoftware7')}).next_sibling
collection_data7 = raw_data7.find_all('li')

raw_data1 = soup2.find('h2', {"id": lambda L: L and L.startswith(
    'AtlassianSupportEndofLifePolicy-JiraSoftware')}).next_sibling.next_sibling.text
jira1 = raw_data1.split(')')

raw_data2 = soup2.find('h2', {"id": lambda L: L and L.startswith(
    'AtlassianSupportEndofLifePolicy-JiraSoftware')}).next_sibling.text
jira2 = raw_data2.split(')')

print(jira1)

def push_V_LTS(collection_data):
    for data in collection_data:
        item = {}
        set_data = data.text
        set_data = set_data.replace('release notes', '')

        nonlts = re.findall('Jira Software\D\d.\d+', set_data)
        lts = re.findall(
            'Jira Software\D\d.\d+\s+LONG\sTERM\sSUPPORT', set_data)

        version_data = re.findall('\d+\.\d+', str(nonlts))
        for version in version_data:
            item['version'] = float(version)
            item['long term support'] = False
            # print('Version: ' + str(item['version']))
            # print('LTS: ' + str(item['long term support']))

        version_data = re.findall('\d+\.\d+', str(lts))
        for version in version_data:
            item['version'] = float(version)
            item['long term support'] = True
            # print('Version: ' + str(item['version']))
            # print('LTS: ' + str(item['long term support']))

        maindata1.append(item)

def push_V_EOL(collection_data):
    for set_data in collection_data:
        item = {}
        col_data = set_data.replace('(', '')
        col_data = col_data.replace(' ', '')
        # To match with datetime library
        col_data = col_data.replace('January', 'Jan')
        col_data = col_data.replace('February', 'Feb')
        col_data = col_data.replace('March', 'Mar')
        col_data = col_data.replace('April', 'Apr')
        col_data = col_data.replace('June', 'Jun')
        col_data = col_data.replace('July', 'Jul')
        col_data = col_data.replace('August', 'Aug')
        col_data = col_data.replace('September', 'Sep')
        col_data = col_data.replace('October', 'Oct')
        col_data = col_data.replace('November', 'Nov')
        col_data = col_data.replace('December', 'Dec')
        new_data = col_data.replace('EOLdate:', ' ')

        # Massage version data
        item['version'] = re.findall('\d+\.\d+', new_data)
        for version in item['version']:
            item['version'] = float(version)

        # Massage EOL data
        # Special Case 1
        date_v1 = re.findall('[A-Za-z]+\d+,\d+', new_data)
        for date in date_v1:
            item['eol'] = datetime.strptime(date, '%b%d,%Y')
            item['eol'] = str(item['eol'])
            
        # Special Case 2
        date_v2 = re.findall('\d+[A-Za-z]+,\d+', new_data)
        for date in date_v2:
            item['eol'] = datetime.strptime(date, '%d%b,%Y')
            item['eol'] = str(item['eol'])

        # store data
        maindata2.append(item)

push_V_LTS(collection_data8)
push_V_LTS(collection_data7)
push_V_EOL(jira2)
push_V_EOL(jira1)

set1 = list(filter(None, maindata1))
set2 = list(filter(None, maindata2))

for a in set1:
    item = {}
    # a['version']
    # item['product'] = 'Jira Software'  # optional
    item['version'] = a['version']
    item['long term support'] = a['long term support']
    item['eol'] = 'null' # No data from official site
    for b in set2:
        b['version']
        if b['version'] == a['version']:
            item['eol'] = b['eol']
    finaldata.append(item)

    # For Debug purpose
    # print('Version: ' + str(item['version']))
    # print('LTS: ' + str(item['long term support']))
    # print('EOL Date: ' + str(item['eol']))

# Output to Json
with open("jira.json", "w") as writeJSON:
    json.dump(finaldata, writeJSON, indent=4, ensure_ascii=False)