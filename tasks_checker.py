import re

class TaskChecker:


    def __init__(self, solution, test_cases):
        self.solution = solution
        self.test_cases = test_cases


    def check(self):
        function_name = re.findall(r'def\s+(\w+)\s*\(',self.solution)[0]
        regex = re.compile('\n *')
        self.solution = regex.sub('\n    ',self.solution)
        print(self.solution)
        exec(self.solution, globals())
        func = globals()[function_name]

        num_passed_tests = 0

        for test_input,test_inputt, expected_output in self.test_cases:
            try:
                user_output = func(test_input,test_inputt)
                if user_output == expected_output:
                    num_passed_tests += 1
            except Exception:
                num_passed_tests = -1
        if num_passed_tests > 0:
            num_passed_tests = num_passed_tests / len(self.test_cases) * 100

        return num_passed_tests