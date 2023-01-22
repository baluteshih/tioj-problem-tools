from bs4 import BeautifulSoup

import src.helper as helper

'''
Requirement: Admin permission.

Description: Remove all the testcases of a TIOJ problem.

Return value: None
'''
def clean_testdata(problem_id, tioj, settings):
    helper.throw_status(f'Cleaning the testdata of TIOJ problem {problem_id}...')
    
    while True:
        rel = tioj.get(settings.endpoints.testdata_list % problem_id)
        soup = BeautifulSoup(rel.text, "html.parser")
        token_name = soup.find('head').find('meta', {'name':'csrf-param'})['content']
        token = soup.find('head').find('meta', {'name':'csrf-token'})['content']

        data = {
            token_name: token
        }

        found = False
        for a in soup.find_all('a', href=True):
            if a.text == 'Destroy':
                href = a['href']
                data['_method'] = a['data-method']
                found = True
        
        if not found:
            break
        
        tioj.post(tioj.get_url(href), data=data)
        
