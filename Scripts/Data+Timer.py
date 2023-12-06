# Data

# Importing modules
from psychopy import visual, event, core, sound, gui, data
import pandas as pd, random, os, string
import tkinter as tk
import time
from threading import Thread

## Logfile ##
# Making sure there is a logfile directory
if not os.path.exists("logfiles"):
    os.makedirs("logfiles")
# Setting up logfile
columns = ["ID", "Condition","Age", "Gender", "Vid_1", "Button_Estimate_1", "Written_Estimate_1", "Vid_2", "Button_Estimate_2", "Written_Estimate_2"]
logfile = pd.DataFrame(columns = columns)

## GUI ##
# Creating dialogue box
DialogueBox = gui.Dlg(title = "Time experiment")
DialogueBox.addText('Please fill in the following fields:')
# Adding information fields
DialogueBox.addField('Condition:', color = "purple")
DialogueBox.addField('Participant ID:', color = "blue")
DialogueBox.addField('Age:', color = "green")
DialogueBox.addField('Gender:', choices = ["female", "male", "other"], color = "red")
# Showing dialogue box
DialogueBox.show()

# Collecting participant information
if DialogueBox.OK:
    Condition = DialogueBox.data[0]
    ID = DialogueBox.data[1]
    Age = DialogueBox.data[2]
    Gender = DialogueBox.data[3]
elif DialogueBox.Cancel:
    core.quit()

## Text chuncks ##
task_txt1 = '''Press down this button for as long as you felt the stimuli lasted'''
task_txt2 = '''Please write down how long you think the stimuli lasted (in seconds)'''
intro1= '''Hello! And welcome to this experiment! \n (press space to continue)'''
intro2 = '''In this experiment you will be presented with some stimuli, and it will be your task to estimate how long the stimuli lasted. \n (press space to continue)'''
end = "Thanks for participating"

## Experiment presentation ##
#Window
win = visual.Window(fullscr = True)
# Presenting introduction
instruction = visual.TextStim(win,text = intro1, color="black")
instruction.draw()
win.flip()
event.waitKeys()

instruction2 = visual.TextStim(win,text = intro2, color="black")
instruction2.draw()
win.flip()
event.waitKeys()

# Video presentation
video_path = 'Noice.mp4'
video_stim = visual.MovieStim3(win, video_path, size=(1920, 1080), flipVert=False, flipHoriz=False)
video_stim.play()

while video_stim.status != visual.FINISHED:
    video_stim.draw()
    win.flip()

video_stim.stop()

# Button press measurement
# Create a rectangle as the button
button_size = (0.2, 0.1)  # Set the size of the button (width, height)
button = visual.Rect(win, width=button_size[0], height=button_size[1], fillColor='white')
# instructions
button_instruction = visual.TextStim(win, text=task_txt1, color="black")
# positions
button.pos = (0, 0)
# Set the position of the text above the button
text_offset = 0.20  # Adjust this value to control the vertical distance
button_instruction.pos = (0, button.pos[1] + button.size[1]/2 + text_offset)

# Create a Mouse object
mouse = event.Mouse()

# Initialize variables
button_pressed = False
click_start_time = None

# Main experiment loop
while True:
    # Draw the button
    button_instruction.draw()
    button.draw()

    # Check if the mouse button is pressed over the button
    if mouse.isPressedIn(button) and not button_pressed:
        click_start_time = core.getTime()
        button_pressed = True

    # Check if the mouse button is released
    if mouse.getPressed()[0] == 0 and button_pressed:
        click_end_time = core.getTime()
        click_duration = click_end_time - click_start_time
        break

    # Check for the 'escape' key to end the experiment
    if 'escape' in event.getKeys():
        break

    # Flip the window to update the display
    win.flip()

# Close the window after button press measurement
win.close()

# Creating dialogue box
TimeBox1 = gui.Dlg(title = "Time estimate")
TimeBox1.addText('Please fill in your estimate of the duration:')
# Adding information fields
TimeBox1.addField('Time Estimate:', color = "blue")
# Showing dialogue box
TimeBox1.show()

# Collecting participant information
if TimeBox1.OK:
    Written_1 = TimeBox1.data[0]
elif TimeBox1.Cancel:
    core.quit()

## Timer part ##
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

    timer_label = tk.Label(new_window, text=f"Time Left: 1:00", font=("Helvetica", 16))
    timer_label.pack(pady=20)
    timer_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    def update_timer_label(new_time):
        timer_label.config(text=new_time)
        if new_time == "Time Left: 00:00":
            # Timer has completed, close the window
            close_timer_window(new_window, timer)

    timer = Timer(minutes=1, speed=speed, update_callback=update_timer_label)
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
    # Check if the timer has completed before destroying the window
    if not timer.is_running:
        window.destroy()

    # If the main window is still present, destroy it
    if root.winfo_exists():
        root.destroy()

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

button_3 = tk.Button(button_frame, text="3", command=lambda: start_timer(10), height=2, width=5)
button_3.pack(side=tk.LEFT, padx=10)

# Center the buttons in the frame
button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Bind the "Escape" key to close the window
root.bind('<Escape>', close_window)

root.mainloop()

## Second Stimuli ##
win = visual.Window(fullscr = True)
# Presenting introduction
instruction = visual.TextStim(win,text = intro1, color="black")
instruction.draw()
win.flip()
event.waitKeys()

instruction2 = visual.TextStim(win,text = intro2, color="black")
instruction2.draw()
win.flip()
event.waitKeys()

# Video presentation
video_path = 'Noice.mp4'
video_stim = visual.MovieStim3(win, video_path, size=(1920, 1080), flipVert=False, flipHoriz=False)
video_stim.play()

while video_stim.status != visual.FINISHED:
    video_stim.draw()
    win.flip()

video_stim.stop()

# Button press measurement
# Create a rectangle as the button
button_size = (0.2, 0.1)  # Set the size of the button (width, height)
button = visual.Rect(win, width=button_size[0], height=button_size[1], fillColor='white')
# instructions
button_instruction = visual.TextStim(win, text=task_txt1, color="black")
# positions
button.pos = (0, 0)
# Set the position of the text above the button
text_offset = 0.20  # Adjust this value to control the vertical distance
button_instruction.pos = (0, button.pos[1] + button.size[1]/2 + text_offset)

# Create a Mouse object
mouse = event.Mouse()

# Initialize variables
button_pressed = False
click_start_time = None

# Main experiment loop
while True:
    # Draw the button
    button_instruction.draw()
    button.draw()

    # Check if the mouse button is pressed over the button
    if mouse.isPressedIn(button) and not button_pressed:
        click_start_time = core.getTime()
        button_pressed = True

    # Check if the mouse button is released
    if mouse.getPressed()[0] == 0 and button_pressed:
        click_end_time = core.getTime()
        click_duration2 = click_end_time - click_start_time
        break

    # Check for the 'escape' key to end the experiment
    if 'escape' in event.getKeys():
        break

    # Flip the window to update the display
    win.flip()

# Close the window after button press measurement
win.close()

# Creating dialogue box
TimeBox1 = gui.Dlg(title = "Time estimate")
TimeBox1.addText('Please fill in your estimate of the duration:')
# Adding information fields
TimeBox1.addField('Time Estimate:', color = "blue")
# Showing dialogue box
TimeBox1.show()

# Collecting participant information
if TimeBox1.OK:
    Written_2 = TimeBox1.data[0]
elif TimeBox1.Cancel:
    core.quit()


# Appending data to the logfile
logfile = logfile.append({
    "ID": ID,
    "Condition": Condition,
    "Age": Age,
    "Gender": Gender,
    "Vid_1": video_path,
    "Button_Estimate_1": click_duration,
    "Written_Estimate_1": Written_1,
    "Vid_2": video_path,
    "Button_Estimate_2": click_duration2,
    "Written_Estimate_2": Written_2,
}, ignore_index=True)

# Save logfile
logfile_name = f"logfiles/logfile_{ID}_{Age}_{Gender}.csv"
logfile.to_csv(logfile_name)

