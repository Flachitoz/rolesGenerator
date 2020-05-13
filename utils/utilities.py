import os
import sys
from tkinter.messagebox import showinfo


def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def show_message(message, message_type="Warning"):
    showinfo(message_type, message)


def are_fields_present(table, column1, column2):
    if table == "students" and (not column1.get() or not column2.get()):
        if not column1.get() and not column2.get():
            show_message("Name and surname are missing!")
        elif not column1.get():
            show_message("Name is missing!")
        elif not column2.get():
            show_message("Surname is missing!")
        return False
    
    elif table == "roles" and not column1.get():
        show_message("Role is missing!")
        return False
    
    return True
