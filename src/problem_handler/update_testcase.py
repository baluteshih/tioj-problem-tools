from os.path import basename

import src.helper as helper
from src.problem_handler.get_data_endpointmap import get_data_endpointmap

'''
Requirement: Admin permission.

Description: Update the testcases of a tps problem to a TIOJ problem. When update_file is False, the function will only update the metadata of testcases (e.g. time limit).

Return value: None.
'''
def update_testcase(problem, problem_id, tioj, settings, update_file=True):
    helper.throw_status(f"Updating the testcase of problem [bold]{problem.metadata['code']}[/bold] to TIOJ problem {problem_id}...")

    data_endpointmap = get_data_endpointmap(problem_id, tioj, settings)

    for i, name in enumerate(problem.testdata):
        helper.throw_status(f"Updating testcase {basename(name)}...")

        data = {}
        deldata = []
        files = {}
  
        if update_file:
            files[settings.tioj_instance.input_file] = open(name + settings.path.input_suffix, 'rb')
            files[settings.tioj_instance.output_file] = open(name + settings.path.output_suffix, 'rb')
        else:
            dummy_file = ("", "", "application/octet-stream")
            files[settings.tioj_instance.input_file] = dummy_file
            files[settings.tioj_instance.output_file] = dummy_file 
            deldata.append(settings.tioj_instance.input_file)
            deldata.append(settings.tioj_instance.output_file)
        data[settings.tioj_instance.time_limit] = str(int(float(problem.metadata['time_limit']) * 1000))
        data[settings.tioj_instance.vss_limit] = str(int(float(problem.metadata['memory_limit']) * 1024))
        if 'rss_limit' in problem.metadata:
            data[settings.tioj_instance.rss_limit] = str(int(float(problem.metadata['rss_limit']) * 1024))
        data[settings.tioj_instance.output_limit] = str(int(float(problem.metadata['output_limit']) * 1024))
  
        if basename(name) in data_endpointmap:
            for endpoint in data_endpointmap[basename(name)]:
                response = tioj.submit_form(endpoint, data=data, deldata=deldata, files=files)
        else:
            helper.throw_status(f"Cannot find {basename(name)} on TIOJ problem {problem_id}, uploading...")
            if not update_file:
                files[settings.tioj_instance.input_file] = open(name + settings.path.input_suffix, 'rb')
                files[settings.tioj_instance.output_file] = open(name + settings.path.output_suffix, 'rb')
            response = tioj.submit_form(settings.endpoints.create_testdata % problem_id, data=data, files=files)
        
    helper.throw_info(f"Completed update the testcase of problem [bold]{problem.metadata['code']}[/bold] to TIOJ problem {problem_id}.")
