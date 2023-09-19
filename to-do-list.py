import tkinter as tk
import sqlite3 as sql

# Conecta a la base de datos SQLite3
connection = sql.connect("DatabaseToDoList.db")
cursor = connection.cursor()

# Crea la tabla de tareas si no existe
cursor.execute("CREATE TABLE IF NOT EXISTS TAREAS (ID INTEGER PRIMARY KEY, TITULO VARCHAR(50), DESCRIPCION VARCHAR(100), COMPLETADA BOOLEAN)")
connection.commit()

class Task:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.completed = False

class TaskList:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description):
        task = Task(title, description)
        self.tasks.append(task)

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True

    def list_tasks(self):
        return self.tasks

class TaskManagerApp:
    def __init__(self, root):
        self.task_list = TaskList()
        self.root = root
        self.root.title("To Do List")
        self.root.geometry("600x400")  # Cambiar las dimension

        self.title_label = tk.Label(root, text="Título:")
        self.title_label.pack()
        self.title_entry = tk.Entry(root)
        self.title_entry.pack()

        self.description_label = tk.Label(root, text="Descripción:")
        self.description_label.pack()
        self.description_entry = tk.Entry(root)
        self.description_entry.pack()

        self.add_button = tk.Button(root, text="Agregar Tarea", command=self.add_task)
        self.add_button.pack()

        self.task_listbox = tk.Listbox(root, width=80)
        self.task_listbox.pack()

        self.complete_button = tk.Button(root, text="Marcar como Completada", command=self.complete_task)
        self.complete_button.pack()

        self.remove_button = tk.Button(root, text="Eliminar Tarea", command=self.remove_task)
        self.remove_button.pack()

        self.list_tasks()  # Cargar tareas al inicio de la aplicación

    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        if title and description:
            self.task_list.add_task(title, description)
            self.insert_task_into_db(title, description)
            self.title_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.update_task_listbox()

    def insert_task_into_db(self, title, description):
        cursor.execute("INSERT INTO TAREAS (TITULO, DESCRIPCION, COMPLETADA) VALUES (?, ?, ?)", (title, description, 0))
        connection.commit()

    def complete_task(self):
        selected_task = self.task_listbox.curselection()
        if selected_task:
            index = selected_task[0]
            self.task_list.complete_task(index)
            task_id = self.get_task_id(index)
            self.update_task_as_completed(task_id)
            self.update_task_listbox()

    def update_task_as_completed(self, task_id):
        cursor.execute("UPDATE TAREAS SET COMPLETADA = 1 WHERE ID = ?", (task_id,))
        connection.commit()

    def remove_task(self):
        selected_task = self.task_listbox.curselection()
        if selected_task:
            index = selected_task[0]
            print(index)
            self.task_list.remove_task(index)
            task_id = self.get_task_id(index)
            print(task_id)
            self.delete_task_from_db(task_id)
            self.update_task_listbox()

    def delete_task_from_db(self, task_id):
        cursor.execute("DELETE FROM TAREAS WHERE ID = ?", (task_id,))
        connection.commit()

    def get_task_id(self, index):
        if 0 <= index <= len(self.task_list.tasks):
            cursor.execute("SELECT ID FROM TAREAS")
            task_ids = cursor.fetchall()
            return task_ids[index][0]
        else:
            return None


    def list_tasks(self):
        cursor.execute("SELECT * FROM TAREAS")
        tasks = cursor.fetchall()
        self.task_list.tasks = []  # Limpiar la lista de tareas antes de cargarlas
        for task in tasks:
            title, description, completed = task[1], task[2], task[3]
            task_status = "Completada" if completed else "Pendiente"
            self.task_list.add_task(title, description)
            self.task_listbox.insert(tk.END, f"{len(self.task_list.tasks)}. {title} ({task_status})")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.task_list.list_tasks()):
            status = "Completada" if task.completed else "Pendiente"
            self.task_listbox.insert(tk.END, f"{i + 1}. {task.title} ({status})")

def main():
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
