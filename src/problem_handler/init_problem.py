import src.helper as helper
from src.problem_handler.Problem import Problem
from src.problem_handler.create_empty_problem import create_empty_problem

'''
Requirement: None.

Description: Generate the problem structure from the tps directory with verification. Replace problem_id if needed.

problem_id replacement:
- '': Replace by tioj_problem_id if it exists in problem.json.
- new: Replace by the created problem id returned from create_empty_problem.
- otherwise: Should be digits and will be remained.

Return value: The problem structure generated by the tps directory and the problem_id. 
'''
def init_problem(tps_directory, problem_id, tioj, settings):
    helper.throw_status(f'Parsing {tps_directory}...')

    problem = Problem(tps_directory, settings) 
    
    if problem_id == '':
        helper.throw_status('Found empty problem_id, trying to parse from problem.json...')
        if 'tioj_problem_id' in problem.metadata:
            problem_id = problem.metadata['tioj_problem_id']

    if problem_id == 'new':
        helper.throw_status(f'Assigning new problem_id...')
        problem_id = create_empty_problem(tioj, settings)

    if not problem_id.isdigit():
        helper.throw_error('problem_id must be digits')
    problem_id = str(int(problem_id))

    return problem, problem_id
