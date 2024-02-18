import os
from datetime import datetime, date

class TaskManager:
    """Task Manager class for functions"""
    def __init__(self):
        self.username_password = {}
        self.task_list = []

        self.DATETIME_STRING_FORMAT = "%Y-%m-%d"

        self.load_user_data()
        self.load_task_data()

    def load_user_data(self):
        if not os.path.exists("user.txt"):
            with open("user.txt", "w") as default_file:   
                default_file.write("admin;password\n")

        with open("user.txt", 'r') as user_file:
            user_data = user_file.read().split("\n")
        
        for user in user_data:
            if not user:
                continue
            username, password = user.split(';')
            self.username_password[username] = password

    def load_task_data(self):
        if not os.path.exists("tasks.txt"):
            return

        with open("tasks.txt", "r") as task_file:
            task_data = task_file.read().split("\n")

        for t_str in task_data:
            if not t_str:
                continue
            curr_t = {}
            task_components = t_str.split(";")
            curr_t['number'] = task_components[0]
            curr_t['username'] = task_components[1]
            curr_t['title'] = task_components[2]
            curr_t['description'] = task_components[3]
            curr_t['due_date'] = datetime.strptime(task_components[4], self.DATETIME_STRING_FORMAT)
            curr_t['assigned_date'] = datetime.strptime(task_components[5], self.DATETIME_STRING_FORMAT)
            curr_t['completed'] = task_components[6]

            self.task_list.append(curr_t)

    def save_task_data(self):
        with open("tasks.txt", "w") as task_file:
            for task in self.task_list:
                str_attrs = [
                    str(task['number']),
                    task['username'],
                    task['title'],
                    task['description'],
                    task['due_date'].strftime(self.DATETIME_STRING_FORMAT),
                    task['assigned_date'].strftime(self.DATETIME_STRING_FORMAT),
                    task['completed']
                ]
                task_file.write(";".join(str_attrs) + "\n")

    def register_user(self):
        new_username = input("New Username: ")

        while new_username in self.username_password:
            print("Username already exists")
            new_username = input("New Username: ")    

        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")

        while new_password != confirm_password:
            print("Passwords do not match")
            new_password = input("New Password: ")
            confirm_password = input("Confirm Password: ")

        self.username_password[new_username] = new_password
        with open("user.txt", "a") as user_file:
            user_file.write(f"{new_username};{new_password}\n")
        print("New User Added")

    def add_task(self):
        task_username = input("Name of person assigned to task: ")
        while task_username not in self.username_password:
            print("User does not exist. Please enter a valid username")
            task_username = input("Name of person assigned to task: ")
            
        task_title = input("Title of Task: ").capitalize()
        task_description = input("Description of Task: ")

        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, self.DATETIME_STRING_FORMAT)
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

        task_count = len(self.task_list) + 1
        curr_date = date.today()

        task = {
            "number" : str(task_count),
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": task_status
        }

        self.task_list.append(task)
        self.save_task_data()
        print("Task successfully added.")

    def view_all(self):
        for t in self.task_list:
            disp_str = f"Task number: \t {t['number']}\n"
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(self.DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(self.DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n{t['description']}\n"
            disp_str += f"Completed: \t {t['completed']}"
            print("-----------------------------------")
            print(disp_str)    
            print("-----------------------------------")

    def view_mine(self, curr_user):
        print(f"\n-------- {curr_user}'s tasks --------")
        user_tasks = [t for t in self.task_list if t['username'] == curr_user]
        if not user_tasks:
            print("No tasks open for you! Well done!")
            self.view_all()
            return
        for t in user_tasks:
            disp_str = f"Task number: \t {t['number']}\n"
            disp_str += f"Task: \t\t {t['title']}"
            print("-----------------------------------")
            print(disp_str)
            print("-----------------------------------")
        self.task_selector(user_tasks)

    def task_selector(self, user_tasks):
        while True:
            task_number = input('''Select a task to view in detail (use task number)
                                Type -1 to exit\n''')
            
            if task_number == '-1':
                return

            selected_task = next((task for task in user_tasks if task['number'] == task_number), None)

            if selected_task:
                disp_str = f"Task number: \t {selected_task['number']}\n"
                disp_str += f"Task: \t\t {selected_task['title']}\n"
                disp_str += f"Assigned to: \t {selected_task['username']}\n"
                disp_str += f"Date Assigned: \t {selected_task['assigned_date'].strftime(self.DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {selected_task['due_date'].strftime(self.DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Completed: \t {selected_task['completed']}\n\n"
                disp_str += f"Task Description: \n{selected_task['description']}"

                print("-----------------------------------")
                print(disp_str)
                print("-----------------------------------")
                self.task_editor(selected_task)
                break 

            print(f"Task with number {task_number} not found.")

    def task_editor(self, selected_task):
        editor = input("Have you completed this task? (yes/no)\n")
        if editor.lower() == "yes":
            selected_task['completed'] = 'yes'
            self.save_task_data()
            print("Task marked as complete.")
        elif editor.lower() == "no":
            selected_task['completed'] = 'no'
            self.save_task_data()
            print("Task marked as incomplete.")

        '''Function to write a task report to the task_overview.txt file
        -   num_tasks, counts every task in task_list
        -   num_complete_tasks, counts all tasks with complete == yes
        -   num_incomplete_tasks, counts all tasks with complete == no
        -   num_overdue_tasks, counts all tasks with complete == no and due_date is passed
        The data is converted to strings and added to user_overview.txt
        message appears to show it has been successful'''
    def task_report(self,task_list):
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
    def user_report(self,task_list):
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
    def display_statistics(self):
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

    def run(self):
        while True:
            print("\n-------------------------")
            print("Welcome to Task Manager")
            print("""-------------------------
        r   -   Registering a user
        a   -   Adding a task
        va  -   View all tasks
        vm  -   View my task  
        gr  -   Generate reports            
        ds  -   Display statistics
        e   -   Exit""")
            choice = input("Select an option: ")

            if choice == "r":
                self.register_user()
            elif choice == "a":
                self.add_task()
            elif choice == "va":
                self.view_all()
            elif choice == "vm":
                username = input("Enter your username: ")
                if username in self.username_password:
                    self.view_mine(username)
                else:
                    print("Invalid Username.")
            elif choice == "gr":
                while True:
                    report_option = input('''
        1     -   Task report
        2     -   User Report
        -1    -   Return to menu
        Select an option: ''')
                    if report_option == "1":
                        self.task_report(self)

                    elif report_option == "2":
                        self.user_report(self)

                    elif report_option == "-1":
                        self.run()
                    else:
                        print ("Error, option not available")
            elif choice == "ds":
                self.display_statistics()
            elif choice == "e":
                print("Exiting Task Manager. Goodbye!")
                break
            else:
                print("Invalid Choice. Please select again.")

if __name__ == "__main__":
    tm = TaskManager()
    tm.run()