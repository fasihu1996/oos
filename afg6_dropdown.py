from tkinter import *

def print_all():
    print(f"Auswahl: {s_d.get()}")
    pass

root = Tk()
root.title("Radio buttons")
root.iconbitmap("./images/thb.ico")
root.geometry("400x350")

s_d = StringVar()

d = OptionMenu(root, s_d, "Menü 1", "Menü 2", "Menü 3")
d.pack()


b = Button(root, text="Lies alles", command=print_all)
b.pack()

if __name__ == "__main__":
    root.mainloop()