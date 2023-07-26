import src.helper as helper

'''
Requirement: Logged in.

Description: Submit local program to problem "probem_id".

Return value: None.
'''
def submit_submission(problem_id, path, compiler, replace, tioj, settings):
    if not problem_id.isdigit():
        helper.throw_error('problem_id must be digits')
    problem_id = str(int(problem_id))
    
    helper.throw_status(f"Submit to TIOJ problem {problem_id} from {path} (compiler: {settings.tioj_instance.compiler_list[compiler - 1]})...")

    code = helper.read_file(path)
    for pattern, string in replace:
        code = code.replace(pattern, string) 

    data = {
        settings.tioj_instance.submission_compiler_id: compiler,
        settings.tioj_instance.submission_code: code 
    }

    response = tioj.submit_form(settings.endpoints.submit_problem % problem_id, data=data)

    helper.throw_info(f"Completed submit the {path} to TIOJ problem {problem_id}.")
