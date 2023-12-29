#calculator_class.py

class Calculator():
    def __init__(self):
            self.__SEMESTERS = {} # dict of semesters, key = semester name, value = Semester
            self.__OVERALL_LETTER_GRADE = "F"
            self.__OVERALL_GPA = 0 

    def __grade_to_letter(self, grade):
        if grade >= 85:
            return "A"
        elif grade >= 80:
            return "A-"
        elif grade >= 75:
            return "B+"
        elif grade >= 70:
            return "B"
        elif grade >= 65:
            return "B-"
        elif grade >= 60:
            return "C+"
        elif grade >= 55:
            return "C"
        elif grade >= 50:
            return "D"
        else:
            return "F"
    def __grade_to_GPA(self, grade):
        if grade >= 85:
            return 4.0
        elif grade >= 80:
            return 3.7
        elif grade >= 75:
            return 3.3
        elif grade >= 70:
            return 3.0
        elif grade >= 65:
            return 2.7
        elif grade >= 60:
            return 2.3
        elif grade >= 55:
            return 2.0
        elif grade >= 50:
            return 1.7
        else:
            return 0.0
    def __gpa_to_letter(self, GPA):
        if GPA >= 4.0:
            return "A"
        elif GPA >= 3.7:
            return "A-"
        elif GPA >= 3.3:
            return "B+"
        elif GPA >= 3.0:
            return "B"
        elif GPA >= 2.7:
            return "B-"
        elif GPA >= 2.3:
            return "C+"
        elif GPA >= 2.0:
            return "C"
        elif GPA >= 1.7:
            return "D"
        else:
            return "F"
        
    def __get_overall_GPA(self, semesters): # given a dict of semesters, return overall GPA
        overall_GPA = 0
        if len(semesters) == 0:
            return 0
        for sem in semesters.values():
            overall_GPA += self.__grade_to_GPA(self.__get_semester_grade(sem))
        return overall_GPA/len(semesters)
    def __get_semester_grade(self, semester): # given semester, return semester grade
        semester_grade = 0
        if len(semester.courses) == 0:
            return 0
        for course in semester.courses.values():
            semester_grade += self.__get_course_grade(course)
        return semester_grade/len(semester.courses)
    def __get_course_grade(self, course): # given course, return course grade
        course_grade = 0
        for section in course.sections.values():
            course_grade += self.__get_section_grade(section)
        return course_grade
    def __get_section_grade(self, sections): # given section, return section grade
        section_grade = 0
        for subsection in sections.subsections.values():
            section_grade += subsection.weighted_grade
        return section_grade
    def __get_section_grade_percentage(self, sections): # given section, return section grade
        section_grade = 0
        if len(sections.subsections) == 0:
            return 0
        for subsection in sections.subsections.values():
            section_grade += subsection.grade
        return section_grade/len(sections.subsections)

    class __Grade():
        def __init__(self, grade_name, grade_weight, grade):
            self.grade_name = grade_name # assignment 1/2/3...
            self.grade_weight = grade_weight # weight % of subsection
            self.grade = grade # % percentage received
            self.weighted_grade = self.calculate(grade_weight, grade) # grade * weight / 100
        def g_grade_update(self, new_grade):
            self.grade = new_grade
            self.weighted_grade = self.calculate(self.grade_weight, self.grade)
        # calculate grade given percentage and weight
        def calculate(self, weight, grade): # use this to calculate grade for sections and subsections
            return (grade * weight) / 100 
    class __Section():
        def __init__(self, section_name, section_grade, section_weight, subsections, course):
            self.section_name = section_name # assignments/midterm/final...
            #self.section_grade = section_grade # subsection grades added together (calculated with weight - max summed to weight)
            self.section_weight = section_weight # weight % of section
            self.subsections = subsections # dict of grades in section, keys are subsection names, values are Grade objects
        def add_subsection(self, grade_name, grade_weight, grade):
            self.subsections[grade_name] = Calculator._Calculator__Grade(grade_name, grade_weight, grade)
        def remove_subsection(self, grade_name):
            for sub in self.subsections.copy():
                if sub == grade_name:
                    del self.subsections[grade_name]
                    return True #print("Subsection removed")
            return False #print("Subsection not found")
        def edit_subsection(self, grade_name, new_grade): # edit subsection grade
            for sub in self.subsections.values():
                if sub.grade_name == grade_name:
                    sub.g_grade_update(new_grade) # update grade
                    return True #print("Subsection updated")
            return False #print("Subsection not found")
    class __Course():
        def __init__(self, course_code, curr_grade, semester): 
            self.course_code = course_code # eg. comp424
            self.sections = {} # sections, key = section name, value = Section
        def __str__(self): # print course code
            return self.course_code
        def add_section(self, section_name, section_weight, section_grade, subsections): # add section
            self.sections[section_name] = Calculator._Calculator__Section(section_name, section_grade, section_weight, subsections, self)
        def remove_section(self, section_name): # remove section
            if section_name in self.sections.copy():
                del self.sections[section_name]
                return True #print("Section removed")
            return False #print("Section not found")
        def edit_section(self, section_name, subsection_name, new_grade): # edit subsection grade
            if section_name in self.sections:
                self.sections[section_name].edit_subsection(subsection_name, new_grade)
    class __Semester():
        def __init__(self, semester_name, courses, semester_grade):
            self.semester_name = semester_name # fall/winter/summer year - eg. fall2020
            self.courses = courses # dict of courses, key = course code, value = Course
        def __str__(self): # print semester name
            return self.semester_name
        def add_course(self, course_name, course_grade): # add course
            self.courses[course_name] = Calculator._Calculator__Course(course_name, course_grade, self)
        def remove_course(self, course):
            if course in self.courses.copy():    
                del self.courses[course]
                return True #print("Course removed")
            return False #print("Course not found")


    def get_semesters(self):
        return self.__SEMESTERS.keys()
    def get_courses(self, semester_name):
        return self.__SEMESTERS[semester_name].courses.keys()
    def get_sections(self, semester_name, course_name):
        return self.__SEMESTERS[semester_name].courses[course_name].sections.keys()
    def get_subsections(self, semester_name, course_name, section_name):
        return self.__SEMESTERS[semester_name].courses[course_name].sections[section_name].subsections.keys()
    #semester functions    
    def add_semester(self, semester_name): # add semester (empty semester)
        courses = {}
        semester_grade = 0
        self.__SEMESTERS[semester_name] = self.__Semester(semester_name, courses, semester_grade)
        print("Semester added.")
    def print_semesters(self):
        for sem in self.__SEMESTERS.keys():
            print(sem)
    def remove_semester(self, semester_name): # remove semester
        if semester_name in self.__SEMESTERS.copy():
            del self.__SEMESTERS[semester_name]
            return True, "Semester removed."
        return False, "Semester not found. Please try again."
    def change_semester_name(self, semester_name, new_semester_name): # change semester name
        if semester_name in self.__SEMESTERS.copy():
            self.__SEMESTERS[new_semester_name] = self.__SEMESTERS[semester_name]
            del self.__SEMESTERS[semester_name]
            return True, "Semester name changed."
        return False, "Semester not found. Please try again."
    def check_semester(self, semester_name): # check if semester exists
        if semester_name in self.__SEMESTERS.copy():
            return True, ""
        return False, "Semester not found. Please try again."
    #course functions
    def add_course(self, semester_name, course_name): # add course (empty course)
        course_grade = 0
        self.__SEMESTERS[semester_name].add_course(course_name, course_grade)
        return "Course added."
    def print_courses(self, semester_name): # print courses in semester
        for c in self.__SEMESTERS[semester_name].courses.keys():
            print(c)
    def remove_course(self, semester_name, course_name): # remove course
        if self.__SEMESTERS[semester_name].remove_course(course_name):
            return "Course removed."
    def check_course(self, semester_name, course_name):
        if course_name in self.__SEMESTERS[semester_name].courses.copy():
            return True, ""
        return False, "Course not found. Please try again."
    def change_course_name(self, semester_name, course_name, new_course_name): # change course name
        self.__SEMESTERS[semester_name].courses[new_course_name] = self.__SEMESTERS[semester_name].courses[course_name]
        del self.__SEMESTERS[semester_name].courses[course_name]
        return "Course name changed."
    #section functions
    def add_section(self, semester_name, course_name, section_name, section_weight): # add section
        section_grade = 0
        subsections = {}
        self.__SEMESTERS[semester_name].courses[course_name].add_section(section_name, section_weight, section_grade, subsections)
        return "Section added."
    def print_sections(self, semester_name, course_name): # print sections in course
        for s in self.__SEMESTERS[semester_name].courses[course_name].sections.keys():
            print(s)
    def remove_section(self, semester_name, course_name, section_name): # remove section
        if self.__SEMESTERS[semester_name].courses[course_name].remove_section(section_name):
            return "Section removed."
    def check_section(self, semester_name, course_name, section_name): # check if section exists
        if section_name in self.__SEMESTERS[semester_name].courses[course_name].sections.copy():
            return True, ""
        return False, "Section not found. Please try again."
    def change_section_name(self, semester_name, course_name, section_name, new_section_name): # change section name
        self.__SEMESTERS[semester_name].courses[course_name].sections[new_section_name] = self.__SEMESTERS[semester_name].courses[course_name].sections[section_name]
        del self.__SEMESTERS[semester_name].courses[course_name].sections[section_name]
        return "Section name changed."
    #subsection functions
    def add_subsection(self, semester_name, course_name, section_name, subsection_name, subsection_weight, subsection_grade): # add subsection
        self.__SEMESTERS[semester_name].courses[course_name].sections[section_name].add_subsection(subsection_name, subsection_weight, subsection_grade)
        return "Subsection added."
    def print_subsections(self, semester_name, course_name, section_name): # print subsections in section
        for sub in self.__SEMESTERS[semester_name].courses[course_name].sections[section_name].subsections.keys():
            print(sub)
    def remove_subsection(self, semester_name, course_name, section_name, subsection_name): # remove subsection
        if self.__SEMESTERS[semester_name].courses[course_name].sections[section_name].remove_subsection(subsection_name):
            return "Subsection removed."
    def check_subsection(self, semester_name, course_name, section_name, subsection_name): # check if subsection exists
        if subsection_name in self.__SEMESTERS[semester_name].courses[course_name].sections[section_name].subsections.copy():
            return True, ""
        return False, "Subsection not found. Please try again."
    def change_subsection_name(self, semester_name, course_name, section_name, subsection_name, new_subsection_name): # change subsection name
        self.__SEMESTERS[semester_name].courses[course_name].sections[section_name].subsections[new_subsection_name] = self.__SEMESTERS[semester_name].courses[course_name].sections[section_name].subsections[subsection_name]
        del self.__SEMESTERS[semester_name].courses[course_name].sections[section_name].subsections[subsection_name]
        return "Subsection name changed."
    def edit_subsection_grade(self, semester_name, course_name, section_name, subsection_name, new_grade): # edit subsection grade
        if self.__SEMESTERS[semester_name].courses[course_name].sections[section_name].edit_subsection(subsection_name, new_grade):
            return "Subsection grade updated."
    def get_overall_GPA(self):
        return self.__get_overall_GPA(self.__SEMESTERS)
    def get_overall_letter_grade(self, GPA): # get overall letter grade
        return self.__gpa_to_letter(GPA)
    def get_semester_grade(self, semester_name): # get semester grade
        return self.__get_semester_grade(self.__SEMESTERS[semester_name])
    def get_semester_letter_grade(self, semester_name): # get semester letter grade
        return self.__grade_to_letter(self.__get_semester_grade(self.__SEMESTERS[semester_name]))
    def get_semester_GPA(self, semester_name): # get semester GPA
        return self.__grade_to_GPA(self.__get_semester_grade(self.__SEMESTERS[semester_name]))
    def get_course_grade(self, semester_name, course_name): # get course grade
        return self.__get_course_grade(self.__SEMESTERS[semester_name].courses[course_name])
    def get_course_letter_grade(self, semester_name, course_name): # get course letter grade
        return self.__grade_to_letter(self.__get_course_grade(self.__SEMESTERS[semester_name].courses[course_name]))
    def get_course_GPA(self, semester_name, course_name): # get course GPA
        return self.__grade_to_GPA(self.__get_course_grade(self.__SEMESTERS[semester_name].courses[course_name]))
    def get_section_grade(self, semester_name, course_name, section_name): # get section grade
        return self.__get_section_grade_percentage(self.__SEMESTERS[semester_name].courses[course_name].sections[section_name])
    def get_section_letter_grade(self, semester_name, course_name, section_name): # get section letter grade
        return self.__grade_to_letter(self.__get_section_grade_percentage(self.__SEMESTERS[semester_name].courses[course_name].sections[section_name]))
    def get_section_GPA(self, semester_name, course_name, section_name): # get section GPA
        return self.__grade_to_GPA(self.__get_section_grade_percentage(self.__SEMESTERS[semester_name].courses[course_name].sections[section_name]))
    def get_subsection_grade(self, semester_name, course_name, section_name, subsection_name): # get subsection grade
        return self.__SEMESTERS[semester_name].courses[course_name].sections[section_name].subsections[subsection_name].grade
    def get_subsection_letter_grade(self, semester_name, course_name, section_name, subsection_name): # get subsection letter grade
        return self.__grade_to_letter(self.__SEMESTERS[semester_name].courses[course_name].sections[section_name].subsections[subsection_name].grade)
    def get_subsection_GPA(self, semester_name, course_name, section_name, subsection_name): # get subsection GPA
        return self.__grade_to_GPA(self.__SEMESTERS[semester_name].courses[course_name].sections[section_name].subsections[subsection_name].grade)
    def get_subsection_weight(self, semester_name, course_name, section_name, subsection_name):
        return self.__SEMESTERS[semester_name].courses[course_name].sections[section_name].subsections[subsection_name].grade_weight
    def get_section_weight(self, semester_name, course_name, section_name):
        return self.__SEMESTERS[semester_name].courses[course_name].sections[section_name].section_weight
    