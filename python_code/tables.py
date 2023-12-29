#tables

from tabulate import tabulate

class Table():
    def __init__(self):
        pass
    def print_table(self, CALCULATOR):
        a = CALCULATOR.get_overall_GPA()
        tt_list = [["overall", "", "", "", "", "", "", CALCULATOR.get_overall_letter_grade(a), str(a)]]
        for semester in CALCULATOR.get_semesters(): # semester keys
            tt_list.append(["", semester, "", "", "", "", str(round(CALCULATOR.get_semester_grade(semester), 2)) + "%", CALCULATOR.get_semester_letter_grade(semester), str(CALCULATOR.get_semester_GPA(semester))])
            for course in CALCULATOR.get_courses(semester):
                tt_list.append(["", "", course, "", "", "", str(round(CALCULATOR.get_course_grade(semester, course), 2)) + "%", CALCULATOR.get_course_letter_grade(semester, course), str(CALCULATOR.get_course_GPA(semester, course))])
                for section in CALCULATOR.get_sections(semester, course):
                    tt_list.append(["", "", "", section, "", CALCULATOR.get_section_weight(semester, course, section), str(round(CALCULATOR.get_section_grade(semester, course, section), 2)) + "%", CALCULATOR.get_section_letter_grade(semester, course, section), str(CALCULATOR.get_section_GPA(semester, course, section))])
                    for subsection in CALCULATOR.get_subsections(semester, course, section):
                        tt_list.append(["", "", "", "", subsection, CALCULATOR.get_subsection_weight(semester, course, section, subsection), str(round(CALCULATOR.get_subsection_grade(semester, course, section, subsection), 2)) + "%", CALCULATOR.get_subsection_letter_grade(semester, course, section, subsection), str(CALCULATOR.get_subsection_GPA(semester, course, section, subsection))])

        header_list = ["OVERALL", "SEMESTER", "COURSE", "SECTION", "SUBSECTION", "WEIGHT", "GRADE", "LETTER GRADE", "GPA"]
        print(tabulate(tt_list, headers = header_list, tablefmt="simple_outline"))
    def tab(self, CALCULATOR):
        a = CALCULATOR.get_overall_GPA()
        tt_list = [["overall", "", "", "", "", "", "", CALCULATOR.get_overall_letter_grade(a), str(a)]]
        for semester in CALCULATOR.get_semesters(): # semester keys
            tt_list.append(["", semester, "", "", "", "", str(round(CALCULATOR.get_semester_grade(semester), 2)) + "%", CALCULATOR.get_semester_letter_grade(semester), str(CALCULATOR.get_semester_GPA(semester))])
            for course in CALCULATOR.get_courses(semester):
                tt_list.append(["", "", course, "", "", "", str(round(CALCULATOR.get_course_grade(semester, course), 2)) + "%", CALCULATOR.get_course_letter_grade(semester, course), str(CALCULATOR.get_course_GPA(semester, course))])
                for section in CALCULATOR.get_sections(semester, course):
                    tt_list.append(["", "", "", section, "", CALCULATOR.get_section_weight(semester, course, section), str(round(CALCULATOR.get_section_grade(semester, course, section), 2)) + "%", CALCULATOR.get_section_letter_grade(semester, course, section), str(CALCULATOR.get_section_GPA(semester, course, section))])
                    for subsection in CALCULATOR.get_subsections(semester, course, section):
                        tt_list.append(["", "", "", "", subsection, CALCULATOR.get_subsection_weight(semester, course, section, subsection), str(round(CALCULATOR.get_subsection_grade(semester, course, section, subsection), 2)) + "%", CALCULATOR.get_subsection_letter_grade(semester, course, section, subsection), str(CALCULATOR.get_subsection_GPA(semester, course, section, subsection))])

        header_list = ["OVERALL", "SEMESTER", "COURSE", "SECTION", "SUBSECTION", "WEIGHT", "GRADE", "LETTER GRADE", "GPA"]
        return tabulate(tt_list, headers = header_list, tablefmt="simple_outline")