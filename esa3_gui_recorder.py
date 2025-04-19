import tkinter as tk
from tkinter import *
from tkinter.ttk import Combobox, Treeview
import urllib.request, urllib.error, certifi, ssl, datetime as dt, sqlite3, threading, os
from tkinter import messagebox

# active recordings + progress dict
active_recordings = {}
recording_progress = {}

def record(url, filename, duration, blocksize):
    """Record audio stream from the given URL."""
    if int(duration) < 1:
        messagebox.showerror("Value Error", "Duration cannot be smaller than 1!")
    if int(blocksize) < 1:
        messagebox.showerror("Value Error", "Blocksize cannot be smaller than 1!")
    if filename is None:
        now = dt.datetime.now()
        filename = now.strftime("%Y-%m-%d-%H-%M-%S")
    if not os.path.exists("recordings"):
        os.makedirs("recordings")

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    try:
        stream = urllib.request.urlopen(url, context=ssl_context)
        stream_byterate = 128 * int(stream.headers.get('icy-br'))
        start_time = dt.datetime.now()
        blocks_target = int(duration) * stream_byterate / int(blocksize)
        blocks_written = 0
        filepath = f"recordings/{filename}.mp3"

        recording_progress[filename] = 0

        with open(filepath, 'wb') as f:
            while blocks_written < blocks_target:
                f.write(stream.read(int(blocksize)))
                blocks_written += 1
                recording_progress[filename] = (blocks_written / blocks_target) * 100
                update_status_bar()

        conn = sqlite3.connect('recordings.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS recordings
                     (identifier INTEGER PRIMARY KEY, url TEXT, filename TEXT, date TEXT, time TEXT, duration INTEGER, bitrate INTEGER)''')
        c.execute("INSERT INTO recordings (url, filename, date, time, duration, bitrate) VALUES (?, ?, ?, ?, ?, ?)",
                  (url, filename, start_time.date().isoformat(), start_time.time().strftime("%H:%M:%S"), duration, blocksize))
        conn.commit()
        conn.close()

        recording_progress.pop(filename)
        update_status_bar("Recording completed successfully.")
    except urllib.error.HTTPError:
        messagebox.showerror("HTTP Error", "A HTTP error occurred while attempting to connect to the resource. Please check the URL.")
    except TypeError:
        messagebox.showerror("Type Error", "The provided URL does not have a valid mp3 stream.")
    except ValueError:
        messagebox.showerror("Value Error", "The provided URL is not a valid web resource.")


def update_status_bar(message="Ready"):
    """Update the status bar with the progress of active recordings."""
    if active_recordings:
        progress_text = " - ".join([f"{filename}: {recording_progress.get(filename, 0):.2f}%" for filename in active_recordings])
        status_bar.config(text=f"Recording in progress: {progress_text}")
    else:
        status_bar.config(text=message)
    root.update_idletasks()

def record_in_thread(url, filename, duration, blocksize):
    """Run the record function in a separate thread."""
    if not c_dur.get():
        duration = 30
    if not c_btr.get() or not blocksize.isdigit():
        blocksize = 128

    # Clear input fields
    url_field.delete(0, "end")
    filename_field.delete(0, "end")

    active_recordings[filename] = 0
    update_status_bar()

    def threaded_record():
        try:
            record(url, filename, duration, blocksize)
            update_treeview()
        finally:
            active_recordings.pop(filename)
            update_status_bar()

    threading.Thread(target=threaded_record, daemon=True).start()

def initialize_database():
    """Create the database and recordings table if they do not exist."""
    conn = sqlite3.connect('recordings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS recordings
                 (identifier INTEGER PRIMARY KEY, url TEXT, filename TEXT, date TEXT, time TEXT, duration INTEGER, bitrate INTEGER)''')
    conn.commit()
    conn.close()

def update_treeview():
    """Update the Treeview with entries from the database."""
    for row in tree.get_children():
        tree.delete(row)
    conn = sqlite3.connect('recordings.db')
    c = conn.cursor()
    c.execute("SELECT identifier, url, filename, date, time, duration, bitrate FROM recordings")
    rows = c.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)
    conn.close()

def delete_selected_entry():
    """Delete the selected entry from the Treeview and database."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select an entry to delete.")
        return

    # Get the ID of the selected entry
    item = tree.item(selected_item)
    entry_id = item["values"][0]

    conn = sqlite3.connect('recordings.db')
    c = conn.cursor()
    c.execute("DELETE FROM recordings WHERE identifier = ?", (entry_id,))
    conn.commit()
    conn.close()

    # Delete from Treeview
    tree.delete(selected_item)
    update_status_bar("Entry deleted successfully.")

    # Delete from directory
    del_loc = messagebox.askyesno("Delete locally?", "Also delete the .mp3 file?")
    if del_loc:
        filename = item["values"][2]
        filepath = f"recordings/{filename}.mp3"
        if os.path.exists(filepath):
            os.remove(filepath)

    update_status_bar("File deleted successfully.")
    root.after(3000, lambda: update_status_bar())

def clear_all_entries():
    """Clear all entries from the Treeview and database."""
    if not tree.get_children():
        messagebox.showinfo("No Entries", "The database is already empty.")
        return None

    # Confirm action
    if not messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all entries?"):
        return None

    # Clear database
    conn = sqlite3.connect('recordings.db')
    c = conn.cursor()

    conn = sqlite3.connect('recordings.db')
    c = conn.cursor()
    c.execute("SELECT filename FROM recordings")
    filenames = [row[0] for row in c.fetchall()]

    c.execute("DELETE FROM recordings")
    conn.commit()
    conn.close()

    # Clear Treeview
    for row in tree.get_children():
        tree.delete(row)

    delall = messagebox.askyesno("Delete local files?", "Do you want to clear all .mp3 files as well?")
    if delall:
        if os.path.exists("recordings"):
            for file in filenames:
                filepath = f"recordings/{file}.mp3"
                if os.path.exists(filepath):
                    os.remove(filepath)
    update_status_bar("All entries cleared successfully.")
    root.after(3000, update_status_bar())


root = tk.Tk()
root.title("Audiorecorder")
root.iconbitmap("images/thb.ico")
root.geometry("900x600")

# Configure grid columns to expand dynamically
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(5, weight=1)

# URL field
Label(root, text="URL").grid(row=0, column=0, padx=10, pady=10, sticky="w")
url_field = Entry(root, width=80)
url_field.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Filename field
Label(root, text="Filename").grid(row=1, column=0, padx=10, pady=10, sticky="w")
filename_field = Entry(root, width=80)
filename_field.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Duration checkbox and spinbox
c_dur = BooleanVar()
Checkbutton(root, text="Duration in seconds", variable=c_dur, command=lambda : spinbox_duration.config(state="normal") if c_dur.get() else
            spinbox_duration.config(state="disabled")).grid(row=2, column=0, padx=10, pady=10, sticky="w")

spinbox_duration = Spinbox(root, from_=1, to=120, width=5, state="normal")
spinbox_duration.delete(0, "end")
spinbox_duration.insert(0, "30")
spinbox_duration.config(state="disabled")
spinbox_duration.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Bitrate checkbox and dropdown
c_btr = BooleanVar()
bitrates = ["64","128", "192", "256", "320"]
Checkbutton(root, text="Bitrate", variable=c_btr, command=lambda : dropdown_bitrate.config(state="normal" if c_btr.get()
            else dropdown_bitrate.config(state="disabled"))).grid(row=3, column=0, padx=10, pady=10, sticky="w")
dropdown_bitrate = Combobox(root, values=bitrates, state="disabled")
dropdown_bitrate.set("128")
dropdown_bitrate.grid(row=3, column=1, padx=10, pady=10, sticky="w")

start_button = Button(root, text="Start download", command=lambda: record_in_thread(url_field.get(), filename_field.get(), spinbox_duration.get(), dropdown_bitrate.get()))
start_button.grid(row=4, column=0, columnspan=2, pady=10)

delete_button = Button(root, text="Delete Selected", command=delete_selected_entry)
delete_button.grid(row=4, column=1, pady=10, padx=10, sticky="s")

clear_button = Button(root, text="Clear All", command=clear_all_entries)
clear_button.grid(row=4, column=1, pady=10, padx=10, sticky="e")


# Treeview for displaying recordings
tree = Treeview(root, columns=("id", "url", "filename", "date", "time", "duration", "bitrate"), show="headings", height=10)
tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
# Define column headers and widths
tree.heading("id", text="ID")
tree.column("id", width=15, anchor="center")
tree.heading("url", text="URL")
tree.column("url", width=300, anchor="w")
tree.heading("filename", text="Filename")
tree.column("filename", width=150, anchor="w")
tree.heading("date", text="Date")
tree.column("date", width=100, anchor="center")
tree.heading("time", text="Time")
tree.column("time", width=80, anchor="center")
tree.heading("duration", text="Duration")
tree.column("duration", width=80, anchor="center")
tree.heading("bitrate", text="Bitrate")
tree.column("bitrate", width=80, anchor="center")

initialize_database()
update_treeview()

# Add a status bar at the bottom
status_bar = Label(root, text="Ready", anchor="w", relief="sunken")
status_bar.grid(row=6, column=0, columnspan=2, sticky="nsew")

if __name__ == "__main__":
    root.mainloop()