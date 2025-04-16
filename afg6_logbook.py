import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import sqlite3
from datetime import datetime


class Logbook:
    def __init__(self, root):
        self.root = root
        self.root.title("Logbuch mit Tkinter")
        self.conn = sqlite3.connect('logbook.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS logs(identifier INTEGER PRIMARY KEY, author TEXT,
        entry TEXT, date TEXT, time TEXT)''')
        self.conn.commit()

        self.style = Style()
        self.style.configure("BW.TLabel", foreground="black", background="white")

        self.table = Treeview(self.root, columns=("ID", "Author", "Entry", "Date", "Time"))
        self.table.pack(expand=YES, fill=BOTH)
        self.table.column("#0", width=1, minwidth=1)
        self.table.heading("#0", text="")
        self.table.column("ID", width=50, minwidth=50)
        self.table.heading("ID", text="ID")
        self.table.column("Author", width=100, minwidth=100)
        self.table.heading("Author", text="Author")
        self.table.column("Entry", width=400, minwidth=400)
        self.table.heading("Entry", text="Entry")
        self.table.column("Date", width=100, minwidth=100)
        self.table.heading("Date", text="Date")
        self.table.column("Time", width=100, minwidth=100)
        self.table.heading("Time", text="Timestamp")
        self.curr_idx = 0


        self.new_button = Button(self.root, text="Create new entry", command=self.new_entry)
        self.new_button.pack(side=RIGHT)

        self.load_entries()

    def new_entry(self):
        entry_window = tk.Toplevel(self.root)
        entry_window.geometry("400x300")
        entry_window.title("New Entry")

        author_frame = Frame(entry_window)
        author_frame.pack(pady=10, fill=X)
        Label(author_frame, text="Author:", width=10, anchor=W).pack(side=LEFT, padx=5)
        author_entry = Entry(author_frame, width=40)
        author_entry.pack(side=LEFT, padx=5)

        Label(entry_window, text="Entry:").pack(anchor=W, padx=5)
        entry_text = Text(entry_window, width=50, height=10)
        entry_text.pack(pady=5, padx=5)

        Button(entry_window, text="Save entry", command=lambda: self.create_entry(entry_window, author_entry.get(), entry_text.get("1.0", "end-1c"))).pack(pady=10)

    def create_entry(self, entry_window, author, entry):
        now = datetime.now()
        cur_date= now.strftime("%d/%m/%Y")
        cur_time = now.strftime("%H:%M:%S")
        self.table.insert("", "end", values=(self.curr_idx + 1, author, entry, cur_date, cur_time))
        self.c.execute("INSERT INTO logs (author, entry, date, time) VALUES (?, ?, ?, ?)", (author, entry, cur_date, cur_time))
        self.conn.commit()
        self.curr_idx += 1
        entry_window.destroy()
        return messagebox.showinfo(title="Entry saved", message="Your entry has been successfully saved")

    def load_entries(self):
        self.c.execute("SELECT identifier, author, entry FROM logs")
        rows = self.c.fetchall()
        for row in rows:
            self.table.insert("", "end", values=row)
            self.curr_idx = max(self.curr_idx, row[0])



if __name__ == "__main__":
    root = tk.Tk()
    app = Logbook(root)
    root.mainloop()