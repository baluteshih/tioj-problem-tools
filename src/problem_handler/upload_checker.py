import src.helper as helper

'''
Requirement: Admin permission.

Description: Update the checker of a tps problem to a TIOJ problem.

Return value: None.
'''
def upload_checker(problem, problem_id, tioj, settings):
    helper.throw_status(f"Uploading the checker of problem [bold]{problem.metadata['code']}[/bold] to TIOJ problem {problem_id}...")
    
    data = {}
    
    data[settings.tioj_instance.checker] = helper.read_file(problem.full_path(settings.path.checker))
    
    response = tioj.submit_form(settings.endpoints.edit_problem % problem_id, data=data)
    
    helper.throw_info(f"Completed upload the checker of problem [bold]{problem.metadata['code']}[/bold] to TIOJ problem {problem_id}.")
