### Time Perception Experiment ###

## Importing modules ##
from psychopy import visual, event, core, sound, gui, data, clock
import pandas as pd, random, os, string
import tkinter as tk
import time
from threading import Thread

## Logfile ##
# Making sure there is a logfile directory
if not os.path.exists("logfiles"):
    os.makedirs("logfiles")
# Setting up logfile
columns = ["ID", "Condition","Age", "Gender", 
"Beep_Time1", "Button_Estimate_1", "Written_Estimate_1", 
"Beep_Time2", "Button_Estimate_2", "Written_Estimate_2",
"Beep_Time3", "Button_Estimate_3", "Written_Estimate_3",
"Beep_Time4", "Button_Estimate_4", "Written_Estimate_4",
"Beep_Time5", "Button_Estimate_5", "Written_Estimate_5",
"Beep_Time6", "Button_Estimate_6", "Written_Estimate_6",
"Beep_Time7", "Button_Estimate_7", "Written_Estimate_7",
"Beep_Time8", "Button_Estimate_8", "Written_Estimate_8",
"Beep_Time9", "Button_Estimate_9", "Written_Estimate_9",
"Beep_Time10", "Button_Estimate_10", "Written_Estimate_10",
"Beep_Time11", "Button_Estimate_11", "Written_Estimate_11",
"Beep_Time12", "Button_Estimate_12", "Written_Estimate_12",]
logfile = pd.DataFrame(columns = columns)

## Text chuncks ##
consent ='''You're about to participate in an experiment exploring time perception and it's affect on actions. \n
This experiment consists of multiple tasks. 
Explicit instructions for each task will be written  on the screen before every task. \n
Participating in this experiment presents no related harm nor benefit.  \n
You may contact one of the authors if you wish for your data to be deleted no later than: 21/12/23 \n
Press SPACE to give consent.'''
trial = '''You will be asked to estimate the duration of a tone being played to you. \n
The tone will be played, afterwards you will have to press and hold a button for as long as the tone played, and afterwards type the estimated duration. \n
Here is a single trial, so you know what to do moving forward. \n
Press SPACE to start the trial.'''
start = '''Great job, now you will be played a series of tones and will be asked to estimate their duration after each of them. \n
Press SPACE to start the experiment.'''
task_txt1 = '''Press down this button with the left mouse button for as long as you felt the stimuli lasted'''
task_txt2 = '''Please write down how long you think the stimuli lasted (in seconds)'''
Lego = '''Now your task will consists of recreating Lego structures that will be presented on a secondary screen with limited time. \n
Please wait before proceeding for further instructions from the experimenter.'''
Start2 = '''Now you will perform analogous task to the first one. \n
You will be asked to estimate the duration of a tone being played to you. 
The tone will be played, afterwards you will have to press and hold a button for as long as the tone played, and afterwards type the estimated duration. \n
This time there is no trial. \n
Press SPACE to continue'''
end = '''This part of the experiment is over, now you will be asked by the experimenter to answer a few questions. \n
Press SPACE to end the experiment'''

## Presenting introduction/consent ##
win = visual.Window(fullscr = True)
instruction = visual.TextStim(win,text = consent, color="black", height=0.08)
instruction.draw()
win.flip()
event.waitKeys()
# Close the window
win.close()

## GUI ##
# Creating dialogue box
DialogueBox = gui.Dlg(title = "Time experiment")
DialogueBox.addText('Please fill in the following fields:')
# Adding information fields
DialogueBox.addField('Condition:', choices = [1, 2, 3], color = "purple")
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


## Trial ##
win = visual.Window(fullscr = True)
instruction2 = visual.TextStim(win,text = trial, color="black")
instruction2.draw()
win.flip()
event.waitKeys()
win.flip(clearBuffer=True)

# Audio
beep = sound.Sound(
    value = 'A', secs = 2,
    volume = 1.0)
beep.play()
core.wait(3.0)
win.flip()

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

# Main Button loop
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

    # Check for the 'escape' key to end
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

# "Collecting" participant information
if TimeBox1.OK:
    Written = TimeBox1.data[0]
elif TimeBox1.Cancel:
    core.quit()

## Experiment presentation ##
win = visual.Window(fullscr = True)
instruction2 = visual.TextStim(win,text = start, color="black")
instruction2.draw()
win.flip()
event.waitKeys()
win.flip(clearBuffer=True)

## Audio 1 ##
beep = sound.Sound(
    value = 'A', secs = 5,
    volume = 1.0)
beep_time1 = 5
beep.play()
core.wait(6.0)
win.flip()

# Button press measurement 1
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

# Main Button loop
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
        click_duration1 = click_end_time - click_start_time
        break

    # Check for the 'escape' key to end
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

## Audio 2 ##
win = visual.Window(fullscr = True)
beep = sound.Sound(
    value = 'A', secs = 3,
    volume = 1.0)
beep_time2 = 3
beep.play() 
core.wait(4.0)
win.flip()

# Button
button_size = (0.2, 0.1)
button = visual.Rect(win, width=button_size[0], height=button_size[1], fillColor='white')
button_instruction = visual.TextStim(win, text=task_txt1, color="black")
button.pos = (0, 0)
text_offset = 0.20
button_instruction.pos = (0, button.pos[1] + button.size[1]/2 + text_offset)

mouse = event.Mouse()
button_pressed = False
click_start_time = None
# Main loop
while True:
    button_instruction.draw()
    button.draw()

    if mouse.isPressedIn(button) and not button_pressed:
        click_start_time = core.getTime()
        button_pressed = True

    if mouse.getPressed()[0] == 0 and button_pressed:
        click_end_time = core.getTime()
        click_duration2 = click_end_time - click_start_time
        break

    if 'escape' in event.getKeys():
        break

    win.flip()

win.close()

TimeBox1 = gui.Dlg(title = "Time estimate")
TimeBox1.addText('Please fill in your estimate of the duration:')
TimeBox1.addField('Time Estimate:', color = "blue")
TimeBox1.show()

if TimeBox1.OK:
    Written_2 = TimeBox1.data[0]
elif TimeBox1.Cancel:
    core.quit()

## Audio 3 ##
win = visual.Window(fullscr = True)
beep = sound.Sound(
    value = 'A', secs = 9,
    volume = 1.0)
beep_time3 = 9
beep.play() 
core.wait(10.0)
win.flip()

# Button
button_size = (0.2, 0.1)
button = visual.Rect(win, width=button_size[0], height=button_size[1], fillColor='white')
button_instruction = visual.TextStim(win, text=task_txt1, color="black")
button.pos = (0, 0)
text_offset = 0.20
button_instruction.pos = (0, button.pos[1] + button.size[1]/2 + text_offset)

mouse = event.Mouse()
button_pressed = False
click_start_time = None
# Main loop
while True:
    button_instruction.draw()
    button.draw()

    if mouse.isPressedIn(button) and not button_pressed:
        click_start_time = core.getTime()
        button_pressed = True

    if mouse.getPressed()[0] == 0 and button_pressed:
        click_end_time = core.getTime()
        click_duration3 = click_end_time - click_start_time
        break

    if 'escape' in event.getKeys():
        break

    win.flip()

win.close()

TimeBox1 = gui.Dlg(title = "Time estimate")
TimeBox1.addText('Please fill in your estimate of the duration:')
TimeBox1.addField('Time Estimate:', color = "blue")
TimeBox1.show()

if TimeBox1.OK:
    Written_3 = TimeBox1.data[0]
elif TimeBox1.Cancel:
    core.quit()

## Audio 4 ##
win = visual.Window(fullscr = True)
beep = sound.Sound(
    value = 'A', secs = 4,
    volume = 1.0)
beep_time4 = 4
beep.play()
core.wait(5.0)
win.flip()

# Button
button_size = (0.2, 0.1)
button = visual.Rect(win, width=button_size[0], height=button_size[1], fillColor='white')
button_instruction = visual.TextStim(win, text=task_txt1, color="black")
button.pos = (0, 0)
text_offset = 0.20
button_instruction.pos = (0, button.pos[1] + button.size[1]/2 + text_offset)

mouse = event.Mouse()
button_pressed = False
click_start_time = None
# Main loop
while True:
    button_instruction.draw()
    button.draw()

    if mouse.isPressedIn(button) and not button_pressed:
        click_start_time = core.getTime()
        button_pressed = True

    if mouse.getPressed()[0] == 0 and button_pressed:
        click_end_time = core.getTime()
        click_duration4 = click_end_time - click_start_time
        break

    if 'escape' in event.getKeys():
        break

    win.flip()

win.close()

TimeBox1 = gui.Dlg(title = "Time estimate")
TimeBox1.addText('Please fill in your estimate of the duration:')
TimeBox1.addField('Time Estimate:', color = "blue")
TimeBox1.show()

if TimeBox1.OK:
    Written_4 = TimeBox1.data[0]
elif TimeBox1.Cancel:
    core.quit()

## Audio 5 ##
win = visual.Window(fullscr = True)
beep = sound.Sound(
    value = 'A', secs = 2,
    volume = 1.0)
beep_time5 = 2
beep.play() 
core.wait(3.0)
win.flip()

# Button
button_size = (0.2, 0.1)
button = visual.Rect(win, width=button_size[0], height=button_size[1], fillColor='white')
button_instruction = visual.TextStim(win, text=task_txt1, color="black")
button.pos = (0, 0)
text_offset = 0.20
button_instruction.pos = (0, button.pos[1] + button.size[1]/2 + text_offset)

mouse = event.Mouse()
button_pressed = False
click_start_time = None
# Main loop
while True:
    button_instruction.draw()
    button.draw()

    if mouse.isPressedIn(button) and not button_pressed:
        click_start_time = core.getTime()
        button_pressed = True

    if mouse.getPressed()[0] == 0 and button_pressed:
        click_end_time = core.getTime()
        click_duration5 = click_end_time - click_start_time
        break

    if 'escape' in event.getKeys():
        break

    win.flip()

win.close()

TimeBox1 = gui.Dlg(title = "Time estimate")
TimeBox1.addText('Please fill in your estimate of the duration:')
TimeBox1.addField('Time Estimate:', color = "blue")
TimeBox1.show()

if TimeBox1.OK:
    Written_5 = TimeBox1.data[0]
elif TimeBox1.Cancel:
    core.quit()

## Audio 6 ##
win = visual.Window(fullscr = True)
beep = sound.Sound(
    value = 'A', secs = 7,
    volume = 1.0)
beep_time6 = 7
beep.play() 
core.wait(8.0)
win.flip()

# Button
button_size = (0.2, 0.1)
button = visual.Rect(win, width=button_size[0], height=button_size[1], fillColor='white')
button_instruction = visual.TextStim(win, text=task_txt1, color="black")
button.pos = (0, 0)
text_offset = 0.20
button_instruction.pos = (0, button.pos[1] + button.size[1]/2 + text_offset)

mouse = event.Mouse()
button_pressed = False
click_start_time = None
# Main loop
while True:
    button_instruction.draw()
    button.draw()

    if mouse.isPressedIn(button) and not button_pressed:
        click_start_time = core.getTime()
        button_pressed = True

    if mouse.getPressed()[0] == 0 and button_pressed:
        click_end_time = core.getTime()
        click_duration6 = click_end_time - click_start_time
        break

    if 'escape' in event.getKeys():
        break

    win.flip()

win.close()

TimeBox1 = gui.Dlg(title = "Time estimate")
TimeBox1.addText('Please fill in your estimate of the duration:')
TimeBox1.addField('Time Estimate:', color = "blue")
TimeBox1.show()

if TimeBox1.OK:
    Written_6 = TimeBox1.data[0]
elif TimeBox1.Cancel:
    core.quit()


## Presenting Lego introduction ##
win = visual.Window(fullscr = True)
instruction = visual.TextStim(win,text = Lego, color="black", height=0.08)
instruction.draw()
win.flip()
event.waitKeys()
win.close()

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

def start_timer(Condition):
    if Condition == 1:
        speed = 1/1.1
    elif Condition == 2:
        speed = 1
    elif Condition == 3:
        speed = 1/0.9
    else:
        raise ValueError("Invalid condition")
    
    new_window = tk.Toplevel(root)
    new_window.title(f"Timer {speed}x")
    
    # Make the window fullscreen
    new_window.attributes('-fullscreen', True)

    timer_label = tk.Label(new_window, text=f"Time Left: 5:00", font=("Helvetica", 16))
    timer_label.pack(pady=20)
    timer_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    def update_timer_label(new_time):
        timer_label.config(text=new_time)
        if new_time == "Time Left: 00:00":
            # Timer has completed, close the window
            close_timer_window(new_window, timer)

    timer = Timer(minutes=5, speed=speed, update_callback=update_timer_label)
    timer_thread = Thread(target=timer.start)
    timer_thread.start()

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

# Automatically start the timer with the provided condition
timer_thread = Thread(target=lambda: start_timer(Condition))
timer_thread.start()

# Bind the "Escape" key to close the window
root.bind('<Escape>', close_window)

root.mainloop()

## Second Round of Audio Stimuli ##
win = visual.Window(fullscr = True)
instruction2 = visual.TextStim(win,text = Start2, color="black")
instruction2.draw()
win.flip()
event.waitKeys()
win.flip(clearBuffer=True)

## Audio 7 ##
beep = sound.Sound(
    value = 'A', secs = 3,
    volume = 1.0)
beep_time7 = 3
beep.play()
core.wait(4.0)
win.flip()

# Button
button_size = (0.2, 0.1)
button = visual.Rect(win, width=button_size[0], height=button_size[1], fillColor='white')
button_instruction = visual.TextStim(win, text=task_txt1, color="black")
button.pos = (0, 0)
text_offset = 0.20
button_instruction.pos = (0, button.pos[1] + button.size[1]/2 + text_offset)

mouse = event.Mouse()
button_pressed = False
click_start_time = None
# Main loop
while True:
    button_instruction.draw()
    button.draw()

    if mouse.isPressedIn(button) and not button_pressed:
        click_start_time = core.getTime()
        button_pressed = True

    if mouse.getPressed()[0] == 0 and button_pressed:
        click_end_time = core.getTime()
        click_duration7 = click_end_time - click_start_time
        break

    if 'escape' in event.getKeys():
        break

    win.flip()

win.close()

TimeBox1 = gui.Dlg(title = "Time estimate")
TimeBox1.addText('Please fill in your estimate of the duration:')
TimeBox1.addField('Time Estimate:', color = "blue")
TimeBox1.show()

if TimeBox1.OK:
    Written_7 = TimeBox1.data[0]
elif TimeBox1.Cancel:
    core.quit()

## Audio 8 ##
win = visual.Window(fullscr = True)
beep = sound.Sound(
    value = 'A', secs = 6,
    volume = 1.0)
beep_time8 = 6
beep.play()
core.wait(7.0)
win.flip()

# Button
button_size = (0.2, 0.1)
button = visual.Rect(win, width=button_size[0], height=button_size[1], fillColor='white')
button_instruction = visual.TextStim(win, text=task_txt1, color="black")
button.pos = (0, 0)
text_offset = 0.20
button_instruction.pos = (0, button.pos[1] + button.size[1]/2 + text_offset)

mouse = event.Mouse()
button_pressed = False
click_start_time = None
# Main loop
while True:
    button_instruction.draw()
    button.draw()

    if mouse.isPressedIn(button) and not button_pressed:
        click_start_time = core.getTime()
        button_pressed = True

    if mouse.getPressed()[0] == 0 and button_pressed:
        click_end_time = core.getTime()
        click_duration8 = click_end_time - click_start_time
        break

    if 'escape' in event.getKeys():
        break

    win.flip()

win.close()

TimeBox1 = gui.Dlg(title = "Time estimate")
TimeBox1.addText('Please fill in your estimate of the duration:')
TimeBox1.addField('Time Estimate:', color = "blue")
TimeBox1.show()

if TimeBox1.OK:
    Written_8 = TimeBox1.data[0]
elif TimeBox1.Cancel:
    core.quit()

## Audio 9 ##
win = visual.Window(fullscr = True)
beep = sound.Sound(
    value = 'A', secs = 5,
    volume = 1.0)
beep_time9 = 5
beep.play()
core.wait(6.0)
win.flip()

# Button
button_size = (0.2, 0.1)
button = visual.Rect(win, width=button_size[0], height=button_size[1], fillColor='white')
button_instruction = visual.TextStim(win, text=task_txt1, color="black")
button.pos = (0, 0)
text_offset = 0.20
button_instruction.pos = (0, button.pos[1] + button.size[1]/2 + text_offset)

mouse = event.Mouse()
button_pressed = False
click_start_time = None
# Main loop
while True:
    button_instruction.draw()
    button.draw()

    if mouse.isPressedIn(button) and not button_pressed:
        click_start_time = core.getTime()
        button_pressed = True

    if mouse.getPressed()[0] == 0 and button_pressed:
        click_end_time = core.getTime()
        click_duration9 = click_end_time - click_start_time
        break

    if 'escape' in event.getKeys():
        break

    win.flip()

win.close()

TimeBox1 = gui.Dlg(title = "Time estimate")
TimeBox1.addText('Please fill in your estimate of the duration:')
TimeBox1.addField('Time Estimate:', color = "blue")
TimeBox1.show()

if TimeBox1.OK:
    Written_9 = TimeBox1.data[0]
elif TimeBox1.Cancel:
    core.quit()

## Audio 10 ##
win = visual.Window(fullscr = True)
beep = sound.Sound(
    value = 'A', secs = 2,
    volume = 1.0)
beep_time10 = 2
beep.play()
core.wait(3.0)
win.flip()

# Button
button_size = (0.2, 0.1)
button = visual.Rect(win, width=button_size[0], height=button_size[1], fillColor='white')
button_instruction = visual.TextStim(win, text=task_txt1, color="black")
button.pos = (0, 0)
text_offset = 0.20
button_instruction.pos = (0, button.pos[1] + button.size[1]/2 + text_offset)

mouse = event.Mouse()
button_pressed = False
click_start_time = None
# Main loop
while True:
    button_instruction.draw()
    button.draw()

    if mouse.isPressedIn(button) and not button_pressed:
        click_start_time = core.getTime()
        button_pressed = True

    if mouse.getPressed()[0] == 0 and button_pressed:
        click_end_time = core.getTime()
        click_duration10 = click_end_time - click_start_time
        break

    if 'escape' in event.getKeys():
        break

    win.flip()

win.close()

TimeBox1 = gui.Dlg(title = "Time estimate")
TimeBox1.addText('Please fill in your estimate of the duration:')
TimeBox1.addField('Time Estimate:', color = "blue")
TimeBox1.show()

if TimeBox1.OK:
    Written_10 = TimeBox1.data[0]
elif TimeBox1.Cancel:
    core.quit()

## Audio 11 ##
win = visual.Window(fullscr = True)
beep = sound.Sound(
    value = 'A', secs = 9,
    volume = 1.0)
beep_time11 = 9
beep.play()
core.wait(10.0)
win.flip()

# Button
button_size = (0.2, 0.1)
button = visual.Rect(win, width=button_size[0], height=button_size[1], fillColor='white')
button_instruction = visual.TextStim(win, text=task_txt1, color="black")
button.pos = (0, 0)
text_offset = 0.20
button_instruction.pos = (0, button.pos[1] + button.size[1]/2 + text_offset)

mouse = event.Mouse()
button_pressed = False
click_start_time = None
# Main loop
while True:
    button_instruction.draw()
    button.draw()

    if mouse.isPressedIn(button) and not button_pressed:
        click_start_time = core.getTime()
        button_pressed = True

    if mouse.getPressed()[0] == 0 and button_pressed:
        click_end_time = core.getTime()
        click_duration11 = click_end_time - click_start_time
        break

    if 'escape' in event.getKeys():
        break

    win.flip()

win.close()

TimeBox1 = gui.Dlg(title = "Time estimate")
TimeBox1.addText('Please fill in your estimate of the duration:')
TimeBox1.addField('Time Estimate:', color = "blue")
TimeBox1.show()

if TimeBox1.OK:
    Written_11 = TimeBox1.data[0]
elif TimeBox1.Cancel:
    core.quit()

## Audio 12 ##
win = visual.Window(fullscr = True)
beep = sound.Sound(
    value = 'A', secs = 4,
    volume = 1.0)
beep_time12 = 4
beep.play()
core.wait(5.0)
win.flip()

# Button
button_size = (0.2, 0.1)
button = visual.Rect(win, width=button_size[0], height=button_size[1], fillColor='white')
button_instruction = visual.TextStim(win, text=task_txt1, color="black")
button.pos = (0, 0)
text_offset = 0.20
button_instruction.pos = (0, button.pos[1] + button.size[1]/2 + text_offset)

mouse = event.Mouse()
button_pressed = False
click_start_time = None
# Main loop
while True:
    button_instruction.draw()
    button.draw()

    if mouse.isPressedIn(button) and not button_pressed:
        click_start_time = core.getTime()
        button_pressed = True

    if mouse.getPressed()[0] == 0 and button_pressed:
        click_end_time = core.getTime()
        click_duration12 = click_end_time - click_start_time
        break

    if 'escape' in event.getKeys():
        break

    win.flip()

win.close()

TimeBox1 = gui.Dlg(title = "Time estimate")
TimeBox1.addText('Please fill in your estimate of the duration:')
TimeBox1.addField('Time Estimate:', color = "blue")
TimeBox1.show()

if TimeBox1.OK:
    Written_12 = TimeBox1.data[0]
elif TimeBox1.Cancel:
    core.quit()

## End ##
win = visual.Window(fullscr = True)
instruction = visual.TextStim(win,text = end, color="black")
instruction.draw()
win.flip()
event.waitKeys()
# Close the window
win.close()

# Appending data to the logfile
logfile = logfile.append({
    "ID": ID,
    "Condition": Condition,
    "Age": Age,
    "Gender": Gender,
    "Beep_Time1": beep_time1,
    "Button_Estimate_1": click_duration1,
    "Written_Estimate_1": Written_1,
    "Beep_Time2": beep_time2,
    "Button_Estimate_2": click_duration2,
    "Written_Estimate_2": Written_2,
    "Beep_Time3": beep_time3,
    "Button_Estimate_3": click_duration3,
    "Written_Estimate_3": Written_3,
    "Beep_Time4": beep_time4,
    "Button_Estimate_4": click_duration4,
    "Written_Estimate_4": Written_4,
    "Beep_Time5": beep_time5,
    "Button_Estimate_5": click_duration5,
    "Written_Estimate_5": Written_5,
    "Beep_Time6": beep_time6,
    "Button_Estimate_6": click_duration6,
    "Written_Estimate_6": Written_6,
    "Beep_Time7": beep_time7,
    "Button_Estimate_7": click_duration7,
    "Written_Estimate_7": Written_7,
    "Beep_Time8": beep_time8,
    "Button_Estimate_8": click_duration8,
    "Written_Estimate_8": Written_8,
    "Beep_Time9": beep_time9,
    "Button_Estimate_9": click_duration9,
    "Written_Estimate_9": Written_9,
    "Beep_Time10": beep_time10,
    "Button_Estimate_10": click_duration10,
    "Written_Estimate_10": Written_10,
    "Beep_Time11": beep_time11,
    "Button_Estimate_11": click_duration11,
    "Written_Estimate_11": Written_11,
    "Beep_Time12": beep_time12,
    "Button_Estimate_12": click_duration12,
    "Written_Estimate_12": Written_12,
}, ignore_index=True)

# Save logfile
logfile_name = f"logfiles/logfile_{ID}_{Age}_{Gender}.csv"
logfile.to_csv(logfile_name)

