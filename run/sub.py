import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def parse_html(url):
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html5lib')
    return soup

def push_CONFL_V_LTS(collection_data, maindata):
    for confl in collection_data:
        item = {}
        lts = 'LONG TERM SUPPORT'

        item['version'] = confl.text.replace('Confluence ', '')

        if lts in item['version']:
            item['long term support'] = True
            item['version'] = item['version'].replace(lts, '')
            item['version'] = float(item['version'])
        else:
            item['long term support'] = False
            item['version'] = float(item['version'])
        maindata.append(item)

def push_JIRA_V_LTS(collection_data, maindata):
    for data in collection_data:
        item = {}
        set_data = data.text
        set_data = set_data.replace('release notes', '')
        nonlts = re.findall('Jira Software\D\d.\d+', set_data)
        lts = re.findall('Jira Software\D\d.\d+\s+LONG\sTERM\sSUPPORT', set_data)

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

        maindata.append(item)

def push_V_EOL(collection_data, maindata):
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
        newSet = re.findall('\d+\.\d+', new_data)
        for version in newSet:
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
        maindata.append(item)

def remove_empty_data(data):
    newSet = list(filter(None, data))
    return newSet

def merge_all_data(set1, set2, finaldata):
    for a in set1:
        item = {}
        item['version'] = a['version']
        item['long term support'] = a['long term support']
        item['eol'] = 'null' # No data from official site
        for b in set2:
            b['version']
            if b['version'] == a['version']:
                item['eol'] = b['eol']
        finaldata.append(item)
    return finaldata
