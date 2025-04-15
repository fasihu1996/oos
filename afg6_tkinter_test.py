from tkinter import *

def client_exit():
    print("Exit button pressed")
    root.destroy()

def make_red():
    w.config(fg="red")
    b.config(fg="red")

root = Tk()

text = """
Ich
bin
ein
mehrzeiliger
Text"""

w = Label(root, text=text, fg="blue", bg="yellow", justify=LEFT)
w.pack()
b = Button(root, text="Exit", command=client_exit)
b.pack()
b2 = Button(root, text="Rot", command=make_red)
b2.pack()

if __name__ == '__main__':
    root.mainloop()