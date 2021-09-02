from bs4 import BeautifulSoup
import requests
import re
import json

base_url1 = 'https://confluence.atlassian.com/jirasoftware/jira-software-release-notes-776821069.html'
maindata1 = []
html_doc = requests.get(base_url1).text
soup = BeautifulSoup(html_doc, 'html5lib')

# raw_data = soup.find_all('a', attrs={ 'data-macro-name' : 'sp-plaintextbody-link'})
raw_data8 = soup.find('h2', {"id": lambda L: L and L.startswith(
    'JiraSoftwarereleasenotes-JiraSoftware8')}).next_sibling
collection_data8 = raw_data8.find_all('li')

raw_data7 = soup.find('h2', {"id": lambda L: L and L.startswith(
    'JiraSoftwarereleasenotes-JiraSoftware7')}).next_sibling
collection_data7 = raw_data7.find_all('li')

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

push_V_LTS(collection_data8)
push_V_LTS(collection_data7)

res = list(filter(None, maindata1))

with open("jira_data.json", "w") as writeJSON:
    json.dump(res, writeJSON, indent=4, ensure_ascii=False)
