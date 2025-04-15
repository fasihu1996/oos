from tkinter import *

def print_all():
    print(f"Radio: {i_r.get()}")
    print(f"Knoblauch: {b_c.get()}")
    pass

root = Tk()
root.title("Radio buttons")
root.iconbitmap("./images/thb.ico")
root.geometry("400x350")

i_r = IntVar()

r_buttons = []
for t, v in (("Montag", 1), ("Dienstag", 2), ("Mittwoch", 3)):
    r = Radiobutton(root, text=t, value=v, variable=i_r)
    r.pack()

b_c = BooleanVar()
c = Checkbutton(root, text="Mit Knoblauch", variable=b_c)
c.pack()


b = Button(root, text="Lies alles", command=print_all)
b.pack()

if __name__ == "__main__":
    root.mainloop()