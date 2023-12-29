#cli.py
import calculator_class
import tables
import tester

def main():
    print("Welcome to the Grade Calculator!")
    CALCULATOR = calculator_class.Calculator()
    tester.test(CALCULATOR) # for testing purposes
    #file_name = input("What is the name of the file? (eg. grades.txt) : ")
    #TODO read/write from file
    while True:
        # choose action
        print("What would you like to do? (Enter number of action)")
        action = input("1. Add/Modify a Semester\n2. Add/Modify a Course\n3. View Summary\n4. Exit\n")
        if action == "1": # modify semester
            while True:
                print("What would you like to do? (Enter number of action)")
                sem_action = input("1. Add a Semester\n2. Remove a Semester\n3. Modify Semester information\n4. Exit\n")
                print("Reminder: semester grades are calculated according to the average of the courses in the semester. Exit and choose 2 to modify course grades.")
                print("Semester grades are automatically calculated when you add a course. They are set to 0 by default.")
                if sem_action == "1": # add semester
                    semester_name = input("What is the name of the semester? (eg. fall2020) : ")
                    CALCULATOR.add_semester(semester_name)
                    break
                elif sem_action == "2": # remove semester
                    print("Which semester would you like to remove? (Enter semester name)")
                    print("Semesters:")
                    CALCULATOR.print_semesters()
                    semester = input()
                    removed, message = CALCULATOR.remove_semester(semester)
                    print(message)
                    if removed:
                        break
                    else:
                        continue
                elif sem_action == "3": # modify semester information
                    print("Which semester would you like to modify the name of? (Enter semester name)")
                    print("Semesters:")
                    CALCULATOR.print_semesters()
                    semester = input()
                    changed, message = CALCULATOR.change_semester_name(semester)
                    print(message)
                    if changed:
                        break
                    else:
                        continue
                elif sem_action == "4": # exit
                    break
                else:
                    print("Invalid input. Please try again. (Enter number of action only)")
                    continue
        elif action == "2": # modify course
            while True:    
                print("Which semester would you like to modify a course for? (Enter semester name)")
                print("Semesters:")
                CALCULATOR.print_semesters()
                semester = input()
                sem_exists, message = CALCULATOR.check_semester(semester)
                if not sem_exists:
                    print(message)
                    continue
                else:
                    break
            while True:
                print("What would you like to do? (Enter number of action)")
                course_action = input("1. Add a Course\n2. Remove a Course\n3. Modify Course information\n4. Exit\n")
                print("Reminder: course grades are calculated according to the average of the sections in the course. Choose 3 to modify section grades.\n")
                if course_action == "1": # add course (update semester grade)
                    print("Which course would you like to add? (Enter course code)")
                    course = input()
                    print(CALCULATOR.add_course(semester, course))
                    break
                elif course_action == "2": # remove course (update semester grade)
                    print("Which course would you like to remove? (Enter course code)")
                    print("Courses:")
                    CALCULATOR.print_courses(semester)
                    course = input()
                    print(CALCULATOR.remove_course(semester, course))
                    break
                elif course_action == "3": # modify course information (name, section modification, subsection modification)
                    print("Which course would you like to modify? (Enter course code)")
                    print("Courses:")
                    CALCULATOR.print_courses(semester)
                    course = input()
                    course_exists, message2 = CALCULATOR.check_course(semester, course)
                    if not course_exists:
                        print(message2)
                        continue
                    while True:
                        print("What would you like to do? (Enter number of action)")
                        course_action = input("1. Modify Course code\n2. Modify a Section\n3. Exit\n")
                        print("Reminder: course grades are calculated according to the average of the sections in the course. Choose 2 to modify section/subsection grades.\n")
                        if course_action == "1": # modify course code
                            new_code = input("What is the new course code? (eg. comp424) : ")
                            print(CALCULATOR.change_course_code(semester, course, new_code))
                            break
                        elif course_action == "2": # modify section (name, add section, remove section, edit section)
                            while True:
                                print("What would you like to do? (Enter number of action)")
                                section_action = input("1. Add a Section\n2. Remove a Section\n3. Modify a Section\n4. Exit\n")
                                print("Reminder: section grades are calculated according to the average of the subsections in the section. Choose 3 to modify subsection grades.\n")
                                print("(Note: if there are no subsections, the section grade is 0. Add a section, choose 3 and then add a subsection to add a grade.)\n")
                                if section_action == "1": # add section
                                    section_name = input("What is the name of the section? (eg. assignments/midterm) : ")
                                    section_weight = float(input("What is the weight of the section? (eg. 50) : "))
                                    print(CALCULATOR.add_section(semester, course, section_name, section_weight))  
                                    break
                                elif section_action == "2": # remove section
                                    print("Which section would you like to remove? (Enter section name)")
                                    print("Sections:")
                                    CALCULATOR.print_sections(semester, course)
                                    section_name = input()
                                    print(CALCULATOR.remove_section(semester, course, section_name))
                                    break
                                elif section_action == "3": # modify section (name, add subsection, remove subsection, edit subsection)
                                    while True:
                                        # if section option empty - forced exit
                                        if len(CALCULATOR.get_sections(semester, course)) == 0:
                                            print("There are no sections to modify. Exiting...")
                                            break
                                        print("What would you like to do? (Enter number of action)")
                                        subsection_action = input("1. Change Section name\n2. Add a Subsection\n3. Remove a Subsection\n4. Modify a Subsection name\n5. Modify a Subsection Grade\n6. Exit\n")
                                        print("Reminder: subsection grades are calculated according to the percentage received. Choose 3 to modify subsection grades.\n")
                                        print("Which section would you like to modify a subsection in? (Enter section name)")
                                        print("Sections:")
                                        CALCULATOR.print_sections(semester, course)
                                        section_name = input()
                                        section_exists, message3 = CALCULATOR.check_section(semester, course, section_name)
                                        if not section_exists:
                                            print(message3)
                                            continue
                                        if subsection_action == "1": # change section name
                                            new_name = input("What is the new name of the section? (eg. assignments/midterm) : ")
                                            print(CALCULATOR.change_section_name(semester, course, section_name, new_name))
                                            break
                                        elif subsection_action == "2": # add subsection
                                            subsection_name = input("What is the name of the subsection? (eg. assignment 1/2/3...) : ")
                                            subsection_weight = float(input("What is the weight of the subsection? (eg. 50) : "))
                                            subsection_grade = float(input("What is the grade of the subsection? (eg. 80) : ")) 
                                            print(CALCULATOR.add_subsection(semester, course, section_name, subsection_name, subsection_weight, subsection_grade))
                                            break
                                        elif subsection_action == "3": # remove subsection
                                            print("Which subsection would you like to remove? (Enter subsection name)")
                                            print("Subsections:")
                                            CALCULATOR.print_subsections(semester, course, section_name)
                                            subsection_name = input()
                                            subsection_exists, message4 = CALCULATOR.check_subsection(semester, course, section_name, subsection_name)
                                            if not subsection_exists:
                                                print(message4)
                                                continue
                                            print(CALCULATOR.remove_subsection(semester, course, section_name, subsection_name))
                                            break
                                        elif subsection_action == "4": # modify subsection name
                                            print("Note: if there are no subsections, give the name of the section when prompted for the subsection name.")
                                            print("Which subsection would you like to modify? (Enter subsection name)")
                                            print("Subsections:")
                                            CALCULATOR.print_subsections(semester, course, section_name)
                                            subsection_name = input()
                                            subsection_exists, message4 = CALCULATOR.check_subsection(semester, course, section_name, subsection_name)
                                            if not subsection_exists:
                                                print(message4)
                                                continue
                                            new_name = input("What is the new name of the subsection? (eg. assignment 1/2/3...) : ")
                                            print(CALCULATOR.change_subsection_name(semester, course, section_name, subsection_name, new_name))
                                            break
                                        elif subsection_action == "5": # modify subsection grade
                                            print("Note: if there are no subsections, give the name of the section when prompted for the subsection name.")
                                            print("Which subsection would you like to modify? (Enter subsection name)")
                                            print("Subsections:")
                                            CALCULATOR.print_subsections(semester, course, section_name)
                                            subsection_name = input()                                            
                                            subsection_exists, message4 = CALCULATOR.check_subsection(semester, course, section_name, subsection_name)
                                            if not subsection_exists:
                                                print(message4)
                                                continue
                                            new_grade = float(input("What is the new grade of the subsection? (eg. 80) : "))
                                            print(CALCULATOR.edit_subsection_grade(semester, course, section_name, subsection_name, new_grade))
                                            break
                                        elif subsection_action == "6": # exit
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
        elif action == "3": # view summary
            print("\n")
            TABLE = tables.Table()
            TABLE.print_table(CALCULATOR)
            print("\n")
        elif action == "4": # exit
            print("Would you like to save your changes? (Enter number of action)")
            save_action = input("1. Yes\n2. No\n")
            if save_action == "1":
                print("Warning: this will overwrite the file if it already exists.")
                file_name = input("What is the name of the file? (eg. grades.txt) : ")
                f = open(file_name, "w")
                tt = TABLE.tab(CALCULATOR)
                f.write(tt)
                f.close()
                print("Changes were saved. Goodbye!")
                break
            elif save_action == "2":
                print("Goodbye!")
                break
            else:
                print("Invalid input. Please try again. (Enter number of action only)")
                continue
        else:
            print("Invalid input. Please try again. (Enter number of action only)")
            continue

main()
