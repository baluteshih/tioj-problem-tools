'''
source: https://github.com/ioi-2017/tps
'''
import src.helper as helper

class DataVisitor:
    def __init__(self):
        pass

    def on_include(self, testset_name, included_testset, line_number):
        pass

    def on_test(self, testset_name, test_name, line, line_number):
        pass

    def on_testset(self, testset_name, line_number):
        pass

    def on_subtask(self, subtask_name, line_number):
        pass

class DataParseError(Exception):
    def __init__(self, line_number, message):
        self.line_number = line_number
        self.message = message
        super().__init__(message)

class MappingVisitor(DataVisitor):
    def __init__(self):
        DataVisitor.__init__(self)
        self.tests_map = dict()
        self.subtasks = []

    def on_testset(self, testset_name, line_number):
        self.tests_map[testset_name] = set()

    def on_subtask(self, subtask_name, line_number):
        self.subtasks.append(subtask_name)

    def on_include(self, testset_name, included_testset, line_number):
        self.tests_map[testset_name] |= self.tests_map[included_testset]

    def on_test(self, testset_name, test_name, line, line_number):
        self.tests_map[testset_name].add(test_name)

    def print_mapping(self):
        for subtask in self.subtasks:
            print(subtask + ':', sorted(list(self.tests_map[subtask])))

def get_test_name(task_data, testset_name, testset_index, subtask_index, test_index, test_offset, gen_line): #pylint: disable=too-many-arguments
    #pylint: disable=unused-argument
    if task_data['type'] == "OutputOnly":
        return "%02d" % test_index
    return (testset_name if subtask_index < 0 else str(subtask_index)) + "-%02d" % test_offset

def parse_data_or_throw(gen_data, task_data, visitor):
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    """
    gen_data: list of lines in a gen/data file
    task_data: json of problem.json
    visitor: an instance of DataVisitor
    """

    line_number = 0

    testset_index, testset_name = -1, None
    subtask_index, subtask_counter = -1, -1
    test_index, test_offset = 1, -1
    defined_testsets = set()

    for line0 in gen_data:
        line = line0.strip('\n')
        line_number += 1

        if len(line.strip()) == 0 or line.strip().startswith("#"):
            continue

        command = line.strip().split()[0]
        args = line.strip().split()[1:]

        if command.startswith("@"):
            if command in ("@subtask", "@testset"):
                test_offset = 1
                testset_index += 1
                testset_name = args[0]
                defined_testsets.add(testset_name)
                visitor.on_testset(testset_name, line_number)
                if command == "@subtask":
                    visitor.on_subtask(testset_name, line_number)
                    subtask_counter += 1
                    subtask_index = subtask_counter
                else:
                    subtask_index = -1
            elif command == "@include":
                if testset_index < 0:
                    raise DataParseError(line_number, "No subtask/testset is defined.")

                for included_testset in args:
                    if included_testset not in defined_testsets:
                        raise DataParseError(line_number, "Undefined testset %s" % included_testset)
                    visitor.on_include(testset_name, included_testset, line_number)
            else:
                raise DataParseError(line_number, "Unknown command %s" % command)
        else:
            if testset_index < 0:
                raise DataParseError(line_number, "No subtask/testset is defined.")

            test_name = get_test_name(
                task_data=task_data,
                testset_name=testset_name,
                testset_index=testset_index,
                subtask_index=subtask_index,
                test_index=test_index,
                test_offset=test_offset,
                gen_line=line,
            )

            visitor.on_test(testset_name, test_name, line, line_number)

            test_index += 1
            test_offset += 1

def parse_data(gen_data, task_data, visitor):
    """
    gen_data: list of lines in a gen/data file
    task_data: json of problem.json
    visitor: an instance of DataVisitor
    """
    try:
        parse_data_or_throw(gen_data, task_data, visitor)
    except DataParseError as e:
        helper.throw_error("gen_file: Error on line #%d: %s\n" % (e.line_number, e.message))

def get_data_mapping(problem):
    mapping_visitor = MappingVisitor()
    parse_data(problem.gen_file, problem.metadata, mapping_visitor)
    return mapping_visitor
