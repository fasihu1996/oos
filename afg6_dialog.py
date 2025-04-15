from tkinter import *
from tkinter import messagebox, simpledialog

def print_all():
    pass

root = Tk()
root.title("Radio buttons")
root.iconbitmap("./images/thb.ico")
root.geometry("400x350")

print(simpledialog.askinteger(title="Voltage", prompt="Please input a number"))

info = messagebox.showinfo(title="Show info", message="Alles gut!")
print(info)
warning = messagebox.showwarning(title="Show warning", message="Eine Warnung!")
print(warning)
err = messagebox.showerror(title="Show error", message="Ein Fehler")
print(err)

ask = messagebox.askyesno(title="Ja/Nein", message="Ist alles guti?")
print(ask)

b = Button(root, text="Lies alles", command=print_all)
b.pack()

if __name__ == "__main__":
    root.mainloop()