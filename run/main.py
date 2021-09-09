from sub import *

# URL for atllasian product
jira_url = 'https://confluence.atlassian.com/jirasoftware/jira-software-release-notes-776821069.html'
confl_url = 'https://confluence.atlassian.com/doc/confluence-release-notes-327.html'
bamboo_url = 'https://confluence.atlassian.com/bamboo/bamboo-release-notes-671089224.html'
bitbucket_url = 'https://confluence.atlassian.com/bitbucketserver/release-notes-872139866.html'
jsm_url = 'https://confluence.atlassian.com/servicemanagement/jira-service-management-release-notes-780083086.html'
crowd_url = 'https://confluence.atlassian.com/crowd/crowd-release-notes-199094.html'
fisheye_url = 'https://confluence.atlassian.com/fisheye/fisheye-releases-960155725.html'
eol_url = 'https://confluence.atlassian.com/support/atlassian-support-end-of-life-policy-201851003.html'

# Main data set
jira_m_data = []
confl_m_data = []
bamboo_m_data = []
bitbucket_m_data = []
jsm_m_data = []
crowd_m_data = []
fisheye_m_data = []

# Parsing html
confl_soup = parse_html(confl_url)
jira_soup = parse_html(jira_url)
bamboo_soup = parse_html(bamboo_url)
bitbucket_soup = parse_html(bitbucket_url)
# crowd_soup = parse_html(crowd_url)
# fisheye_soup = parse_html(fisheye_url)
# jsm_soup = parse_html(jsm_url)
eol_soup = parse_html(eol_url)

# CONFLUENCE

# confl_data = confl_soup.find_all('h4', {"id": lambda L: L and L.startswith('ConfluenceReleaseNotes')})
# confl_eol = eol_soup.find('h2', {"id": lambda L: L and L.startswith('AtlassianSupportEndofLifePolicy-Confluence')}).next_sibling.text
# confl_eol = confl_eol.split(')')
# version_data = []
# eol_data = []
# push_CONFL_V_LTS(confl_data, version_data)
# push_V_EOL(confl_eol, eol_data)
# version_data = remove_empty_data(version_data)
# eol_data = remove_empty_data(eol_data)
# confl_m_data = merge_all_data(version_data, eol_data, confl_m_data)
# confl_m_data = remove_duplicates(confl_m_data)

# JIRA

# jira_data8 = jira_soup.find('h2', {"id": lambda L: L and L.startswith('JiraSoftwarereleasenotes-JiraSoftware7')}).next_sibling
# jira_data8 = jira_data8.find_all('li')
# jira_data7 = jira_soup.find('h2', {"id": lambda L: L and L.startswith('JiraSoftwarereleasenotes-JiraSoftware8')}).next_sibling
# jira_data7 = jira_data7.find_all('li')
# jira_eol = eol_soup.find('h2', {"id": lambda L: L and L.startswith('AtlassianSupportEndofLifePolicy-JiraSoftware')}).next_sibling.text
# jira_eol = jira_eol.split(')')
# version_data = []
# eol_data = []
# push_JIRA_V_LTS(jira_data8, version_data)
# push_JIRA_V_LTS(jira_data7, version_data)
# push_V_EOL(jira_eol, eol_data)
# version_data = remove_empty_data(version_data)
# eol_data = remove_empty_data(eol_data)
# jira_m_data = merge_all_data(version_data, eol_data, jira_m_data)
# jira_m_data = remove_duplicates(jira_m_data)

# BAMBOO

# bamboo_data8 = bamboo_soup.find('h2', {"id": lambda L: L and L.startswith('BambooReleaseNotes-Bamboo8releasenotes')}).next_sibling
# bamboo_data8 = bamboo_data8.find_all('li')
# bamboo_data7 = bamboo_soup.find('h2', {"id": lambda L: L and L.startswith('BambooReleaseNotes-Bamboo7releasenotes')}).next_sibling
# bamboo_data7 = bamboo_data7.find_all('li')
# bamboo_data6 = bamboo_soup.find('h2', {"id": lambda L: L and L.startswith('BambooReleaseNotes-Bamboo6releasenotes')}).next_sibling
# bamboo_data6 = bamboo_data6.find_all('li')
# bamboo_eol = eol_soup.find('h2', {"id": lambda L: L and L.startswith('AtlassianSupportEndofLifePolicy-Bamboo')}).next_sibling.text
# bamboo_eol = bamboo_eol.split(')')
# version_data = []
# eol_data = []
# push_BAMBOO_V_LTS(bamboo_data8, version_data)
# push_BAMBOO_V_LTS(bamboo_data7, version_data)
# push_BAMBOO_V_LTS(bamboo_data6, version_data)
# push_V_EOL(bamboo_eol, eol_data)
# version_data = remove_empty_data(version_data)
# eol_data = remove_empty_data(eol_data)
# bamboo_m_data = merge_all_data(version_data, eol_data, bamboo_m_data)
# bamboo_m_data = remove_duplicates(bamboo_m_data)

# BITBUCKET

bitbucket_data = bitbucket_soup.find_all('h2', {"id": lambda L: L and L.startswith('Releasenotes-Bitbucket')})
bitbucket_eol = eol_soup.find('h2', {"id": lambda L: L and L.startswith('AtlassianSupportEndofLifePolicy-Bamboo')}).next_sibling.text
bitbucket_eol = bitbucket_eol.split(')')

version_data = []
eol_data = []

push_BIT_V_LTS(bitbucket_data, version_data)
push_V_EOL(bitbucket_eol, eol_data)

version_data = remove_empty_data(version_data)
eol_data = remove_empty_data(eol_data)
bitbucket_m_data = merge_all_data(version_data, eol_data, bitbucket_m_data)
bitbucket_m_data = remove_duplicates(bitbucket_m_data)

for a in bitbucket_m_data:
    print(a)
