from tkinter import *
import time
import threading
import tkinter as tk
import os
import urllib.request, urllib.error, certifi, ssl, datetime as dt, sqlite3

root = Tk()
root.title("Audiorecorder")
root.iconbitmap("../images/thb.ico")
root.geometry("400x350")

url_var = StringVar()
url_frame = Frame(root)
url_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

Label(url_frame, text="URL").grid(row=0, column=0, padx=5, pady=5, sticky="w")
url_field = Entry(url_frame, textvariable=url_var)
url_field.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

c_btr = BooleanVar()
check_bitrate = Checkbutton(url_frame, variable=c_btr)
check_bitrate.grid(row=1, column=0, padx=5, pady=5, sticky="w")
Label(url_frame, text="bitrate").grid(row=1, column=1, padx=5, pady=5, sticky="w")

c_time = BooleanVar()

url_frame.columnconfigure(1, weight=1)

if __name__ == "__main__":
    root.mainloop()
