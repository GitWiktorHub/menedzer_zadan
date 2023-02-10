from tkinter import *
import os

root = Tk()
root.geometry("500x200")

# FUNCTIONS
def import_from_file(file_name):
    file = open(file_name, "r")
    global list_of_tasks
    list_of_tasks = file.readlines()
    file.close()


def show_tasks():
    import_from_file('tasks.txt')
    listbox.delete(0, END)
    for task in list_of_tasks:
        listbox.insert(END, task)


def find_in_listbox():  # wyjątek jeśli nie ma zadania
    import_from_file('tasks.txt')
    index = 7
    task_name = entry_var.get() + "  "
    for i, elem in enumerate(list_of_tasks):
        if elem == task_name:
            index = i
    try:
        listbox.see(index)
    except TclError as e:
        print(e)


def remove_task():  # wyjątek jeśli nie ma zadania
    import_from_file('tasks.txt')
    task_name = entry_var.get()
    for task in list_of_tasks:
        if task == task_name:
            list_of_tasks.remove(task)
    os.remove('tasks.txt')
    file = open('tasks.txt', 'a+')
    for task in list_of_tasks:
        file.write(task)
    file.close()
    show_tasks()


def add_task():
    print('add_task() is running')
    file = open('tasks.txt', 'a+')
    new_task = entry_task_name_var.get()
    file.write(new_task+'\n')
    file.close()
    global description
    description = task_description.get(1.0, END)
    file = open('files/{}.txt'.format(new_task), 'a+')
    file.writelines(description)
    file.close()
    show_tasks()
    window.destroy()


def show_adding_window():
    global window
    window = Tk()
    window.title('Add a new task')
    window.geometry('300x200')
    global enter_name_label  # label do task name'a
    enter_name_label = Label(window, text='Enter here task name: ')
    enter_name_label.pack()
    enter_name_label.place(x=10, y=10)

    global entry_task_name_var  # zmienna przechwytująca to co jest w entry
    entry_task_name_var = StringVar(master=window)

    global entry_task_name  # pole do wpisania nazwy zadania
    entry_task_name = Entry(window, textvariable=entry_task_name_var)
    entry_task_name.pack()
    entry_task_name.place(x=10, y=30)

    global task_description_label  # label do pola na opis zadania
    task_description_label = Label(window, text='Enter here task description: ')
    task_description_label.pack()
    task_description_label.place(x=10, y=50)

    global task_description  # pole opisowe zadania
    task_description = Text(window, width=130, height=280,)
    task_description.pack()
    task_description.place(x=10, y=70)

    global plus  # przycisk dodający zadanie
    plus = Button(window, text='add task', command=add_task)
    plus.pack(side=BOTTOM)
    plus.place(x=220, y=10)

    window.mainloop()


def clear_all_tasks():
    open('tasks.txt', 'w').close()

    for file in os.listdir('files'):
        try:
            os.remove(file)
        except FileNotFoundError:
            print("nie odnaleziono pliku")

    show_tasks()


def listbox_select(index):
    entry_var.set(listbox.get(listbox.curselection()))


# WIDGETS
# Entry
label_var = StringVar(root, 'Find in the list or type here: ')
label = Label(root, textvariable=label_var)
label.pack()
label.place(x=10, y=10)

entry_var = StringVar(root)
entry_var.set('type task name...')
edit = Entry(root, textvariable=entry_var)
edit.pack()
edit.place(x=10, y=30, width=150)

# Listbox
list_label = Label(root, text='Here is your list of tasks')
list_label.pack()
list_label.place(x=10, y=60)

listbox = Listbox(root, width=50, height=6)
listbox.pack()
listbox.place(x=10, y=80)

# MENUS
mainmenu = Menu()
root.config(menu=mainmenu)

opt_menu = Menu(mainmenu)
mainmenu.add_cascade(label='Options', menu=opt_menu)

settings_menu = Menu(mainmenu)
mainmenu.add_cascade(label='Settings', menu=settings_menu)

opt_menu.add_command(label='Add task', command=show_adding_window)
opt_menu.add_command(label='Remove task')
opt_menu.add_command(label='Read description about the task')
opt_menu.add_command(label='Edit task')
opt_menu.add_command(label='Remove task')
opt_menu.add_separator()
opt_menu.add_command(label='Show tasks in text window')
opt_menu.add_separator()
opt_menu.add_command(label='clear all tasks')


# Opis zadań, pole textowe przy dodawaniu zadań
'''
Tutorial(menu) jak korzystać z menagera,
messagebox zaimportować
obsługa wyjątków
(przy entry, jeśli nie ma takiego zadania w liście, lub pliku)
'''

listbox.bind('<<ListboxSelect>>', listbox_select)

# BUTTONS
# Require new, confirming window
add_task_button = Button(root, text='new task', command=show_adding_window)
clear_all_tasks_button = Button(root, text='clear tasks list', command=clear_all_tasks)  # okno potwierdzające

# Choose from the list
find_button = Button(root, text='find', command=find_in_listbox)
remove_task_button = Button(root, text='remove task', command=remove_task)  # obsłużyć wyjątek, jeżeli nie ma takiego zadania w liście - error
read_description_button = Button(root, text='read description')  # okno z labelami
edit_task_button = Button(root, text='edit task')  # okno z polem tekstowym jak przy dodawaniu zadań

# packing
add_task_button.pack()
remove_task_button.pack()
read_description_button.pack()
edit_task_button.pack()
clear_all_tasks_button.pack()
find_button.pack()

# placing
add_task_button.place(x=325, y=10)
remove_task_button.place(x=325, y=40)
read_description_button.place(x=325, y=70)
edit_task_button.place(x=325, y=100)
clear_all_tasks_button.place(x=325, y=130)
find_button.place(x=165, y=25)
show_tasks()

root.mainloop()
