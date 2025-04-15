from tkinter import *

def print_all():
    print(i_v.get())
    i_v.set(42)
    pass

def e_listener(*args):
    print(args)
    print("var geändert")
root = Tk()
root.title("Input Fields")
root.iconbitmap("./images/thb.ico")
root.geometry("400x350")


i_v = IntVar()
i_v.trace("w", e_listener)
s = Scale(root, from_=10, to=100, variable=i_v)
s.pack()

b = Button(root, text="Lies alles", command=print_all)
b.pack()

if __name__ == "__main__":
    root.mainloop()