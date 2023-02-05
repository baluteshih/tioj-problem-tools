import glob

import src.helper as helper

'''
Requirement: None.

Description: Parse and verify testcases of a tps problem and store the file names of them in the problem structure.

Return value: None.
'''
def verify_testdata(problem, settings):

    helper.throw_status(f'Parsing testdata...')
    
    inputs = glob.glob(problem.full_path(settings.path.testdata + settings.path.input_suffix))
    outputs = glob.glob(problem.full_path(settings.path.testdata + settings.path.output_suffix))

    input_name = set(s[:-len(settings.path.input_suffix)] for s in inputs) 
    output_name = set(s[:-len(settings.path.output_suffix)] for s in outputs) 

    for testcase in input_name:
        if testcase not in output_name:
            helper.throw_error(f'{testcase}{settings.path.input_suffix} does not have a matched output.')

    for testcase in output_name:
        if testcase not in input_name:
            helper.throw_error(f'{testcase}{settings.path.output_suffix} does not have a matched input.')

    problem.testdata = list(input_name)
    problem.testdata.sort()

    if len(problem.testdata) > 0:
        helper.throw_status(f'Found {len(problem.testdata)} testcases.')
    else:
        helper.throw_warning('Didn\'t find any testdata.')
