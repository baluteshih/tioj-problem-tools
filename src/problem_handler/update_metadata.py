import src.helper as helper

'''
Requirement: Admin permission.

Description: Update a single attribute of a TIOJ problem. The attribute should be listed in settings.tioj_instance.auto_parse.

Return value: None.
'''
def update_metadata(problem_id, attribute, content, tioj, settings):
    if not problem_id.isdigit():
        helper.throw_error('problem_id must be digits')
    problem_id = str(int(problem_id))
    
    helper.throw_status(f"Updating metadata of TIOJ problem {problem_id}...")

    if attribute not in settings.tioj_instance.auto_parse.__dict__['_box_config']['__safe_keys']:
        helper.throw_error(f'Cannot find attribute {attribute} in tioj_instance_settings.toml/tioj_instance.auto_parse.')

    data = {
        eval(f"settings.tioj_instance.auto_parse.{attribute}"): content
    }

    response = tioj.submit_form(settings.endpoints.edit_problem % problem_id, data=data)

    helper.throw_info(f"Completed update the attribute [bold]{attribute}[/bold] of TIOJ problem {problem_id}.")
