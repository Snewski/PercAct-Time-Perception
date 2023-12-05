import tkinter as tk
from threading import Thread
import time

class Timer:
    def __init__(self, minutes=0, seconds=0, speed=1.0, update_callback=None):
        self.total_seconds = minutes * 60 + seconds
        self.current_seconds = self.total_seconds
        self.is_running = False
        self.is_paused = False
        self.speed = speed
        self.update_callback = update_callback

    def start(self):
        self.is_running = True
        self._run_timer()

    def stop(self):
        self.is_running = False

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False
        if not self.is_running:
            self.start()

    def _run_timer(self):
        while self.is_running and self.current_seconds > 0:
            if not self.is_paused:
                self.current_seconds -= 1
                time.sleep(1 / self.speed)
                if self.update_callback:
                    self.update_callback(self._format_time())

        self.is_running = False
        print("Timer completed!")

    def _format_time(self):
        minutes, seconds = divmod(self.current_seconds, 60)
        return f"Time Left: {minutes:02d}:{seconds:02d}"

def start_timer(speed):
    new_window = tk.Toplevel(root)
    new_window.title(f"Timer {speed}x")
    
    # Make the window fullscreen
    new_window.attributes('-fullscreen', True)

    timer_label = tk.Label(new_window, text=f"Time Left: 10:00", font=("Helvetica", 16))
    timer_label.pack(pady=20)
    timer_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    def update_timer_label(new_time):
        timer_label.config(text=new_time)

    timer = Timer(minutes=10, speed=speed, update_callback=update_timer_label)
    timer_thread = Thread(target=timer.start)
    timer_thread.start()

    # Pause button
    pause_button = tk.Button(new_window, text="Pause", command=timer.pause)
    pause_button.pack(side=tk.LEFT, padx=10)
    pause_button.place(relx=0.45, rely=0.5, anchor=tk.CENTER)

    # Resume button
    resume_button = tk.Button(new_window, text="Resume", command=timer.resume)
    resume_button.pack(side=tk.LEFT, padx=10)
    resume_button.place(relx=0.55, rely=0.5, anchor=tk.CENTER)

    # Bind the "Escape" key to close the window
    new_window.bind('<Escape>', lambda event: close_timer_window(new_window, timer))

def close_timer_window(window, timer):
    # Stop the timer before destroying the window
    timer.stop()
    window.destroy()

def close_window(event):
    root.destroy()

# GUI setup
root = tk.Tk()
root.title("Timer App")

# Make the main window fullscreen
root.attributes('-fullscreen', True)

# Add initial text to the main window
initial_text = tk.Label(root, text="Please choose one of these options", font=("Helvetica", 16))
initial_text.pack(pady=5)
initial_text.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

button_frame = tk.Frame(root)
button_frame.pack(expand=True)

# Make the buttons slightly bigger
button_1 = tk.Button(button_frame, text="1", command=lambda: start_timer(1/1.1), height=2, width=5)
button_1.pack(side=tk.LEFT, padx=10)

button_2 = tk.Button(button_frame, text="2", command=lambda: start_timer(1.0), height=2, width=5)
button_2.pack(side=tk.LEFT, padx=10)

button_3 = tk.Button(button_frame, text="3", command=lambda: start_timer(1/0.9), height=2, width=5)
button_3.pack(side=tk.LEFT, padx=10)

# Center the buttons in the frame
button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Bind the "Escape" key to close the window
root.bind('<Escape>', close_window)

root.mainloop()