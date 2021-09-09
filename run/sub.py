import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def parse_html(url):
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'lxml') # lxml for fast processing, html5lib
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

def push_BIT_V_LTS(collection_data, maindata):
    for confl in collection_data:
        item = {}
        lts = ' (Long Term Support release)'
        confl = confl.text

        confl = confl.replace('Bitbucket Data Center and Server ', '')
        confl = confl.replace('Bitbucket Server and Data Center ', '')
        confl = confl.replace('Bitbucket Server ', '')
        item['version'] = confl

        # print('Version: ' + str(item['version']))

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

def push_BAMBOO_V_LTS(collection_data, maindata):
    for data in collection_data:
        item = {}
        set_data = data.text
        set_data = set_data.replace('release notes', '')
        nonlts = re.findall('Bamboo\D\d.\d+', set_data)

        version_data = re.findall('\d+\.\d+', str(nonlts))
        for version in version_data:
            item['version'] = f"{version:.2f}"
            item['long term support'] = False
            # print('Version: ' + str(item['version']))
            # print('LTS: ' + str(item['long term support']))

        maindata.append(item)

def push_V_EOL(collection_data, maindata):
    for set_data in collection_data:
        item = {}
        set_data = set_data.replace('(', '')
        set_data = set_data.replace(' ', '')
        # To match with datetime library
        set_data = set_data.replace('January', 'Jan')
        set_data = set_data.replace('February', 'Feb')
        set_data = set_data.replace('March', 'Mar')
        set_data = set_data.replace('April', 'Apr')
        set_data = set_data.replace('June', 'Jun')
        set_data = set_data.replace('July', 'Jul')
        set_data = set_data.replace('August', 'Aug')
        set_data = set_data.replace('September', 'Sep')
        set_data = set_data.replace('October', 'Oct')
        set_data = set_data.replace('November', 'Nov')
        set_data = set_data.replace('December', 'Dec')
        new_data = set_data.replace('EOLdate:', ' ')

        # Massage version data
        newSet = re.findall('\d+\.\d+', new_data)
        for version in newSet:
            item['version'] = float(version)

        # Massage EOL data
        # Special Case 1 (Conflunce)
        date_v1 = re.findall('[A-Za-z]+\d+,\d+', new_data)
        for date in date_v1:
            item['eol'] = datetime.strptime(date, '%b%d,%Y')
            item['eol'] = str(item['eol'])
            
        # Special Case 2 (Jira, Confluence)
        date_v2 = re.findall('\d+[A-Za-z]+,\d+', new_data)
        for date in date_v2:
            item['eol'] = datetime.strptime(date, '%d%b,%Y')
            item['eol'] = str(item['eol'])

        # Special Case 3 (Bamboo)
        date_v3 = re.findall('\s\d+[A-Za-z]+\d+', new_data)
        for date in date_v3:
            item['eol'] = datetime.strptime(date, ' %d%b%Y')
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

def remove_duplicates(data):
    res = []
    for i in data:
        if i not in res:
            res.append(i)
    return res
