from tkinter import *

root = Tk()
root.title("Radio buttons")
root.iconbitmap("./images/thb.ico")
root.geometry("400x350")

new_window = Toplevel(root)
l = Label(new_window, text="Ich bin das neue Fenster")
l.pack()

if __name__ == "__main__":
    root.mainloop()