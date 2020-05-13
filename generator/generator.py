import math
from random import randint
from texttable import Texttable
from utils.utilities import show_message


class Generator:

    def __init__(self, database):
        self.students = []
        self.roles = []
        self.database = database
        self.month = ""

    def generate_roles_per_student(self, is_first):
        result = {}
        students_per_role = {}
        preemption = []
        self.students, self.roles = self.database.retrieve_actors()
        if not self._check_rules():
            show_message("Constraints not satisfied! Impossible to generate roles for each student!")
            return

        if is_first:
            self.month = self.database.months[0]
        else:
            self.month = self._find_next_month()
            if self.month is None:
                show_message("Generation ended! Reset all in order to start a new one!")
                return

            previous_results = self.database.retrieve_previous_results(self.month)
            if previous_results is None:
                return

            students_per_role, occurrences_per_student = self._create_dictionaries(previous_results)
            if not students_per_role or not occurrences_per_student:
                show_message("Error! Something went wrong in the computation!")
                return

            preemption = self._find_minimum_and_create_preemption_list(occurrences_per_student)
            if not preemption:
                show_message("Error! Something went wrong in the computation!")
                return
        for role in self.roles:
            result[role] = [self._find_leader(role, students_per_role, preemption)]
        self._find_vice(result)
        self._print_current_result(result)
        self._store_results(result)

    def _print_current_result(self, result):
        table = Texttable()
        rows = [["Role", "Master", "Vice"]]
        for role, student in result.items():
            rows.append([role, student[0], student[1]])
        table.add_rows(rows)
        with open('{}.txt'.format(self.month), 'w') as output_file:
            output_file.write(table.draw())

    def _find_leader(self, role, students_per_role, preemption):
        pos = randint(0, len(self.students)-1)

        if students_per_role:
            if preemption:
                num_preemption = len(preemption)
                for student in list(preemption):
                    if not self._is_role_already_done(student, role, students_per_role):
                        pos = self.students.index(student)
                        preemption.remove(student)
                        return self.students.pop(pos)

                if len(preemption) == num_preemption:
                    pos = self.students.index(preemption[0])
                    preemption.remove(preemption[0])
                    return self.students.pop(pos)

            counter = 30
            role_already_done = self._is_role_already_done(self.students[pos], role, students_per_role)
            while role_already_done and counter > 0:
                pos = randint(0, len(self.students)-1)
                role_already_done = self._is_role_already_done(self.students[pos], role, students_per_role)
                counter -= 1

        return self.students.pop(pos)

    def _find_vice(self, result):
        pos = 0
        roles_to_assign = len(self.roles)
        for student in list(self.students):
            cnt = math.ceil(roles_to_assign / len(self.students))
            for _ in range(cnt):
                value = list(result)[pos]
                result[value].append(student)
                pos += 1
                roles_to_assign -= 1
            self.students.remove(student)

    def _store_results(self, result):
        self.database.create_month_table(self.month)
        self.database.add_month_data(self.month, result)

    def _find_next_month(self):
        for month in self.database.months:
            if not self.database.are_tables_connected([month]):
                return month
        return None

    def _is_role_already_done(self, student, role, students_per_role):
        if self.month == "june":
            return False
        if student in students_per_role[role]:
            return True
        return False

    def _create_dictionaries(self, previous_results):
        students_per_role = {}
        occurrences_per_student = {}

        for student in self.students:
            occurrences_per_student[student] = 0

        for row in previous_results:
            fields = row.split(",")

            if fields[0] in students_per_role:
                students_per_role[fields[0]].append(fields[1])
            else:
                students_per_role[fields[0]] = [fields[1]]

            occurrences_per_student[fields[1]] += 1
        return students_per_role, occurrences_per_student

    def _check_rules(self):
        if len(self.students) >= 10 and \
                5 <= len(self.roles) < len(self.students) <= 2 * len(self.roles):
            return True
        return False

    @staticmethod
    def _find_minimum_and_create_preemption_list(occurrences_per_student):
        minimum = min(list(occurrences_per_student.values()))

        preemption = []
        for student, occ in occurrences_per_student.items():
            if occ == minimum:
                preemption.append(student)

        return preemption
