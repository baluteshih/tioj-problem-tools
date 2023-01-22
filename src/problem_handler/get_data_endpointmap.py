from bs4 import BeautifulSoup

import src.helper as helper

'''
Requirement: Admin permission.

Description: Parse a TIOJ problem's testcase list. Collect all the edit endpoint for each testcase (use the file name for identification).

Return value: A dictionary with the testcase file name as key, the edit endpoint string array as value.
'''
def get_data_endpointmap(problem_id, tioj, settings):
    page = tioj.get(settings.endpoints.testdata_list % problem_id)
    soup = BeautifulSoup(page.text, "html.parser")
    trs = soup.find_all('tr')

    data_endpointmap = dict()
    for i in range(1, len(trs)):
        tds = trs[i].find_all('td')
        name = tds[1].text.split('.')[0]
        if name in data_endpointmap:
            data_endpointmap[name].append(tds[-1].find_all('a')[0]['href'])
        else:
            data_endpointmap[name] = [tds[-1].find_all('a')[0]['href']]

    return data_endpointmap
