from os.path import basename

import src.helper as helper
from src.problem_handler.clean_testdata import clean_testdata

'''
Requirement: Admin permission.

Description: Update the testcases of a tps problem to a TIOJ problem.

Return value: None.
'''
def upload_testdata(problem, problem_id, tioj, settings):
    helper.throw_status(f"Uploading the testdata of problem [bold]{problem.metadata['code']}[/bold] to TIOJ problem {problem_id}...")
  
    clean_testdata(problem_id, tioj, settings)

    for i, name in enumerate(problem.testdata):
        helper.throw_status(f"Uploading testcase {basename(name)}...")

        data = {}
        files = {}
    
        files[settings.tioj_instance.input_file] = open(name + settings.path.input_suffix, 'rb')
        files[settings.tioj_instance.output_file] = open(name + settings.path.output_suffix, 'rb')
        data[settings.tioj_instance.time_limit] = str(int(float(problem.metadata['time_limit']) * 1000))
        data[settings.tioj_instance.vss_limit] = str(int(float(problem.metadata['memory_limit']) * 1024))
        if 'rss_limit' in problem.metadata:
            data[settings.tioj_instance.rss_limit] = str(int(float(problem.metadata['rss_limit']) * 1024))
        data[settings.tioj_instance.output_limit] = str(int(float(problem.metadata['output_limit']) * 1024))
    
        response = tioj.submit_form(settings.endpoints.create_testdata % problem_id, data=data, files=files)
    
    helper.throw_info(f"Completed upload the testdata of problem [bold]{problem.metadata['code']}[/bold] to TIOJ problem {problem_id}.")
