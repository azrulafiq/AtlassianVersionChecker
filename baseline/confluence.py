from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import json

data1 = []
data2 = []
maindata = []
lts = 'LONG TERM SUPPORT'

### Get Version and LTS status ###
html_doc = requests.get(
    'https://confluence.atlassian.com/doc/confluence-release-notes-327.html').text
soup = BeautifulSoup(html_doc, 'html5lib')
collection_data = soup.find_all(
    'h4', {"id": lambda L: L and L.startswith('ConfluenceReleaseNotes')})

for confl in collection_data:
    item = {}
    item['version'] = confl.text.replace('Confluence ', '')

    if lts in item['version']:
        item['long term support'] = True
        item['version'] = item['version'].replace(lts, '')
        item['version'] = float(item['version'])
    else:
        item['long term support'] = False
        item['version'] = float(item['version'])
    data1.append(item)
### Get Version and LTS status ###

### Get Version and EOL date ###
html_doc2 = requests.get(
    'https://confluence.atlassian.com/support/atlassian-support-end-of-life-policy-201851003.html').text
soup2 = BeautifulSoup(html_doc2, 'html5lib')
raw_data = soup2.find('h2', {"id": lambda L: L and L.startswith(
    'AtlassianSupportEndofLifePolicy-Confluence')}).next_sibling.text

collection_data = raw_data.split(')')

for set_data in collection_data:
    item = {}
    col_data = set_data.replace('(', '')
    col_data = col_data.replace(' ', '')
    # To match with datetime library
    col_data = col_data.replace('June', 'Jun')
    new_data = col_data.replace('EOLdate:', ' ')

    # Massage version data
    item['version'] = re.findall('\d+\.\d+', new_data)
    for version in item['version']:
        item['version'] = float(version)

    # Massage EOL data
    item['eol'] = re.findall('[A-Za-z]+\d+,\d+', new_data)
    for date in item['eol']:
        item['eol'] = re.findall('[A-Za-z]+\d+,\d+', new_data)
        item['eol'] = datetime.strptime(date, '%b%d,%Y')
        item['eol'] = str(item['eol'])

    # store data
    data2.append(item)
### Get Version and EOL date ###

### Merge Data1 and Data2 ###

for a in data1:
    item = {}
    a['version']
    item['product'] = 'Confluence'  # optional
    item['version'] = a['version']
    item['long term support'] = a['long term support']
    item['eol'] = 'null' # No data from official site
    for b in data2:
        b['version']
        if b['version'] == a['version']:
            item['eol'] = b['eol']
    maindata.append(item)

    # For Debug purpose
    # print('Version: ' + str(item['version']))
    # print('LTS: ' + str(item['long term support']))
    # print('EOL Date: ' + str(item['eol']))

# Output to Json
with open("confluence.json", "w") as writeJSON:
    json.dump(maindata, writeJSON, indent=4, ensure_ascii=False)