import os
import glob
from tkinter import *
from PIL import ImageTk, Image

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.images = []
        self.image_counter = 0

        # Bilder laden
        os.chdir('./images')
        for file in glob.glob("*.jpg"):
            i = Image.open(file)
            self.images.append((ImageTk.PhotoImage(resize(i, 400))))

        # Grid aufbauen
        self.image_label = Label(self.root, image=self.images[self.image_counter])
        #self.image_label = Label(self.root, text="Hier kommt später das Bild!")
        self.image_label.grid(row=0, column=0, columnspan=3)

        back_button = Button(self.root, text="<<", command=lambda:self.skip(-1))
        exit_button = Button(self.root, text="Bye", command=self.root.quit)
        next_button = Button(self.root, text=">>", command=lambda : self.skip(1))

        back_button.grid(row=1, column=0)
        exit_button.grid(row=1, column=1)
        next_button.grid(row=1, column=2)

        self.statusbar = Label(self.root, text='dummy', anchor=W, bd=1, relief=SUNKEN)
        self.statusbar.grid(row=2, column=0, columnspan=3, sticky=E+W) # beginnt in Spalte 0 und soll über drei Spalten gehen

    def skip(self, number):
        if 0 <= (self.image_counter+number) < len(self.images):
            self.image_counter += number
            self.image_label.grid_forget()
            self.image_label = Label(root, image=self.images[self.image_counter])
            self.image_label.grid(row=0, column=0, columnspan=3)

            self.statusbar.grid_forget()
            self.statusbar = Label(self.root, text=f"Image {self.image_counter + 1} of {len(self.images)}")
            self.statusbar.grid(row=2, column=0, columnspan=3, sticky=E+W)

def resize(image, x):
    w, h = image.size
    return image.resize((x, int(h*x/w)), Image.Resampling.LANCZOS)


if __name__ == '__main__':
    root = Tk()
    root.title("Image Viewer")
    root.iconbitmap("./images/thb.ico")
    root.geometry("400x350")

    iv = ImageViewer(root)

    root.mainloop()