from os.path import isfile

import src.helper as helper

# Replace the statement content to fit TIOJ's features.
def statement_filter(content, problem_id, problem):
    return content.replace('^', '^ ').replace(problem.metadata['code'] + '.h', 'lib%04d.h' % int(problem_id))

# Detect a statement file's existence and then add it into the form's data if it exists.
def add_statement(data, name, path, found_msg, problem_id, problem):
    if isfile(path):
        helper.throw_status(found_msg)
        data[name] = statement_filter(helper.read_file(path), problem_id, problem)

'''
Requirement: Admin permission.

Description: Parse problem.json and the statements. Upload them to a TIOJ problem.

Return value: None
'''
def edit_problem(problem, problem_id, tioj, settings):
    helper.throw_status(f"Editing the metadata of problem [bold]{problem.metadata['code']}[/bold] on TIOJ problem {problem_id}...")
    
    data = {}
    
    add_statement(data, settings.tioj_instance.description, problem.full_path(settings.path.description), 'Found Description!', problem_id, problem)
    add_statement(data, settings.tioj_instance.input, problem.full_path(settings.path.input), 'Found Input Format!', problem_id, problem)
    add_statement(data, settings.tioj_instance.output, problem.full_path(settings.path.output), 'Found Output Format!', problem_id, problem)
    add_statement(data, settings.tioj_instance.hints, problem.full_path(settings.path.hints), "Found Hints!", problem_id, problem)
    add_statement(data, settings.tioj_instance.source, problem.full_path(settings.path.source), 'Found Problem Source!', problem_id, problem)
   
    for prop in settings.tioj_instance.auto_parse.__dict__['_box_config']['__safe_keys']:
        if prop in problem.metadata:
            data[eval(f'settings.tioj_instance.auto_parse.{prop}')] = problem.metadata[prop]

    response = tioj.submit_form(settings.endpoints.edit_problem % problem_id, data=data)
    
    helper.throw_info(f"Completed edit the metadata of problem [bold]{problem.metadata['code']}[/bold] on TIOJ problem {problem_id}.")
