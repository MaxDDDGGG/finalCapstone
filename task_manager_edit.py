import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"
'''Function to read tasks.txt and creates the task list, which is called upon in other functions'''
def read_tasks():
    with open("tasks.txt", "r") as task_file:
        task_data = task_file.read().split("\n")
    
    task_list = []
    for t_str in task_data:
        if not t_str:
            continue
        curr_t = {}
        task_components = t_str.split(";")
        curr_t['number'] = task_components[0]
        curr_t['username'] = task_components[1]
        curr_t['title'] = task_components[2]
        curr_t['description'] = task_components[3]
        curr_t['due_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[5], DATETIME_STRING_FORMAT)
        curr_t['completed'] = task_components[6]

        task_list.append(curr_t)

    return task_list

'''Function to add a user to users.txt.
Firstly it checks if user is already added and prints an error if they are, then loops back to ask again
when inputting the password they are checked, if they match and prints error and loop in not
after everything is correct, the username and password are written to the user.txt'''
def register_user(username_password):
    new_username = input("New Username: ")

    while new_username in username_password:
        print("Username already exists")
        new_username = input("New Username: ")    

    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    while not new_password == confirm_password:
        print("Passwords do not match")
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")

    else:
        print("New User Added")
        username_password[new_username] = new_password
        with open("user.txt", "w") as user_file:
            user_data = [f"{k};{v}" for k, v in username_password.items()]
            user_file.write("\n".join(user_data) + "\n")

'''Function to add a task to the tasks.txt and task list
Task is assigned to user - Check if user exists, if not error message appears, then loop back
task title and descriptions are input
task due date is input, check if in correct format, else error and loop back to redo date only
Then completed (yes/no) added, for user to say if it is finished,
message to say task addded to file
task count is used to count the number of tasks on tasks.txt to assign the next number to the new task 
(The tasks are numbered chronologically)
curr_date, finds todays date to apply the date set.
append task to tasks.txt'''
def add_task():
    task_username = input("Name of person assigned to task: ")
    while task_username not in username_password:
        print("User does not exist. Please enter a valid username")
        task_username = input("Name of person assigned to task: ")
        
    else:
        task_title = input("Title of Task: ").capitalize()
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break
            except ValueError:
                print("Invalid datetime format. Please use the format specified")
        
        task_status = input("Completed (yes/no): ").lower()
        if task_status == "yes":
            print("-----------------------------")
            print("Well done! for completing your task!")
        elif task_status == "no":
            print("-----------------------------")
            print("Task marked as incomplete.")

        try:
            task_count = len(read_tasks())
            task_number = task_count + 1
        except ValueError:
            task_number = 1
        
        curr_date = date.today()

        task_list = {
            "number" : str(task_number),
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": task_status
        }

        with open("tasks.txt", "a") as task_file:
            str_attrs = [
                str(task_list['number']),
                task_list['username'],
                task_list['title'],
                task_list['description'],
                task_list['due_date'].strftime(DATETIME_STRING_FORMAT),
                task_list['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                task_list['completed']
            ]
            task_file.write(";".join(str_attrs) + "\n")
   
        print(f"Task successfully added.")
        print("------------------------------\n")

'''function to view all tasks on tasks.txt, using read_task function for ease,
prints out out the contents of tasks.txt in easy to read format'''
def view_all(task_list):
    task_list = read_tasks()
    for t in task_list:
        disp_str = f"Task number: \t {t['number']}\n"
        disp_str += f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n{t['description']}\n"
        disp_str += f"Completed: \t {t['completed']}"
        print("-----------------------------------")
        print(disp_str)    
        print("-----------------------------------")

'''Function to select a task to view in detail (made to be used in view mine function)
User will select a task number, if number does not exist (or not a number) an error message appears and loops back round.
if -1 is input, the user is taken back to the main menu
when a task number is input (from 1 +) the task is shown in full and then the task editor is run'''
def task_selector(task_list):
    while True:
        task_number = input('''Select a task to view in detail (use task number)
                            Type -1 to exit\n''')
        
        if task_number == '-1':
            menu()

        selected_task = next((task for task in task_list if task['number'] == task_number), None)

        if selected_task:
            disp_str = f"Task number: \t {selected_task['number']}\n"
            disp_str += f"Task: \t\t {selected_task['title']}\n"
            disp_str += f"Assigned to: \t {selected_task['username']}\n"
            disp_str += f"Date Assigned: \t {selected_task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {selected_task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Completed: \t {selected_task['completed']}\n\n"
            disp_str += f"Task Description: \n{selected_task['description']}"

            print("-----------------------------------")
            print(disp_str)
            print("-----------------------------------")
            task_editor(task_number, task_list, disp_str)
            break 

        print(f"Task with number {task_number} not found.")

'''Function to edit the tasks
with an input - is task complete (yes or no)
yes, chnages the completion status to yes and then goes back to the main menu,
no, changes the completion status to no, and then shows the editor menu - task owner and due date can be amended and -1 is exit to main menu.
after they have been amended the task is shown in full with changes and then loops back to editor menu to make another selection or exit'''
def task_editor(task_number, task_list, disp_str):
    editor = input("Have you completed this task? (yes/no): ").lower()

    for task in task_list:
        if str(task['number']) == str(task_number):
            if editor == "yes":
                task['completed'] = "yes"
                print("\nStatus changed to complete!")
                with open("tasks.txt", "w") as task_file:
                    for task in task_list:
                        str_attrs = [
                            str(task['number']),
                            task['username'],
                            task['title'],
                            task['description'],
                            task['due_date'].strftime(DATETIME_STRING_FORMAT),
                            task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                            task['completed']
                        ]
                disp_str = f"Task number: \t {task['number']}\n"
                disp_str += f"Task: \t\t {task['title']}\n"
                disp_str += f"Assigned to: \t {task['username']}\n"
                disp_str += f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \n{task['description']}\n"
                disp_str += f"\nCompleted: \t {task['completed']}"
                
                print("-----------------------------------")
                print(disp_str)
                print("-----------------------------------")
                menu()
            elif editor == "no":
                task['completed'] = "no"
                while True:
                    task_change = input(
'''
-----Editor menu-----
1   -   Task owner
2   -   Task due date
-1  -   Return to menu
Select a number: ''')
                    if task_change == '1':
                        task['username'] = input("Assign task to new user: ")
                        while task['username'] not in username_password:
                            print("\nUser does not exist. Please enter a valid username\n")
                            task['username'] = input("Assign task to new user: ")
                        
                    elif task_change == '2':
                        while True:
                            try:
                                task['due_date'] = datetime.strptime(input("Enter new due date (YYYY-MM-DD): "), DATETIME_STRING_FORMAT)
                                break
                            except ValueError:
                                print("Invalid date format. Please use the format specified.")
                    elif task_change == '-1':
                        menu()
                    else:
                        print("Error, option not available")
                    
                    with open("tasks.txt", "w") as task_file:
                        for task in task_list:
                            str_attrs = [
                                str(task['number']),
                                task['username'],
                                task['title'],
                                task['description'],
                                task['due_date'].strftime(DATETIME_STRING_FORMAT),
                                task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                task['completed']
                            ]
                        task_file.write(";".join(str_attrs) + "\n")

                    disp_str = f"Task number: \t {task['number']}\n"
                    disp_str += f"Task: \t\t {task['title']}\n"
                    disp_str += f"Assigned to: \t {task['username']}\n"
                    disp_str += f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                    disp_str += f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                    disp_str += f"Task Description: \n{task['description']}\n"
                    disp_str += f"\nCompleted: \t {task['completed']}"
                    
                    print("-----------------------------------")
                    print(disp_str)
                    print("-----------------------------------")
                    break
            else: 
                print ("\nError- \nInappropriate response")
                return
        else:
            print(f"\nError- \nTask number {task_number} not found.")

'''Function to view summaries of tasks, if there are no tasks open for the logged in user, the view_all function is called'''
def view_mine(curr_user, task_list):
    print(f"\n-------- {curr_user}'s tasks --------")
    try:
        for t in task_list:
            if t['username'] == curr_user:
                disp_str = f"Task number: \t {t['number']}\n"
                disp_str += f"Task: \t\t {t['title']}"
                print("-----------------------------------")
                print(disp_str)
                print("-----------------------------------")
        task_selector(task_list)
    except:
        print("No tasks open for you! Well done!")
        view_all(task_list)

'''Function to write a task report to the task_overview.txt file
    -   num_tasks, counts every task in task_list
    -   num_complete_tasks, counts all tasks with complete == yes
    -   num_incomplete_tasks, counts all tasks with complete == no
    -   num_overdue_tasks, counts all tasks with complete == no and due_date is passed
    The data is converted to strings and added to user_overview.txt
    message appears to show it has been successful'''
def task_report(task_list):
    num_tasks = sum(1 for t in task_list) 
    num_complete_tasks = sum(1 for t in task_list if t['completed'] == "yes") 
    num_incomplete_tasks = sum(1 for t in task_list if t['completed'] == "no") 
    num_overdue_tasks = sum(1 for t in task_list if t['completed'] == "no" and t['due_date'].date() < date.today()) 
    percentage_incomplete = (num_incomplete_tasks / num_tasks) * 100
    percentage_overdue = (num_overdue_tasks / num_tasks) * 100

 
    task_report_dict = {
        'tasks_count': num_tasks,
        'complete_count': num_complete_tasks,
        'incomplete_count': num_incomplete_tasks,
        'overdue_count': num_overdue_tasks,
        'incomplete_percentage': percentage_incomplete,
        'overdue_percentage': percentage_overdue,
    }

    with open("task_overview.txt","w") as report_file:
        str_tasks = [
            str(task_report_dict['tasks_count']),
            str(task_report_dict['complete_count']),
            str(task_report_dict['incomplete_count']),
            str(task_report_dict['overdue_count']),
            str(task_report_dict['incomplete_percentage']),
            str(task_report_dict['overdue_percentage'])
        ]
        report_file.write(";".join(str_tasks) + "\n")     
        print("\n The report has been generated successfully\n")    

'''function for generating the user specific report, works by iterating through the task list and counting each task that meets the criteria 
    -   total, counts all tasks assigned to current user
    -   complete, counts all tasks with complete == yes and assigned to current user
    -   incomplete, counts all tasks with complete == no and assigned to current user
    -   overdue, counts all tasks with complete == no and due_date is passed and assigned to current user
            -   overdue check is before incomplete in the iterations to aboid everything stopping at just incomplete
            -   overdue also adds to incomplete.
    The data is converted to strings and added to user_overview.txt
    message appears to show it has been successful'''
def user_report(task_list):
    user_tasks = {}

    for task in task_list:
        username = task['username']
        if username not in user_tasks:
            user_tasks[username] = {'total': 0, 'complete': 0, 'incomplete': 0, 'overdue': 0}

        user_tasks[username]['total'] += 1
        complete = task['completed']
        due_date = task['due_date']

        if complete == "yes":
            user_tasks[username]['complete'] += 1
        elif complete == "no" and due_date.date() < date.today():
            user_tasks[username]['overdue'] += 1
            user_tasks[username]['incomplete'] += 1
        elif complete == "no":
            user_tasks[username]['incomplete'] += 1

    with open("user_overview.txt", "w") as report_file:
        for username, data in user_tasks.items():
            user_percentage_complete = (data['complete'] / data['total']) * 100
            user_percentage_incomplete = (data['incomplete'] / data['total']) * 100
            user_percentage_overdue = (data['overdue'] / data['total']) * 100

            str_users = [
                username,
                str(data['total']),
                str(data['complete']),
                str(data['incomplete']),
                str(data['overdue']),
                str(user_percentage_complete),
                str(user_percentage_incomplete),
                str(user_percentage_overdue),
            ]
            report_file.write(";".join(str_users) + "\n")

    print("\nThe report has been generated successfully\n")

'''Function to display the data from task_overview.txt and user_overview.txt
The data has been semi split, the number of users has been placed first, in the tasks over view section
Then each user with tasks has a section of the report'''
def display_statistics():
    reports = []

    with open("task_overview.txt", "r") as report_file:
        task_report_data = report_file.read().split("\n")

    for tasks in task_report_data:
        if not tasks:
            continue
        rep_t = {}
        rep_components = tasks.split(";")
        rep_t['tasks_count'] = rep_components[0]
        rep_t['complete_count'] = rep_components[1]
        rep_t['incomplete_count'] = rep_components[2]
        rep_t['overdue_count'] = rep_components[3]
        rep_t['incomplete_percentage'] = round(float(rep_components[4]))
        rep_t['overdue_percentage'] = round(float(rep_components[5]))

        reports.append(rep_t)

    with open("user_overview.txt", "r") as report_file:
        user_report_data = report_file.read().split("\n")

    for user in user_report_data:
        if not user:
            continue
        rep_u = {}
        rep_components = user.split(";")
        rep_u['username'] = rep_components[0]
        rep_u['total'] = rep_components[1]
        rep_u['complete'] = rep_components[2]
        rep_u['incomplete'] = rep_components[3]
        rep_u['overdue'] = rep_components[4]
        rep_u['user_percentage_complete'] = round(float(rep_components[5]))
        rep_u['user_percentage_incomplete'] = round(float(rep_components[6]))
        rep_u['user_percentage_overdue'] = round(float(rep_components[7]))

        reports.append(rep_u)

    print("-----------------------------------------------")
    print("------------Task Manager Report------------")
    print("\n--------------Tasks Overview--------------")
    print(f"Number of users registered: \t\t{len(user_report_data)}")
    print(f"Total number of tasks: \t\t\t{reports[0]['tasks_count']}")
    print(f"Tasks completed: \t\t\t{reports[0]['complete_count']}")
    print(f"Tasks remaining: \t\t\t{reports[0]['incomplete_count']} ({reports[0]['incomplete_percentage']}%)")
    print(f"Tasks overdue: \t\t\t\t{reports[0]['overdue_count']} ({reports[0]['overdue_percentage']}%)")

    for user_data in reports[1:]:
        print(f"\n------------- {user_data['username']}'s Task Report -------------")
        print(f"Task count: \t\t\t\t{user_data['total']}")
        print(f"Completion percentage: \t\t\t{user_data['complete']} ({user_data['user_percentage_complete']}%)")
        print(f"Tasks remaining percentage: \t\t{user_data['incomplete']} ({user_data['user_percentage_incomplete']}%)")
        print(f"Tasks overdue percentage: \t\t{user_data['overdue']} ({user_data['user_percentage_overdue']}%)")
    print("-----------------------------------------------")

'''Function for the main menu which calls each of the sections''' 
def menu():
    while True:
        print()
        menu_choice = input('''Select one of the following Options below:
    r   -   Registering a user
    a   -   Adding a task
    va  -   View all tasks
    vm  -   View my task  
    gr  -   Generate reports            
    ds  -   Display statistics
    e   -   Exit
    : ''').lower()
        print()
        if menu_choice == 'r':
            register_user(username_password)

        elif menu_choice == 'a':
            add_task()

        elif menu_choice == 'va':
            view_all(task_list)

        elif menu_choice == 'vm':
            view_mine(curr_user, task_list)

        elif menu_choice == 'gr':
            while True:
                report_option = input('''
    1     -   Task report
    2     -   User Report
    -1    -   Return to menu
    Select an option: ''')
                if report_option == "1":
                    task_report(task_list)

                elif report_option == "2":
                    user_report(task_list)

                elif report_option == "-1":
                    menu()
                else:
                    print ("Error, option not available")

        elif menu_choice == 'e':
            print('Goodbye!!!')
            exit()

        elif menu_choice == 'ds' and curr_user == 'admin':
            display_statistics()

        else:
            print("You have made a wrong choice. Please Try again")

'''open up or create new files for tasks, users and task and user reports '''
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass
    
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:   
        default_file.write("admin;password")

if not os.path.exists("task_overview.txt"):
    with open("task_overview.txt", "w") as default_file:
        pass

if not os.path.exists("user_overview.txt"):
    with open("user_overview.txt", "w") as default_file:
        pass

with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")
username_password = {}
for user in user_data:
    if not user:
        continue
    username, password = user.split(';')
    username_password[username] = password

task_list = read_tasks()

'''Logging in function'''
logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password:
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True
        menu()