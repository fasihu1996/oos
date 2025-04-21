import tkinter as tk
import time


class Stopwatch:
    def __init__(self, root):
        self.root = root
        self.root.title("Stoppuhr mit Rundenzeiten")
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.lap_times = []

        # Zeitlabel
        self.time_label = tk.Label(root, text="00:00:00", font=("Helvetica", 40))
        self.time_label.pack(pady=10)

        # Buttons
        self.start_stop_button = tk.Button(root, text="Start", font=("Helvetica", 12), width=10,
                                           command=self.start_stop)
        self.start_stop_button.pack(side="left", padx=5, pady=5)

        self.reset_button = tk.Button(root, text="Reset", font=("Helvetica", 12), width=10, command=self.reset, )
        self.reset_button.pack(side="left", padx=5, pady=5)

        # Hier soll der Button für die Laptimes (Rundenzeiten) hinzugefügt werden

        # Hier soll die Listbox für die Laptimes (Rundenzeiten) hinzugefügt werden

        # Stoppuhr-Aktualisierung starten
        self.update_clock()

    def update_clock(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
        elapsed_time_str = self.format_time(self.elapsed_time)
        self.time_label.config(text=elapsed_time_str)
        self.root.after(100, self.update_clock)

    def format_time(self, elapsed):
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        milliseconds = int((elapsed - int(elapsed)) * 100)
        return f"{minutes:02}:{seconds:02}:{milliseconds:02}"

    def start_stop(self):
        if not self.running:
            # Starten der Stoppuhr
            self.start_time = time.time() - self.elapsed_time
            self.running = True
            self.start_stop_button.config(text="Stopp")  # Ändere den Button zu "Stopp"
        else:
            # Stoppen der Stoppuhr
            self.running = False
            self.start_stop_button.config(text="Start")  # Ändere den Button zu "Start"

    def reset(self):
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.lap_times = []
        self.time_label.config(text="00:00:00")

    def record_lap(self):
        pass


# Hauptfenster erstellen
root = tk.Tk()
app = Stopwatch(root)
root.mainloop()
