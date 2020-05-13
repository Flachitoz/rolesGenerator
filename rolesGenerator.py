import tkinter as tk
from utils.utilities import resource_path
from db.db import Db
from generator.generator import Generator


# window
master = tk.Tk()
master.title("Kids role generator")
master.wm_iconbitmap(resource_path('puzzle.ico'))
master.geometry("450x380")

# frames
top_frame = tk.Frame(master)
top_frame.pack(side='top')
bottom_frame = tk.Frame(master)
bottom_frame.pack(side='top')

database = Db()
generator = Generator(database)

if not database.are_tables_connected(["students", "roles", "september"]):
    database.create_actor_tables()

    # top labels, entries and buttons ( NAME SURNAME )
    name_label = tk.Label(top_frame, text="Name", font='Arial', fg='light sky blue')
    name_label.grid(row=0, padx=10, pady=10, sticky='w')

    name_text = tk.Entry(top_frame, width=30)
    name_text.grid(row=0, column=1, ipady=3)

    add_student_button = tk.Button(top_frame, text='Add student', bg='white', fg='blue',
                                   command=lambda: database.add_actor("students", name_text, surname_text))
    add_student_button.grid(row=1, column=2, padx=50)

    surname_label = tk.Label(top_frame, text="Surname", font='Arial', fg='light sky blue')
    surname_label.grid(row=2, padx=10, sticky='w')

    surname_text = tk.Entry(top_frame, width=30)
    surname_text.grid(row=2, column=1, padx=10, pady=10, ipady=3)

    # center label, entry and button ( ROLE )
    role_label = tk.Label(top_frame, text="Role", font='Arial', fg='green2')
    role_label.grid(row=3, column=0, padx=10, pady=40, sticky='w')

    role_text = tk.Entry(top_frame, width=30)
    role_text.grid(row=3, column=1, padx=10, pady=40, ipady=3)

    add_role_button = tk.Button(top_frame, text='Add role', bg='white', fg='green4',
                                command=lambda: database.add_actor("roles", role_text))
    add_role_button.grid(row=3, column=2, padx=50, pady=40)

    # bottom button ( GENERATE )
    generate_button = tk.Button(bottom_frame, text='Generate roles for the first month!', bg='gold', fg='black',
                                width=30, height=2, command=lambda: generator.generate_roles_per_student(True))
    generate_button.grid(row=0, column=1, pady=10)

    # bottom button ( RESET )
    reset_button = tk.Button(bottom_frame, text='Reset all!', bg='red', fg='black',
                             width=30, height=2, command=database.drop_tables)
    reset_button.grid(row=1, column=1, pady=20)

else:

    # top button ( GENERATE )
    generate_button = tk.Button(top_frame, text='Generate roles for next month!', bg='gold', fg='black',
                                width=30, height=2, command=lambda: generator.generate_roles_per_student(False))
    generate_button.pack(pady=40)

    # bottom button ( RESET )
    reset_button = tk.Button(bottom_frame, text='Reset all!', bg='red', fg='black',
                             width=30, height=2, command=database.drop_tables)
    reset_button.pack(pady=40)

master.mainloop()
