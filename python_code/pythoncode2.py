#pythoncode2.py

OVERALL_GPA = 0
OVERALL_LETTER_GRADE = "F"
OVERALL_GRADE = 0
SEMESTERS = {} # keys are semester names, values are semester grades

def grade_to_letter(grade):
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
def grade_to_GPA(grade):
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
    
def get_overall_grade(semesters): # given a dict of semesters, return overall grade
    overall_grade = 0
    for sem in semesters.values():
        overall_grade += get_semester_grade(sem)
    return overall_grade/len(semesters) # OVERALL_GRADE
def get_semester_grade(semester): # given semester, return semester grade
    semester_grade = 0
    for course in semester.courses.values():
        semester_grade += get_course_grade(course)
    return semester_grade/len(semester.courses)
def get_course_grade(course): # given course, return course grade
    course_grade = 0
    for section in course.sections.values():
        course_grade += get_section_grade(section)
    return course_grade
def get_section_grade(sections): # given section, return section grade
    section_grade = 0
    for subsection in sections.subsections.values():
        section_grade += subsection.weighted_grade
    return section_grade

class Grade():
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
class Section():
    def __init__(self, section_name, section_grade, section_weight, subsections, course):
        self.section_name = section_name # assignments/midterm/final...
        self.section_grade = section_grade # subsection grades added together (calculated with weight - max summed to weight)
        self.section_weigth = section_weight # weight % of section
        self.subsections = subsections # dict of grades in section, keys are subsection names, values are Grade objects
        self.section_itself = self.itself_flag # flag to determine if section itself is a grade
        self.subsection_weights = 0
        self.course = course # course section is in
    def s_grade_update(self): # update grade based on subsections list
        total = 0
        for sub in self.subsections.values():
            total += sub.weighted_grade
        self.grade = total
    def add_subsection(self, grade_name, grade_weight, grade):
        self.subsections[grade_name] = Grade(grade_name, grade_weight, grade)
        self.s_grade_update()
        # update course grade
        self.course.update_curr_grade()
        # update semester grade
        self.course.semester.semester_grade_update()
    def remove_subsection(self, grade_name):
        for sub in self.subsections.copy():
            if sub == grade_name:
                del self.subsections[grade_name]
                self.s_grade_update()
                # update course grade
                self.course.update_curr_grade()
                # update semester grade
                self.course.semester.semester_grade_update()
                return True #print("Subsection removed")
        return False #print("Subsection not found")
    def edit_subsection(self, grade_name, new_grade): # edit subsection grade
        for sub in self.subsections.values():
            if sub.grade_name == grade_name:
                sub.g_grade_update(new_grade) # update grade
                self.s_grade_update() # update section grade
                # update course grade
                self.course.update_curr_grade()
                # update semester grade
                self.course.semester.semester_grade_update()
                return True #print("Subsection updated")
        return False #print("Subsection not found")
    def sub_weight_update(self):
        total = 0
        for sub in self.subsections.values():
            total += sub.grade_weight
        self.subsection_weights = total
    def itself_flag(self): # check if section itself is a grade, delete if add subsections
        for sub in self.subsections.values():
            if sub.grade_name == self.section_name:
                return True
        return False
class Course():
    def __init__(self, course_code, curr_grade, semester): 
        self.course_code = course_code # eg. comp424
        self.curr_grade = curr_grade # current grade (percentage)
        self.semester = semester # semester course is in
        self.sections = {} # sections, key = section name, value = Section
        self.weight = self.sum_weights() # sum of section weights should be 100
    def __str__(self): # print course code
        return self.course_code
    def sum_weights(self): # sum of section weights should be 100
        total = 0
        for s in self.sections.values():
            total += s.section_weight
        return total
    def add_section(self, section_name, section_weight, section_grade, subsections): # add section
        self.sections[section_name] = Section(section_name, section_grade, section_weight, subsections, self)
        self.update_curr_grade() # update current grade and letter grade accordingly
        # update semester grade
        self.semester.semester_grade_update()
        #self.sum_weights()
    def remove_section(self, section_name): # remove section
        if section_name in self.sections.copy():
            del self.sections[section_name]
            self.update_curr_grade()
            # update semester grade
            self.semester.semester_grade_update()
            #self.sum_weights()
            return True #print("Section removed")
        return False #print("Section not found")
    def update_curr_grade(self): # update current grade
        total = 0
        for s in self.sections.values():
            total += s.section_grade
        self.curr_grade = total
    def edit_section(self, section_name, subsection_name, new_grade): # edit subsection grade
        if section_name in self.sections:
            self.sections[section_name].edit_subsection(subsection_name, new_grade)
            self.update_curr_grade() # update current grade 
            # update semester grade
            self.semester.semester_grade_update()
class Semester():
    def __init__(self, semester_name, courses, semester_grade):
        self.semester_name = semester_name # fall/winter/summer year - eg. fall2020
        self.courses = courses # dict of courses, key = course code, value = Course
        self.semester_grade = semester_grade # grade of the semester
    def __str__(self): # print semester name
        return self.semester_name
    def semester_grade_update(self): # update grade
        total = 0
        for c in self.courses.values():
            total += c.curr_grade
        self.semester_grade = total/len(self.courses)
    def add_course(self, course_name, course_grade): # add course
        self.courses[course_name] = Course(course_name, course_grade, self)
        self.semester_grade_update()
    def remove_course(self, course):
        if course in self.courses.copy():    
            del self.courses[course]
            self.semester_grade_update # update grade
            return True #print("Course removed")
        return False #print("Course not found")


def main():
    print("Welcome to the Grade Calculator!")
    #file_name = input("What is the name of the file? (eg. grades.txt) : ")
    #TODO read/write from file
    while True:
        # choose action
        print("What would you like to do? (Enter number of action)")
        action = input("1. Add/Modify a Semester\n2. Add/Modify a Course\n3. View\n4. Exit\n")
        if action == "1": # modify semester
            while True:
                print("What would you like to do? (Enter number of action)")
                sem_action = input("1. Add a Semester\n2. Remove a Semester\n3. Modify Semester information\n4. Exit\n")
                print("Reminder: semester grades are calculated according to the average of the courses in the semester. Exit and choose 2 to modify course grades.")
                print("Semester grades are automatically calculated when you add a course. They are set to 0 by default.")
                if sem_action == "1": # add semester
                    semester_name = input("What is the name of the semester? (eg. fall2020) : ")
                    courses = {}
                    semester_grade = 0
                    SEMESTERS[semester_name] = Semester(semester_name, courses, semester_grade)
                    print("Semester added.")
                    #TODO write to file
                    break
                elif sem_action == "2": # remove semester
                    print("Which semester would you like to remove? (Enter semester name)")
                    print("Semesters:")
                    for s in SEMESTERS.keys():
                        print(s)
                    semester = input()
                    if semester in SEMESTERS.copy():
                        del SEMESTERS[semester]
                        print("Semester removed")
                        #TODO write to file
                        break
                    else:
                        print("Semester not found. Please try again.")
                        continue
                elif sem_action == "3": # modify semester information
                    print("Which semester would you like to modify? (Enter semester name)")
                    print("Semesters:")
                    for s in SEMESTERS.keys():
                        print(s)
                    semester = input()
                    if semester in SEMESTERS:
                        while True:
                            print("What would you like to do? (Enter number of action)")
                            sem_action = input("1. Modify Semester name\n2. Exit\n")
                            if sem_action == "1": # modify semester name
                                new_name = input("What is the new name of the semester? (eg. fall2020) : ")
                                SEMESTERS[new_name] = SEMESTERS.pop(semester)
                                print("Semester name updated.")
                                #TODO write to file
                                break
                            elif sem_action == "2": # exit
                                break
                    else:
                        print("Semester not found. Please try again.")
                        continue
                elif sem_action == "4": # exit
                    break
                else:
                    print("Invalid input. Please try again. (Enter number of action only)")
                    continue
        elif action == "2": # modify course
            while True:
                print("What would you like to do? (Enter number of action)")
                course_action = input("1. Add a Course\n2. Remove a Course\n3. Modify Course information\n4. Exit\n")
                print("Reminder: course grades are calculated according to the average of the sections in the course. Choose 3 to modify section grades.\n")
                if course_action == "1": # add course (update semester grade)
                    print("Which semester would you like to add a course to? (Enter semester name)")
                    print("Semesters:")
                    for s in SEMESTERS.keys():
                        print(s)
                    semester = input()
                    if semester in SEMESTERS:
                        course_code = input("What is the course code? (eg. comp424) : ")
                        curr_grade = 0
                        SEMESTERS[semester].add_course(course_code, curr_grade)
                        print("Course added.")
                        #TODO write to file
                        break
                    else:
                        print("Semester not found. Please try again.")
                        continue
                elif course_action == "2": # remove course (update semester grade)
                    print("Which semester would you like to remove a course from? (Enter semester name)")
                    print("Semesters:")
                    for s in SEMESTERS.keys():
                        print(s)
                    semester = input()
                    if semester in SEMESTERS:
                        print("Which course would you like to remove? (Enter course code)")
                        print("Courses:")
                        for c in SEMESTERS[semester].courses.keys():
                            print(c)
                        course = input()
                        if course in SEMESTERS[semester].courses:
                            SEMESTERS[semester].remove_course(course)
                            print("Course removed.")
                            #TODO write to file
                            break
                        else:
                            print("Course not found. Please try again.")
                            continue
                    else:
                        print("Semester not found. Please try again.")
                        continue
                elif course_action == "3": # modify course information (name, section modification, subsection modification)
                    print("Which semester would you like to modify a course in? (Enter semester name)")
                    print("Semesters:")
                    for s in SEMESTERS.keys():
                        print(s)
                    semester = input()
                    if semester in SEMESTERS:
                        print("Which course would you like to modify? (Enter course code)")
                        print("Courses:")
                        for c in SEMESTERS[semester].courses.keys():
                            print(c)
                        course = input()
                        if course in SEMESTERS[semester].courses:
                            while True:
                                print("What would you like to do? (Enter number of action)")
                                course_action = input("1. Modify Course code\n2. Modify a Section\n3. Exit\n")
                                print("Reminder: course grades are calculated according to the average of the sections in the course. Choose 2 to modify section/subsection grades.\n")
                                if course_action == "1": # modify course code
                                    new_code = input("What is the new course code? (eg. comp424) : ")
                                    SEMESTERS[semester].courses[new_code] = SEMESTERS[semester].courses.pop(course)
                                    print("Course code updated.")
                                    #TODO write to file
                                    break
                                elif course_action == "2": # modify section (name, add section, remove section, edit section)
                                    print("What would you like to do? (Enter number of action)")
                                    section_action = input("1. Add a Section\n2. Remove a Section\n3. Modify a Section\n4. Exit\n")
                                    print("Reminder: section grades are calculated according to the average of the subsections in the section. Choose 3 to modify subsection grades.\n")
                                    print("(Note: if there are no subsections, a subsection will be added with the same name as the section and is_itself = True)")
                                    if section_action == "1": # add section
                                        section_name = input("What is the name of the section? (eg. assignments/midterm) : ")
                                        section_weight = int(input("What is the weight of the section? (eg. 50) : "))
                                        section_grade = 0
                                        subsections = {str(section_name): Grade(section_name, section_weight, section_grade)} # add subsection with same name as section, is_itself = True
                                        SEMESTERS[semester].courses[course].add_section(section_name, section_weight, section_grade, subsections)
                                        print("Section added.")
                                        #TODO write to file
                                        break
                                    elif section_action == "2": # remove section
                                        section_name = input("What is the name of the section? (eg. assignments/midterm) : ")
                                        removed = SEMESTERS[semester].courses[course].remove_section(section_name)
                                        if not removed:
                                            print("Section not found. Please try again.")
                                            continue
                                        print("Section removed.")
                                        #TODO write to file
                                        break
                                    elif section_action == "3": # modify section (name, add subsection, remove subsection, edit subsection)
                                        print("What would you like to do? (Enter number of action)")
                                        subsection_action = input("1. Add a Subsection\n2. Remove a Subsection\n3. Modify a Subsection\n4. Exit\n")
                                        print("Reminder: subsection grades are calculated according to the percentage received. Choose 3 to modify subsection grades.\n")
                                        if subsection_action == "1": # add subsection
                                            print("Which section would you like to add a subsection to? (Enter section name)")
                                            print("Sections:")
                                            for s in SEMESTERS[semester].courses[course].sections.keys():
                                                print(s)
                                            section = input()
                                            if section in SEMESTERS[semester].courses[course].sections:
                                                subsection_name = input("What is the name of the subsection? (eg. assignment 1/2/3...) : ")
                                                subsection_weight = int(input("What is the weight of the subsection? (eg. 50) : "))
                                                subsection_grade = int(input("What is the grade of the subsection? (eg. 80) : "))
                                                # check if section itself is a grade - if so, delete the subsection with the same name
                                                if SEMESTERS[semester].courses[course].sections[section].itself_flag():
                                                    del SEMESTERS[semester].courses[course].sections[section].subsections[section]
                                                SEMESTERS[semester].courses[course].sections[section].add_subsection(subsection_name, subsection_weight, subsection_grade)
                                                print("Subsection added.")
                                                #TODO write to file
                                                break
                                            else:
                                                print("Section not found. Please try again.")
                                                continue
                                        elif subsection_action == "2": # remove subsection
                                            print("Which section would you like to remove a subsection from? (Enter section name)")
                                            print("Sections:")
                                            for s in SEMESTERS[semester].courses[course].sections.keys():
                                                print(s)
                                            section = input()
                                            if section in SEMESTERS[semester].courses[course].sections:
                                                subsection_name = input("What is the name of the subsection? (eg. assignment 1/2/3...) : ")
                                                removed = SEMESTERS[semester].courses[course].sections[section].remove_subsection(subsection_name)
                                                if not removed:
                                                    print("Subsection not found. Please try again.")
                                                    continue
                                                print("Subsection removed.")
                                                #TODO write to file
                                                break
                                            else:
                                                print("Section not found. Please try again.")
                                                continue
                                        elif subsection_action == "3": # modify subsection (name, grade)
                                            print("Which section would you like to modify a subsection in? (Enter section name)")
                                            print("Sections:")
                                            for s in SEMESTERS[semester].courses[course].sections.keys():
                                                print(s)
                                            section = input()
                                            if section in SEMESTERS[semester].courses[course].sections:
                                                print("Note: if there are no subsections, give the name of the section when prompted for the subsection name.")
                                                subsection_name = input("What is the name of the subsection? (eg. assignment 1/2/3...) : ")
                                                name_grade = input("Would you like to modify the name or grade of the subsection? (Enter name/grade) : ")
                                                if name_grade == "name":
                                                    new_name = input("What is the new name of the subsection? (eg. assignment 1/2/3...) : ")
                                                    SEMESTERS[semester].courses[course].sections[section].subsections[new_name] = SEMESTERS[semester].courses[course].sections[section].subsections.pop(subsection_name)
                                                    print("Subsection updated.")
                                                    #TODO write to file
                                                    break
                                                elif name_grade == "grade":
                                                    new_grade = int(input("What is the new grade of the subsection? (eg. 80) : "))
                                                    updated = SEMESTERS[semester].courses[course].sections[section].edit_subsection(subsection_name, new_grade)
                                                    if not updated:
                                                        print("Subsection not found. Please try again.")
                                                        continue
                                                    print("Subsection updated.")
                                                    #TODO write to file
                                                    break
                                        elif subsection_action == "4": # exit
                                            break
                                        else:
                                            print("Invalid input. Please try again. (Enter number of action only)")
                                            continue
                                    elif section_action == "4": # exit
                                        break
                                    else:
                                        print("Invalid input. Please try again. (Enter number of action only)")
                                        continue
                                elif course_action == "3": # exit
                                    break
                                else:
                                    print("Invalid input. Please try again. (Enter number of action only)")
                                    continue
                elif course_action == "4": # exit
                    break
                else:
                    print("Invalid input. Please try again. (Enter number of action only)")
                    continue
        elif action == "3": # view
            while True:
                print("What would you like to do? (Enter number of action)")
                view_action = input("1. View overall grade\n2. View a Semester summary\n3. View a Course summary\n4. Exit\n")
                if view_action == "1": # view overall grade
                    if len(SEMESTERS) == 0:
                        print("No semesters found. Please add a semester and course first.")
                        continue
                    OVERALL_GRADE = get_overall_grade(SEMESTERS)
                    OVERALL_LETTER_GRADE = grade_to_letter(OVERALL_GRADE)
                    OVERALL_GPA = grade_to_GPA(OVERALL_GRADE)
                    print("Overall grade: " + str(OVERALL_GRADE) + "%")
                    print("Overall letter grade: " + OVERALL_LETTER_GRADE)
                    print("Overall GPA: " + str(OVERALL_GPA))
                    print("\n")

                    #TODO print whole summary as table

                    print("\n")
                    break
                elif view_action == "2": # view semester summary (name, courses + grades, grade, GPA, letter grade)
                    print("Which semester would you like to view? (Enter semester name)")
                    print("Semesters:")
                    for s in SEMESTERS.keys():
                        print(s)
                    semester = input()
                    if semester in SEMESTERS:
                        print("\n")
                        print("Semester: " + semester)
                        print("Courses:        Grades:")
                        for c in SEMESTERS[semester].courses.keys():
                            course_grade = get_course_grade(SEMESTERS[semester].courses[c])
                            print(c + "            " + str(course_grade) + "%\n")
                        semester_grade = get_semester_grade(SEMESTERS[semester])
                        print("Semester grade: " + str(semester_grade) + "%")
                        print("Semester letter grade: " + grade_to_letter(semester_grade))
                        print("Semester GPA: " + str(grade_to_GPA(semester_grade)))
                        print("\n")
                        break
                    else:
                        print("Semester not found. Please try again.")
                        continue
                elif view_action == "3": # view course summary (name, sections + grades, subsections + grades if applicable, grade, GPA, letter grade)
                    print("Which semester would you like to view a course from? (Enter semester name)")
                    print("Semesters:")
                    for s in SEMESTERS.keys():
                        print(s)
                    semester = input()
                    if semester in SEMESTERS:
                        print("Which course would you like to view? (Enter course code)")
                        print("Courses:")
                        for c in SEMESTERS[semester].courses.keys():
                            print(c)
                        course = input()
                        if course in SEMESTERS[semester].courses:
                            print("\n")
                            print("Semester: " + semester)
                            print("Course: " + course)
                            print("Sections:          Grades:")
                            for s in SEMESTERS[semester].courses[course].sections.keys():
                                section_grade = get_section_grade(SEMESTERS[semester].courses[course].sections[s])
                                print(s + "                " + str(section_grade) + "%")
                                if not SEMESTERS[semester].courses[course].sections[s].itself_flag():
                                    print("   Subsections:")
                                    for sub in SEMESTERS[semester].courses[course].sections[s].subsections.values():
                                        print("   " + sub.grade_name + "             " + str(sub.grade) + "%")
                            print("\n")
                            course_grade = get_course_grade(SEMESTERS[semester].courses[course])
                            print("Course grade: " + str(course_grade) + "%")
                            print("Course letter grade: " + grade_to_letter(course_grade))
                            print("Course GPA: " + str(grade_to_GPA(course_grade)))
                            print("\n")
                            break
                        else:
                            print("Course not found. Please try again.")
                            continue
                    else:
                        print("Semester not found. Please try again.")
                        continue
                elif view_action == "4": # exit
                    break
                else:
                    print("Invalid input. Please try again. (Enter number of action only)")
                    continue
        elif action == "4": # exit
            break
        else:
            print("Invalid input. Please try again. (Enter number of action only)")
            continue

main()


"""
#calculator_class.py

class Calculator():
    __OVERALL_GPA = 0
    __OVERALL_LETTER_GRADE = "F"
    __OVERALL_GRADE = 0
    __SEMESTERS = {} # keys are semester names, values are semester grades

    def __init__(self):
            self.__SEMESTERS = self.__SEMESTERS
            self.__OVERALL_GRADE = self.__get_overall_grade(self.__SEMESTERS)
            self.__OVERALL_LETTER_GRADE = self.__grade_to_letter(self.__OVERALL_GRADE)
            self.__OVERALL_GPA = self.__grade_to_GPA(self.__OVERALL_GRADE)

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
        
    def __get_overall_grade(self, semesters): # given a dict of semesters, return overall grade
        overall_grade = 0
        if len(semesters) == 0:
            return 0
        for sem in semesters.values():
            overall_grade += self.__get_semester_grade(sem)
        return overall_grade/len(semesters) # OVERALL_GRADE
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
        #def get_subsection_name(self, Subsection): # get subsection name given Subsection object
        #    return Subsection.grade_name
    class __Section():
        def __init__(self, section_name, section_grade, section_weight, subsections, course):
            self.section_name = section_name # assignments/midterm/final...
            #self.section_grade = section_grade # subsection grades added together (calculated with weight - max summed to weight)
            self.section_weight = section_weight # weight % of section
            self.subsections = subsections # dict of grades in section, keys are subsection names, values are Grade objects
            #self.section_itself = self.itself_flag # flag to determine if section itself is a grade
            #self.subsection_weights = 0
            #self.course = course # course section is in
        #def __str__(self): # print section name
        #    return self.section_name
        #def s_grade_update(self): # update grade based on subsections list
        #    total = 0
        #    for sub in self.subsections.values():
        #        total += sub.weighted_grade
        #    self.grade = total
        def add_subsection(self, grade_name, grade_weight, grade):
            self.subsections[grade_name] = Calculator._Calculator__Grade(grade_name, grade_weight, grade)
            #self.s_grade_update()
            # update course grade
            #self.course.update_curr_grade()
            # update semester grade
            #self.course.semester.semester_grade_update()
        def remove_subsection(self, grade_name):
            for sub in self.subsections.copy():
                if sub == grade_name:
                    del self.subsections[grade_name]
                    #self.s_grade_update()
                    # update course grade
                    #self.course.update_curr_grade()
                    # update semester grade
                    #self.course.semester.semester_grade_update()
                    return True #print("Subsection removed")
            return False #print("Subsection not found")
        def edit_subsection(self, grade_name, new_grade): # edit subsection grade
            for sub in self.subsections.values():
                if sub.grade_name == grade_name:
                    sub.g_grade_update(new_grade) # update grade
                    #self.s_grade_update() # update section grade
                    # update course grade
                    #self.course.update_curr_grade()
                    # update semester grade
                    #self.course.semester.semester_grade_update()
                    return True #print("Subsection updated")
            return False #print("Subsection not found")
        #def sub_weight_update(self):
            total = 0
            for sub in self.subsections.values():
                total += sub.grade_weight
            self.subsection_weights = total
        #def itself_flag(self): # check if section itself is a grade, delete if add subsections
            for sub in self.subsections.values():
                if sub.grade_name == self.section_name:
                    return True
            return False
        #def get_section_name(self, Section): # get section name given Section object
            return Section.section_name
    class __Course():
        def __init__(self, course_code, curr_grade, semester): 
            self.course_code = course_code # eg. comp424
            #self.curr_grade = curr_grade # current grade (percentage)
            #self.semester = semester # semester course is in
            self.sections = {} # sections, key = section name, value = Section
            #self.weight = self.sum_weights() # sum of section weights should be 100
        def __str__(self): # print course code
            return self.course_code
        #def sum_weights(self): # sum of section weights should be 100
            total = 0
            for s in self.sections.values():
                total += s.section_weight
            return total
        def add_section(self, section_name, section_weight, section_grade, subsections): # add section
            self.sections[section_name] = Calculator._Calculator__Section(section_name, section_grade, section_weight, subsections, self)
            #self.update_curr_grade() # update current grade and letter grade accordingly
            # update semester grade
            #self.semester.semester_grade_update()
            #self.sum_weights()
        def remove_section(self, section_name): # remove section
            if section_name in self.sections.copy():
                del self.sections[section_name]
                #self.update_curr_grade()
                # update semester grade
                #self.semester.semester_grade_update()
                #self.sum_weights()
                return True #print("Section removed")
            return False #print("Section not found")
        #def update_curr_grade(self): # update current grade
            total = 0
            for s in self.sections.values():
                total += s.section_grade
            self.curr_grade = total
        def edit_section(self, section_name, subsection_name, new_grade): # edit subsection grade
            if section_name in self.sections:
                self.sections[section_name].edit_subsection(subsection_name, new_grade)
                #self.update_curr_grade() # update current grade 
                # update semester grade
                #self.semester.semester_grade_update()
        #def get_course_name(self, Course): # get course name given Course object
        #    return Course.course_code
    class __Semester():
        def __init__(self, semester_name, courses, semester_grade):
            self.semester_name = semester_name # fall/winter/summer year - eg. fall2020
            self.courses = courses # dict of courses, key = course code, value = Course
            #self.semester_grade = semester_grade # grade of the semester
        def __str__(self): # print semester name
            return self.semester_name
        #def semester_grade_update(self): # update grade
            total = 0
            for c in self.courses.values():
                total += c.curr_grade
            self.semester_grade = total/len(self.courses)
        def add_course(self, course_name, course_grade): # add course
            self.courses[course_name] = Calculator._Calculator__Course(course_name, course_grade, self)
        #    self.semester_grade_update()
        def remove_course(self, course):
            if course in self.courses.copy():    
                del self.courses[course]
        #        self.semester_grade_update # update grade
                return True #print("Course removed")
            return False #print("Course not found")
        #def get_semester_name(self, Semester): # get semester name given Semester object
            return Semester.semester_name


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
    #def get_semester(self, semester_name): # get semester ??? object
        if semester_name in self.__SEMESTERS.copy():
            return self.__SEMESTERS[semester_name]
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
    #def get_course(self, semester_name, course_name): # get course object ???
        if course_name in self.__SEMESTERS[semester_name].courses.copy():
            return self.__SEMESTERS[semester_name].courses[course_name]
        return False, "Course not found. Please try again."
    #section functions
    def add_section(self, semester_name, course_name, section_name, section_weight): # add section
        section_grade = 0
        #subsections = {str(section_name): self.__Grade(section_name, section_weight, section_grade)}
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
    #def get_section(self, semester_name, course_name, section_name): # get section object ???
        if section_name in self.__SEMESTERS[semester_name].courses[course_name].sections.copy():
            return self.__SEMESTERS[semester_name].courses[course_name].sections[section_name]
        return False, "Section not found. Please try again."
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
    #def get_subsection(self, semester_name, course_name, section_name, subsection_name): # get subsection object ???
        if subsection_name in self.__SEMESTERS[semester_name].courses[course_name].sections[section_name].subsections.copy():
            return self.__SEMESTERS[semester_name].courses[course_name].sections[section_name].subsections[subsection_name]
        return False, "Subsection not found. Please try again."
    #grade get functions
    def get_overall_grade(self): # get overall grade
        return self.__get_overall_grade(self.__SEMESTERS)
    def get_overall_letter_grade(self, grade): # get overall letter grade
        return self.__grade_to_letter(grade)
    def get_overall_GPA(self, grade): # get overall GPA
        return self.__grade_to_GPA(grade)
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
    """