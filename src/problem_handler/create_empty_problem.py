import src.helper as helper

'''
Requirement: Admin permission.

Description: Create an empty problem on TIOJ, invisible by default. 

Return value: The created problem id.
'''
def create_empty_problem(tioj, settings):
    helper.throw_status('Creating empty problem...')
    response = tioj.submit_form(settings.endpoints.create_problem, data={
        'problem[visible_state]': 'invisible'
    })
    problem_id = response.url.split('/')[-1]
    helper.throw_info(f'Successfully create an empty problem! (id: {problem_id})')
    return problem_id
