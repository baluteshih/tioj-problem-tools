import src.helper as helper

'''
Requirement: Admin permission.

Description: Update the header and grader of a tps problem to a TIOJ problem.

Return value: None.
'''
def upload_grader(problem, problem_id, tioj, settings):
    helper.throw_status(f"Uploading the header and grader of problem [bold]{problem.metadata['code']}[/bold] to TIOJ problem {problem_id}...")
    
    data = {}
    
    data[settings.tioj_instance.header] = helper.read_file(problem.full_path(settings.path.header % problem.metadata['code']))
    data[settings.tioj_instance.grader] = helper.read_file(problem.full_path(settings.path.grader))
    
    response = tioj.submit_form(settings.endpoints.edit_problem % problem_id, data=data)
    
    helper.throw_info(f"Completed upload the header and grader of problem [bold]{problem.metadata['code']}[/bold] to TIOJ problem {problem_id}.")
