import json
import jsonschema
from jsonschema import validate

import src.helper as helper

'''
Requirement: None.

Description: Parse and verify problem.json of a tps problem and store it in the problem structure.

Return value: None.
'''
def verify_metadata(problem, settings):
    helper.throw_status(f'Parsing problem.json...')
    
    problem.metadata = helper.read_json(problem.full_path(settings.path.metadata))
    schema = helper.read_json(settings.default.metadata_schema)
    try:
        validate(instance=problem.metadata, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        helper.throw_error(str(err))
    
    for prop in schema['properties']:
        if (prop not in problem.metadata) and ('default' in schema['properties'][prop]):
            problem.metadata[prop] = schema['properties'][prop]['default']

    # Use old special judge by default if no specjudge_type be appointed.
    if problem.metadata['has_checker'] and problem.metadata['specjudge_type'] == 'none':
         problem.metadata['specjudge_type'] = 'old'
    if problem.metadata['specjudge_type'] != 'none':
        helper.throw_status(f"Found special judge type: {problem.metadata['specjudge_type']}")

    if problem.metadata['has_grader']:
        problem.metadata['interlib_type'] = 'header'
    if problem.metadata['interlib_type'] != 'none':
        helper.throw_status(f"Found interactive library type: {problem.metadata['interlib_type']}")
    
    if problem.metadata['title'] == '':
        helper.throw_warning('Empty title.')
