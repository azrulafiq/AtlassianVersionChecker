from sub import *

jira_m_data = []
confl_m_data = []


jira_url = 'https://confluence.atlassian.com/jirasoftware/jira-software-release-notes-776821069.html'
confl_url = 'https://confluence.atlassian.com/doc/confluence-release-notes-327.html'
bamboo_url = 'https://confluence.atlassian.com/bamboo/bamboo-release-notes-671089224.html'
bitbucket_url = 'https://confluence.atlassian.com/bitbucketserver/release-notes-872139866.html'
jsm_url = 'https://confluence.atlassian.com/servicemanagement/jira-service-management-release-notes-780083086.html'
crowd_url = 'https://confluence.atlassian.com/crowd/crowd-release-notes-199094.html'
fisheye_url = 'https://confluence.atlassian.com/fisheye/fisheye-releases-960155725.html'
eol_url = 'https://confluence.atlassian.com/support/atlassian-support-end-of-life-policy-201851003.html'

# parsing html
confl_soup = parse_html(confl_url)
jira_soup = parse_html(jira_url)
bamboo_soup = parse_html(bamboo_url)
bitbucket_soup = parse_html(bitbucket_url)
jsm_soup = parse_html(jsm_url)
crowd_soup = parse_html(crowd_url)
fisheye_soup = parse_html(fisheye_url)
eol_soup = parse_html(eol_url)

# CONFLUENCE
confl_data = confl_soup.find_all('h4', {"id": lambda L: L and L.startswith('ConfluenceReleaseNotes')})
confl_eol = eol_soup.find('h2', {"id": lambda L: L and L.startswith('AtlassianSupportEndofLifePolicy-Confluence')}).next_sibling.text
confl_eol = confl_eol.split(')')

version_data = []
eol_data = []

push_CONFL_V_LTS(confl_data, version_data)
push_V_EOL(confl_eol, eol_data)

confl_m_data = merge_all_data(version_data, eol_data, confl_m_data)
confl_m_data = remove_empty_data(confl_m_data)

#JIRA
jira_data7 = jira_soup.find('h2', {"id": lambda L: L and L.startswith('JiraSoftwarereleasenotes-JiraSoftware8')}).next_sibling
jira_data7 = jira_data7.find_all('li')
jira_data8 = jira_soup.find('h2', {"id": lambda L: L and L.startswith('JiraSoftwarereleasenotes-JiraSoftware7')}).next_sibling
jira_data8 = jira_data8.find_all('li')

jira_eol7 = eol_soup.find('h2', {"id": lambda L: L and L.startswith('AtlassianSupportEndofLifePolicy-JiraSoftware')}).next_sibling.next_sibling.text
jira_eol7 = jira_eol7.split(')')
jira_eol8 = eol_soup.find('h2', {"id": lambda L: L and L.startswith('AtlassianSupportEndofLifePolicy-JiraSoftware')}).next_sibling.text
jira_eol8 = jira_eol8.split(')')

version_data = []
eol_data = []

push_JIRA_V_LTS(jira_data7, version_data)
push_JIRA_V_LTS(jira_data8, version_data)
push_V_EOL(jira_eol7, eol_data)
push_V_EOL(jira_eol8, eol_data)

# jira_m_data = merge_all_data(version_data, eol_data, jira_m_data)
# jira_m_data = remove_empty_data(jira_m_data)

# for a in version_data:
#     print(a['version'])

for a in version_data:
    item = {}
    item['version'] = a['version']
    print('Version: ' + str(item['version']))