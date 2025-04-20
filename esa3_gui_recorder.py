import tkinter as tk
from tkinter import *
from tkinter import ttk
import urllib.request, urllib.error, certifi, ssl, datetime as dt, sqlite3, threading, os, sv_ttk
from tkinter import messagebox

# active recordings + progress dict
recordings = {}

def record(url, filename, duration, bitrate):
    """Record audio stream from the given URL."""
    if int(duration) < 1:
        messagebox.showerror("Value Error", "Duration cannot be smaller than 1!")
    if int(bitrate) < 1:
        messagebox.showerror("Value Error", "Bitrate cannot be smaller than 1!")
    if filename is None or filename.strip() == "":
        now = dt.datetime.now()
        filename = now.strftime("%Y-%m-%d-%H-%M-%S")
    if not os.path.exists("recordings"):
        os.makedirs("recordings")

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    try:
        stream = urllib.request.urlopen(url, context=ssl_context)
        stream_byterate = int(bitrate) * 1024 // 8  # Convert kbps to bytes per second
        start_time = dt.datetime.now()
        blocks_target = int(duration) * stream_byterate
        blocks_written = 0
        filepath = f"recordings/{filename}.mp3"

        recordings[filename] = 0

        with open(filepath, 'wb') as f:
            while blocks_written < blocks_target:
                f.write(stream.read(1024))  # Read in chunks of 1024 bytes
                blocks_written += 1024
                recordings[filename] = (blocks_written / blocks_target) * 100
                update_status_bar()

        conn = sqlite3.connect('recordings.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS recordings
                     (identifier INTEGER PRIMARY KEY, url TEXT, filename TEXT, date TEXT, time TEXT, duration INTEGER, bitrate INTEGER)''')
        c.execute("INSERT INTO recordings (url, filename, date, time, duration, bitrate) VALUES (?, ?, ?, ?, ?, ?)",
                  (url, filename, start_time.date().isoformat(), start_time.time().strftime("%H:%M:%S"), duration, bitrate))
        conn.commit()
        conn.close()

        recordings.pop(filename)
        update_status_bar("Recording completed successfully.")
    except urllib.error.HTTPError as e:
        messagebox.showerror("HTTP Error", "A HTTP error occurred while attempting to connect to the resource. Please check the URL.")
        print(e)
    except TypeError as e:
        messagebox.showerror("Type Error", "The provided URL does not have a valid mp3 stream.")
        print(e)
    except ValueError as e:
        messagebox.showerror("Value Error", "The provided URL is not a valid web resource.")
        print(e)

def update_status_bar(message="Ready"):
    """Update the status bar with the progress of active recordings."""
    if recordings:
        progress_text = " - ".join([f"{filename}: {progress:.2f}%" for filename, progress in recordings.items()])
        status_bar.config(text=f"Recording in progress: {progress_text}")
    else:
        status_bar.config(text=message)
    root.update_idletasks()

def record_in_thread(url, filename, duration, bitrate):
    """Run the record function in a separate thread."""
    if not c_dur.get():
        duration = 30
    if not c_btr.get() or not bitrate.isdigit():
        bitrate = 128

    # Clear input fields
    url_field.delete(0, "end")
    filename_field.delete(0, "end")

    recordings[filename] = 0
    update_status_bar()

    def threaded_record():
        try:
            record(url, filename, duration, bitrate)
            update_treeview()
        finally:
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
        else:
            update_status_bar("File not found locally.")

    # Avoid overwriting the status message
    root.after(3000, lambda: update_status_bar("Ready"))

def clear_all_entries():
    """Clear all entries from the Treeview and database."""
    if not tree.get_children():
        messagebox.showinfo("No Entries", "The database is already empty.")
        return

    # Confirm action
    if not messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all entries?"):
        return

    # Clear database
    conn = sqlite3.connect('recordings.db')
    c = conn.cursor()
    c.execute("SELECT filename FROM recordings")
    filenames = [row[0] for row in c.fetchall()]

    c.execute("DELETE FROM recordings")
    conn.commit()
    conn.close()
    update_status_bar("All entries cleared successfully.")

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

    update_status_bar("Local audio files deleted")

def toggle_theme():
    global is_light_mode
    if is_light_mode:
        sv_ttk.set_theme("dark")
        theme_button.config(image=light_mode_icon)
    else:
        sv_ttk.set_theme("light")
        theme_button.config(image=dark_mode_icon)
    is_light_mode = not is_light_mode

root = tk.Tk()
root.title("Audiorecorder")
root.iconbitmap("images/thb.ico")
root.geometry("900x600")
sv_ttk.set_theme("dark")

# Configure grid columns to expand dynamically
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(5, weight=1)

# URL field
ttk.Label(root, text="URL").grid(row=0, column=0, padx=10, pady=10, sticky="w")
url_field = ttk.Entry(root, width=80)
url_field.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Filename field
ttk.Label(root, text="Filename").grid(row=1, column=0, padx=10, pady=10, sticky="w")
filename_field = ttk.Entry(root, width=80)
filename_field.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Duration checkbox and spinbox
c_dur = BooleanVar()
ttk.Checkbutton(root, text="Duration in seconds", variable=c_dur, command=lambda : spinbox_duration.config(state="normal") if c_dur.get() else
            spinbox_duration.config(state="disabled")).grid(row=2, column=0, padx=10, pady=10, sticky="w")

spinbox_duration = ttk.Spinbox(root, from_=1, to=120, width=5, state="normal")
spinbox_duration.delete(0, "end")
spinbox_duration.insert(0, "30")
spinbox_duration.config(state="disabled")
spinbox_duration.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Bitrate checkbox and dropdown
c_btr = BooleanVar()
bitrates = ["64","128", "192", "256", "320"]
ttk.Checkbutton(root, text="Bitrate", variable=c_btr, command=lambda : dropdown_bitrate.config(state="normal" if c_btr.get()
            else dropdown_bitrate.config(state="disabled"))).grid(row=3, column=0, padx=10, pady=10, sticky="w")
dropdown_bitrate = ttk.Combobox(root, values=bitrates, state="disabled")
dropdown_bitrate.set("128")
dropdown_bitrate.grid(row=3, column=1, padx=10, pady=10, sticky="w")

start_button = ttk.Button(root, text="Start download", command=lambda: record_in_thread(url_field.get(), filename_field.get(), spinbox_duration.get(), dropdown_bitrate.get()))
start_button.grid(row=4, column=0, columnspan=2, pady=10)

delete_button = ttk.Button(root, text="Delete Selected", command=delete_selected_entry)
delete_button.grid(row=4, column=0, pady=10, padx=(10,5), sticky="e")

clear_button = ttk.Button(root, text="Clear All", command=clear_all_entries)
clear_button.grid(row=4, column=1, pady=10, padx=(5,10), sticky="w")


# Treeview for displaying recordings
tree = ttk.Treeview(root, columns=("id", "url", "filename", "date", "time", "duration", "bitrate"), show="headings", height=10)
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
status_bar = ttk.Label(root, text="Ready", anchor="w", relief="sunken", padding=(5,0))
status_bar.grid(row=6, column=0, columnspan=2, sticky="nsew")

light_mode_icon = tk.PhotoImage(file="images/light.png")
dark_mode_icon = tk.PhotoImage(file="images/dark.png")
is_light_mode = sv_ttk.get_theme() == "light"
theme_button = ttk.Button(root, image=dark_mode_icon if is_light_mode else light_mode_icon, command=toggle_theme)
theme_button.grid(row=6, column=1, sticky="e", ipadx=1, ipady=1)

if __name__ == "__main__":
    root.mainloop()