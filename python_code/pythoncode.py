# grade calculator

#TODO: grades
GPA = 0

#letter grades
def letter_grade(grade):
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
# GPA
def gpa(letter_grade):
    if letter_grade == "A":
        return 4.0
    elif letter_grade == "A-":
        return 3.7
    elif letter_grade == "B+":
        return 3.3
    elif letter_grade == "B":
        return 3.0
    elif letter_grade == "B-":
        return 2.7
    elif letter_grade == "C+":
        return 2.3
    elif letter_grade == "C":
        return 2.0
    elif letter_grade == "D":
        return 1.0
    else:
        return 0.0
def letter(gpa):
    if gpa >= 4.0:
        return "A"
    elif gpa >= 3.7:
        return "A-"
    elif gpa >= 3.3:
        return "B+"
    elif gpa >= 3.0:
        return "B"
    elif gpa >= 2.7:
        return "B-"
    elif gpa >= 2.3:
        return "C+"
    elif gpa >= 2.0:
        return "C"
    elif gpa >= 1.0:
        return "D"
    else:
        return "F"

# GPA and letter grade by course
def gpa_by_course(course): # Course
    return course.course_letter_grade, gpa(course.course_letter_grade)
# GPA and letter grade by semester
def gpa_by_semester(smstr): # semester
    smstr.gpa_update()
    return letter(smstr.gpa), smstr.gpa
# overall GPA 
def overall_gpa(semesters): # list of Semesters
    total_gpa = 0
    for gpas in semesters:
        total_gpa += gpas.gpa
    GPA = total_gpa/len(semesters)
    return GPA

# Semester: which semester "", dict of courses, GPA of the semester
class Semester():
    def __init__(self, semester_name, courses, gpa):
        self.semester_name = semester_name # fall/winter/summer year - eg. fall2020
        self.courses = courses # dict of courses, key = course code, value = Course
        self.gpa = gpa # GPA of the semester
    def __str__(self): # print semester name
        return self.semester_name
    def gpa_update(self): # update gpa
        total = 0
        for c in self.courses.values():
            total += gpa(c.course_letter_grade)
        self.gpa = total/len(self.courses)
    def add_course(self, course_name, grade): # add course
        self.courses[course_name] = Course(course_name, grade, self)
        self.gpa_update
    def remove_course(self, course):
        if course in self.courses.copy():    
            del self.courses[course]
            self.gpa_update # update gpa
            return True #print("Course removed")
        return False #print("Course not found")

# Course: course code, current grade, course letter grade, sections
class Course():
    def __init__(self, course_code, curr_grade, semester, weight = 0): 
        self.course_code = course_code # eg. comp424
        self.curr_grade = curr_grade # current grade (percentage)
        self.semester = semester # semester course is in
        self.course_letter_grade = "F" # letter grade
        self.sections = {} # sections, key = section name, value = Section
        self.weight = weight
    def __str__(self): # print course code
        return self.course_code
    def weight_update(self): # update weight
        total = 0
        for s in self.sections.values():
            total += s.weight
        self.weight = total
    def letter_grade(self): # update letter grade
        self.course_letter_grade = letter_grade(self.curr_grade)
    def add_section(self, section_name, weight, grade, subsections, section_itself): # add section
        self.sections[section_name] = Section(section_name, grade, weight, subsections, section_itself)
        self.update_curr_grade() # update current grade and letter grade accordingly
        self.weight_update()
    def remove_section(self, section_name): # remove section
        if section_name in self.sections.copy():
            del self.sections[section_name]
            self.update_curr_grade()
            self.weight_update()
            return True #print("Section removed")
        return False #print("Section not found")
    def update_curr_grade(self): # update current grade
        total = 0
        for s in self.sections.values():
            total += s.grade
        self.curr_grade = total
        self.letter_grade()
    def edit_section(self, section_name, subsection_name, new_grade): # edit subsection grade
        if section_name in self.sections:
            self.sections[section_name].edit_subsection(subsection_name, new_grade)
            self.update_curr_grade() # update current grade and letter grade accordingly
            self.weight_update()

# Section: section name, grade, subsections
class Section():
    def __init__(self, section_name, grade, weight, subsections, section_itself):
        self.section_name = section_name # assignments/midterm/final...
        self.grade = grade # subsection grades added together (calculated with weight - max summed to weight)
        self.weight = weight # weight % of section
        self.subsections = subsections # list of grades in section
        self.section_itself = section_itself # flag to determine if section itself is a grade
        self.subsection_weights = 0
    def s_grade_update(self): # update grade based on subsections list
        total = 0
        for i in range(len(self.subsections)):
            total += self.subsections[i].weighted_grade
        self.grade = total
    def add_subsection(self, subsection, weight, grade):
        self.subsections.append(Grade(subsection, weight, grade))
        self.s_grade_update()
    def remove_subsection(self, subsection):
        for i in self.subsections:
            if i.name == subsection:
                self.subsections.remove(i)
                self.s_grade_update()
                return True #print("Subsection removed")
        return False #print("Subsection not found")
    def edit_subsection(self, subsection, new_grade):
        for i in self.subsections:
            if i.name == subsection:
                i.g_grade_update(new_grade)
                self.s_grade_update()
                return True #print("Subsection updated")
        return False #print("Subsection not found")
    def sub_weight_update(self):
        total = 0
        for i in self.subsections:
            total += i.weight
        self.subsection_weights = total

# Grade: name, weight, grade
class Grade():
    def __init__(self, name, weight, grade):
        self.name = name # assignment 1/2/3...
        self.weight = weight # weight % of subsection
        self.grade = grade # % percentage received
        self.weighted_grade = self.calculate(weight, grade) # grade * weight / 100
    def g_grade_update(self, new_grade):
        self.grade = new_grade
    # calculate grade given percentage and weight
    def calculate(self, weight, grade): # use this to calculate grade for sections and subsections
        return (grade * weight) / 100 

# useful functions

    

"""
while True:
    file_name = input("What is the name of the file? (eg. grades.txt) : ")
    option = input("Would you like to append or overwrite or create a new file? (append/overwrite/new) : ")
    if option == "append":
        f = open(file_name, "a") 
        break
    elif option == "overwrite":
        f = open(file_name, "w")
        break
    elif option == "new":
        try:
            f = open(file_name, "x")      
        except FileExistsError:
            print("File already exists, try again")
            continue
        f = open(file_name, "x")
        break
"""
semesters = [] # list of semesters
while True:
    # choose action
    action = input("What would you like to do? \n'a' : add a semester\n'b' : edit a semester\n'c' : edit a course grades\n'd' : view\n'q' : quit\n ")
    if action == "a": # add a semester
        semester = input("What semester is it? (fall/winter/summer year - eg. fall2020) or type 'back' to go back: ")
        if semester == "back":
            continue
        num_courses = input("How many courses are you taking? : ")
        try :
            num_courses = int(num_courses)
        except ValueError:
            print("Please enter a number")
            continue
        num_courses = int(num_courses)
        new_semester = Semester(semester, {}, 0)
        for i in range(num_courses):
            course_code = input("What is the course code " + str(i+1) + "? (eg. comp424) : ")
            new_semester.add_course(course_code, 0)
            while True:
                section_name = input("What is the section name? (eg. assignments/midterm/final) or type 'done' to finish : ")
                if section_name == "done":
                    if new_semester.courses[course_code].weight != 100: # course total weight must be 100
                        print("Course weight must be 100, try again by adding/removing/editing a section")
                        continue
                    else:
                        print("Course added")
                        break
                section_weight = input("What is the weight of the section? (eg. 20) : ") # sections must add up to 100 weight
                try :
                    section_weight = int(section_weight)
                except ValueError:
                    print("Please enter a number")
                    continue
                section_weight = int(section_weight)
                grade = input("What is the grade of the section? (eg. 80) or '0' if don't know yet : ")
                try :
                    grade = int(grade)
                except ValueError:
                    print("Please enter a number")
                    continue
                grade = int(grade)
                if new_semester.courses[course_code].weight + section_weight > 100: # course total weight must be less than 100
                    print("Weight exceeds 100, try again")
                    continue
                new_semester.courses[course_code].add_section(section_name, section_weight, grade, [Grade(section_name, section_weight, grade)], True)
                sub = input("Are you adding a subsection? (yes/no) : ")
                if sub == "yes":
                    while True:
                        subsection_name = input("What is the subsection name? (eg. assignment 1/2/3) or type 'done' to finish : ")
                        if subsection_name == "done":
                            if new_semester.courses[course_code].sections[section_name].weight != section_weight: # subsections weight must add up to section weight
                                print("Weight is not" + weight + ", try again by adding/removing/editing a subsection")
                                continue
                            else:
                                print("Subsection added")
                                break
                        if subsection_name in new_semester.courses[course_code].sections[section_name].subsections:
                            print("Subsection already exists, try again or remove the subsection")
                            continue
                        sub_weight = input("What is the weight of the subsection? (eg. 20) : ")
                        try :
                            sub_weight = int(sub_weight)
                        except ValueError:
                            print("Please enter a number")
                            continue
                        sub_weight = int(sub_weight)
                        grade = input("What is the grade of the subsection? (eg. 80) : ")
                        try :
                            grade = int(grade)
                        except ValueError:
                            print("Please enter a number")
                            continue
                        grade = int(grade)
                        if new_semester.courses[course_code].sections[section_name].subsection_weights + sub_weight > section_weight: # subsections weight must add up to section weight
                            print("Weight exceeds " + str(section_weight) + ", try again")
                            continue
                        if new_semester.courses[course_code].sections[section_name].section_itself:
                            new_semester.courses[course_code].sections[section_name].subsections.remove(new_semester.courses[course_code].sections[section_name].subsections[0])
                            new_semester.courses[course_code].sections[section_name].section_itself = False
                        new_semester.courses[course_code].sections[section_name].add_subsection(subsection_name, sub_weight, grade)
                elif sub == "no":
                    continue
        semesters.append(new_semester)
    elif action == "b": # edit a semester
        semester = input("What semester is it? (fall/winter/summer year - eg. fall2020) or type 'back' to go back : ")
        if semester == "back":
            continue
        edit = input("Are you adding or removing a course? (add/remove) or type 'back' to go back : " )
        if edit == "back":
            continue
        elif edit == "add":
            for i in range(len(semesters)):
                if semesters[i].semester_name == semester:
                    edit_semester = semesters[i]
                    course_code = input("What is the course code? (eg. comp424) : ")
                    edit_semester.add_course(course_code, 0)
                    while True: # add sections until weight is 100
                        section_name = input("What is the section name? (eg. assignments/midterm/final) or type 'done' to finish : ")
                        if section_name == "done":
                            if edit_semester.courses[course_code].weight != 100:
                                print("Weight is not 100, try again by adding/removing/editing a section")
                                continue
                            else:
                                print("Course added")
                                break
                        section_weight = input("What is the weight of the section? (eg. 20) : ")
                        try :
                            section_weight = int(section_weight)
                        except ValueError:
                            print("Please enter a number")
                            continue
                        section_weight = int(section_weight)
                        grade = input("What is the grade of the section? (eg. 80) : ")
                        try :
                            grade = int(grade)
                        except ValueError:
                            print("Please enter a number")
                            continue
                        grade = int(grade)
                        if edit_semester.courses[course_code].weight + section_weight > 100:
                            print("Weight exceeds 100, try again")
                            continue
                        edit_semester.courses[course_code].add_section(section_name, section_weight, grade, [Grade(section_name, section_weight, grade)], True)
                        sub = input("Are you adding a subsection? (yes/no) : ")
                        if sub == "yes":
                            while True:
                                subsection_name = input("What is the subsection name? (eg. assignment 1/2/3) or type 'done' to finish : ")
                                if subsection_name == "done":
                                    if edit_semester.courses[course_code].sections[section_name].weight != section_weight:
                                        print("Weight is not" + str(section_weight) + ", try again by adding/removing/editing a subsection")
                                        continue
                                    else:
                                        print("Subsection added")
                                        break
                                if subsection_name in edit_semester.courses[course_code].sections[section_name].subsections:
                                    print("Subsection already exists, try again or remove the subsection")
                                    continue
                                weight = input("What is the weight of the subsection? (eg. 20) : ")
                                try :
                                    weight = int(weight)
                                except ValueError:
                                    print("Please enter a number")
                                    continue
                                weight = int(weight)
                                grade = input("What is the grade of the subsection? (eg. 80) : ")
                                try :
                                    grade = int(grade)
                                except ValueError:
                                    print("Please enter a number")
                                    continue
                                grade = int(grade)
                                if edit_semester.courses[course_code].sections[section_name].weight + weight > section_weight:
                                    print("Weight exceeds 100, try again")
                                    continue
                                if edit_semester.courses[course_code].sections[section_name].section_itself:
                                    edit_semester.courses[course_code].sections[section_name].subsections.remove(edit_semester.courses[course_code].sections[section_name].subsections[0])
                                    edit_semester.courses[course_code].sections[section_name].section_itself = False
                                edit_semester.courses[course_code].sections[section_name].add_subsection(subsection_name, weight, grade)
                        elif sub == "no":
                            continue
                    break
        elif edit == "remove":
            for i in range(len(semesters)):
                if semesters[i].semester_name == semester:
                    edit_semester = semesters[i]
                    course_code = input("What is the course code? (eg. comp424) : ")
                    removed = edit_semester.remove_course(course_code)
                    if not removed:
                        print("Course not found, try again or add a course")
                    else:
                        print("Course removed")
                    break
    #TODO: grade needed to pass/get a certain grade
    elif action == "c": # edit a course grades
        semester = input("What semester is it? (fall/winter/summer year - eg. fall2020) or type 'back' to go back : ")
        if semester == "back":
            continue
        found = False
        for i in range(len(semesters)):
            if semesters[i].semester_name == semester:
                edit_semester = semesters[i]
                found = True
                break
        if not found:
            print("Semester not found, try again or add a semester")
            continue
        course_code = input("What is the course code? (eg. comp424) : ")
        if course_code not in edit_semester.courses: #find course
            print("Course not found, try again or add a course")
            break
        else:
            # options: add section, remove section, edit section
            edit_course = edit_semester.courses[course_code]
            edit = input("Are you adding, removing, or editing a section? (add/remove/edit) or type 'back' to go back : " )
            if edit == "back":
                continue
            elif edit == "add":
                section_name = input("What is the section name? (eg. assignments/midterm/final) : ")
                section_weight = input("What is the weight of the section? (eg. 20) : ")
                try :
                    section_weight = int(section_weight)
                except ValueError:
                    print("Please enter a number")
                    continue
                section_weight = int(section_weight)
                if edit_course.weight + weight > 100:
                    print("Weight exceeds 100, try again or remove a section first")
                    continue
                grade = input("What is the grade of the section? (eg. 80) : ")
                try :
                    grade = int(grade)
                except ValueError:
                    print("Please enter a number")
                    continue
                grade = int(grade)
                edit_course.add_section(section_name, section_weight, grade, [Grade(section_name, section_weight, grade)], True)
                sub = input("Are you adding a subsection? (yes/no) : ")
                if sub == "yes":
                    while True:
                        subsection_name = input("What is the subsection name? (eg. assignment 1/2/3) or type 'done' to finish : ")
                        if subsection_name == "done":
                            if edit_course.sections[section_name].weight != section_weight:
                                print("Weight is not" + str(section_weight) + ", try again by adding/removing/editing a subsection")
                                continue
                            else:
                                print("Subsection added")
                                break
                        if subsection_name in edit_course.sections[section_name].subsections:
                            print("Subsection already exists, try again or remove the subsection")
                            continue
                        weight = input("What is the weight of the subsection? (eg. 20) : ")
                        try :
                            weight = int(weight)
                        except ValueError:
                            print("Please enter a number")
                            continue
                        weight = int(weight)
                        grade = input("What is the grade of the subsection? (eg. 80) : ")
                        try :
                            grade = int(grade)
                        except ValueError:
                            print("Please enter a number")
                            continue
                        grade = int(grade)
                        if edit_course.sections[section_name].weight + weight > section_weight:
                            print("Weight exceeds 100, try again")
                            continue
                        if edit_course.sections[section_name].section_itself:
                            edit_course.sections[section_name].subsections.remove(edit_course.sections[section_name].subsections[0])
                            edit_course.sections[section_name].section_itself = False
                        edit_course.sections[section_name].add_subsection(subsection_name, weight, grade)
                elif sub == "no":
                    continue
            elif edit == "remove":  

#TODO: fix weigth update

                section_name = input("What is the section name to be removed? (eg. assignments/midterm/final) : ")
                removed = edit_course.remove_section(section_name)
                if not removed:
                    print("Section not found, try again or add a section")
                    break
                else:
                    print("Section removed")
                    if edit_course.weight != 100:
                        print("Weight is not 100, please add a section")
                        while True: # add sections until weight is 100
                            section_name = input("What is the section name to be added? (eg. assignments/midterm/final) or 'back' to remove : ")
                            if section_name == "back":
                                break
                            weight = input("What is the weight of the section? (eg. 20) : ")
                            try :
                                weight = int(weight)
                            except ValueError:
                                print("Please enter a number")
                                continue
                            weight = int(weight)
                            if edit_course.weight + weight > 100:
                                print("Weight exceeds 100, try again or remove a section first")
                                continue
                            grade = input("What is the grade of the section? (eg. 80) : ")
                            try :
                                grade = int(grade)
                            except ValueError:
                                print("Please enter a number")
                                continue
                            grade = int(grade)
                            edit_course.add_section(section_name, weight, grade, [Grade(section_name, weight, grade)], True)
                            sub = input("Are you adding a subsection? (yes/no) : ")
                            if sub == "yes":
                                while True:
                                    subsection_name = input("What is the subsection name? (eg. assignment 1/2/3) or type 'done' to finish : ")
                                    if subsection_name == "done":
                                        if edit_course.sections[section_name].weight != 100:
                                            print("Weight is not 100, try again by adding/removing/editing a subsection")
                                            continue
                                        else:
                                            print("Subsection added")
                                            break
                                    if subsection_name in edit_course.sections[section_name].subsections:
                                        print("Subsection already exists, try again or remove the subsection")
                                        continue
                                    weight = input("What is the weight of the subsection? (eg. 20) : ")
                                    try :
                                        weight = int(weight)
                                    except ValueError:
                                        print("Please enter a number")
                                        continue
                                    weight = int(weight)
                                    grade = input("What is the grade of the subsection? (eg. 80) : ")
                                    try :
                                        grade = int(grade)
                                    except ValueError:
                                        print("Please enter a number")
                                        continue
                                    grade = int(grade)
                                    if edit_course.sections[section_name].weight + weight > 100:
                                        print("Weight exceeds 100, try again")
                                        continue
                                    if edit_course.sections[section_name].section_itself:
                                        edit_course.sections[section_name].subsections.remove(edit_course.sections[section_name].subsections[0])
                                        edit_course.sections[section_name].section_itself = False
                                    edit_course.sections[section_name].add_subsection(subsection_name, weight, grade)
                            elif sub == "no":
                                continue
                        break
            elif edit == "edit":
                sub_edit = input("Are you adding, removing, or editing a sub section? (add/remove/edit) or type 'back' to go back : " )
                if sub_edit == "back":
                    continue
                elif sub_edit == "add":
                    section_name = input("What is the section name? (eg. assignments/midterm/final) : ")
                    if section_name not in edit_course.sections:
                        print("Section not found, try again or add a section")
                        continue
                    subsection_name = input("What is the subsection name? (eg. assignment 1/2/3) : ")
                    if subsection_name in edit_course.sections[section_name].subsections:
                        print("Subsection already exists, try again or remove the subsection")
                        continue
                    weight = input("What is the weight of the subsection? (eg. 20) : ")
                    try :
                        weight = int(weight)
                    except ValueError:
                        print("Please enter a number")
                        continue
                    weight = int(weight)
                    if edit_course.sections[section_name].weight + weight > 100:
                        print("Weight exceeds 100, try again or remove a subsection")
                        continue
                    grade = input("What is the grade of the subsection? (eg. 80) : ")
                    try :
                        grade = int(grade)
                    except ValueError:
                        print("Please enter a number")
                        continue
                    grade = int(grade)
                    if edit_course.sections[section_name].section_itself:
                        edit_course.sections[section_name].subsections.remove(edit_course.sections[section_name].subsections[0])
                        edit_course.sections[section_name].section_itself = False
                    edit_course.sections[section_name].add_subsection(subsection_name, weight, grade)
                elif sub_edit == "remove":
                    section_name = input("What is the section name? (eg. assignments/midterm/final) : ")
                    if section_name not in edit_course.sections:
                        print("Section not found, try again or add a section")
                        continue
                    subsection_name = input("What is the subsection name? (eg. assignment 1/2/3) : ")
                    removed = edit_course.sections[section_name].remove_subsection(subsection_name)
                    if not removed:
                        print("Subsection not found, try again or add a subsection")
                    else:
                        print("Subsection removed")
                        if edit_course.sections[section_name].weight != 100:
                            print("Weight is not 100, please add a subsection")
                            while True:
                                subsection_name = input("What is the subsection name to be added? (eg. assignment 1/2/3) or 'back' to remove : ")
                                if subsection_name == "back":
                                    break
                                if subsection_name in edit_course.sections[section_name].subsections:
                                    print("Subsection already exists, try again or remove the subsection")
                                    continue
                                weight = input("What is the weight of the subsection? (eg. 20) : ")
                                try :
                                    weight = int(weight)
                                except ValueError:
                                    print("Please enter a number")
                                    continue
                                weight = int(weight)
                                if edit_course.sections[section_name].weight + weight > 100:
                                    print("Weight exceeds 100, try again or remove a subsection first")
                                    continue
                                grade = input("What is the grade of the subsection? (eg. 80) : ")
                                try :
                                    grade = int(grade)
                                except ValueError:
                                    print("Please enter a number")
                                    continue
                                grade = int(grade)
                                edit_course.sections[section_name].add_subsection(subsection_name, weight, grade)
                            break
                elif sub_edit == "edit":
                    section_name = input("What is the section name? (eg. assignments/midterm/final) : ")
                    if section_name not in edit_course.sections:
                        print("Section not found, try again or add a section")
                        continue
                    subsection_name = input("What is the subsection name? (eg. assignment 1/2/3) : ")
                    if subsection_name not in edit_course.sections[section_name].subsections:
                        print("Subsection not found, try again or add a subsection")
                        continue
                    new_grade = input("What is the new grade? (eg. 80) : ")
                    try :
                        new_grade = int(new_grade)
                    except ValueError:
                        print("Please enter a number")
                        continue
                    new_grade = int(new_grade)
                    edit_course.edit_section(section_name, subsection_name, new_grade)
    elif action == "d": # view
        view = input("What would you like to view? \n'a' : overall GPA\n'b' : semester summary\n'c' : course summary\n'back' to go back\n")
        if view == "back":
            continue
        elif view == "a": # overall GPA
            GPA = overall_gpa(semesters)
            print("Your overall GPA is " + str(GPA))
        elif view == "b": # semester summary
            semester = input("What semester is it? (fall/winter/summer year - eg. fall2020) or type 'back' to go back : ")
            if semester == "back":
                continue
            for i in range(len(semesters)):
                found = False
                if semesters[i].semester_name == semester:
                    print("Your letter grade and GPA for " + semester + " is " + str(gpa_by_semester(semesters[i])) + "\n")
                    print("Your courses for " + semester + " are: " + "\n")
                    for course in semesters[i].courses:
                        print(str(course) + " with letter grade and GPA: " + str(gpa_by_course(semesters[i].courses[course])))
                    found = True
                    break
            if not found:
                print("Semester not found, try again or add a semester")
        elif view == "c": # course summary
            semester = input("What semester is it? (fall/winter/summer year - eg. fall2020) or type 'back' to go back : ")
            if semester == "back":
                continue
            course_code = input("What is the course code? (eg. comp424) : ")
            for i in range(len(semesters)):
                found = False
                if semesters[i].semester_name == semester:
                    if course_code not in semesters[i].courses:
                        print("Course not found, try again or add a course")
                        break
                    else:
                        print("Your letter grade and GPA for " + course_code + " is " + str(gpa_by_course(semesters[i].courses[course_code])) + "\n")
                        print("Your sections for " + course_code + " are: " + str(", ".join(semesters[i].courses[course_code].sections.keys())) + "\n")
                        print("Section and subsection grades for " + course_code + " are: ")
                        for section in semesters[i].courses[course_code].sections:
                            print(str(section) + " with grade: " + str(semesters[i].courses[course_code].sections[section].grade))
                            for subsection in semesters[i].courses[course_code].sections[section].subsections:
                                if not section.section_itself:   
                                    print(str(subsection.name) + " with grade: " + str(subsection.grade))
                        found = True
                        break
            if not found:
                print("Course not found, try again or add a course")
    elif action == "q": # quit
        #f.close()
        break