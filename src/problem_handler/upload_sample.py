import src.helper as helper
from src.problem_handler.clean_sample import clean_sample

'''
Requirement: Admin permission.

Description: Update the sample testcases of a tps problem to a TIOJ problem.

Return value: None.
'''
def upload_sample(problem, problem_id, tioj, settings):
    helper.throw_status(f"Uploading the sample of problem [bold]{problem.metadata['code']}[/bold] to TIOJ problem {problem_id}...")
   
    clean_sample(problem_id, tioj, settings)

    data = {}
    
    for i, name in enumerate(problem.samples):
        data[settings.tioj_instance.sample_input % i] = helper.read_file(name + settings.path.input_suffix)
        data[settings.tioj_instance.sample_destroy % i] = 'false'
        data[settings.tioj_instance.sample_output % i] = helper.read_file(name + settings.path.output_suffix)
    
    response = tioj.submit_form(settings.endpoints.edit_problem % problem_id, data=data)
    
    helper.throw_info(f"Completed upload the sample of problem [bold]{problem.metadata['code']}[/bold] to TIOJ problem {problem_id}.")
