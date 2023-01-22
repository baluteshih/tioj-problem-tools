import json
import jsonschema
from jsonschema import validate

import src.helper as helper

'''
Requirement: None.

Description: Parse and verify solutions.json of a tps problem and store it in the problem structure.

Return value: None.
'''
def verify_solutions(problem, settings):
    helper.throw_status(f'Parsing solutions.json...')
    
    problem.solutions = helper.read_json(problem.full_path(settings.path.solutions))
    schema = helper.read_json(settings.default.solutions_schema)
    try:
        validate(instance=problem.solutions, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        helper.throw_error(str(err))

    cnt = 0
    problem.model_solution = ''
    for solution in problem.solutions:
        if problem.solutions[solution]['verdict'] == settings.default.solution_code_verdict:
            cnt += 1
            problem.model_solution = solution

    if cnt == 0:
        helper.throw_error(f'Cannot find a solution code with verdict {settings.default.solution_code_verdict}')
    elif cnt > 1:
        helper.throw_error(f'More than one solution codes with verdict {settings.default.solution_code_verdict}')
    else:
        helper.throw_status(f'Found {settings.default.solution_code_verdict} [bold]{problem.model_solution}[/bold]')
