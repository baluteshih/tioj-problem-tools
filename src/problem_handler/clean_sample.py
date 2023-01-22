import re
import src.helper as helper

'''
Requirement: Admin permission.

Description: Remove all the sample testcase of a TIOJ problem.

Return value: None
'''
def clean_sample(problem_id, tioj, settings):
    helper.throw_status(f'Cleaning the sample of TIOJ problem {problem_id}...')

    data = {}
    
    form_data, submit_endpoint = tioj.get_form(settings.endpoints.edit_problem % problem_id)

    for column in form_data:
        if re.match(settings.tioj_instance.sample_destroy_regex, column) != None:
            data[column] = 1
      
    response = tioj.submit_form(settings.endpoints.edit_problem % problem_id, data=data)
