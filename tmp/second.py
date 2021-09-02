from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import json

maindata2 = []

html_doc2 = requests.get(
    'https://confluence.atlassian.com/support/atlassian-support-end-of-life-policy-201851003.html').text
soup2 = BeautifulSoup(html_doc2, 'html5lib')
raw_data1 = soup2.find('h2', {"id": lambda L: L and L.startswith(
    'AtlassianSupportEndofLifePolicy-JiraSoftware')}).next_sibling.next_sibling.text

raw_data2 = soup2.find('h2', {"id": lambda L: L and L.startswith(
    'AtlassianSupportEndofLifePolicy-JiraSoftware')}).next_sibling.text

jira1 = raw_data1.split(')')
jira2 = raw_data2.split(')')

def pushdata(collection_data):
    for set_data in collection_data:
        item = {}
        col_data = set_data.replace('(', '')
        col_data = col_data.replace(' ', '')
        # To match with datetime library
        col_data = col_data.replace('June', 'Jun')
        col_data = col_data.replace('October', 'Oct')
        col_data = col_data.replace('September', 'Sep')
        col_data = col_data.replace('December', 'Dec')
        col_data = col_data.replace('March', 'Mar')
        col_data = col_data.replace('February', 'Feb')
        col_data = col_data.replace('November', 'Nov')
        col_data = col_data.replace('July', 'Jul')
        col_data = col_data.replace('August', 'Aug')
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

pushdata(jira2)
pushdata(jira1)

# Output to Json
with open("jira_eol.json", "w") as writeJSON:
    json.dump(maindata2, writeJSON, indent=4, ensure_ascii=False)