# Data

# Importing modules
from psychopy import visual, event, core, sound, gui, data
import pandas as pd, random, os, string
import tkinter as tk

## Logfile ##
# Making sure there is a logfile directory
if not os.path.exists("logfiles"):
    os.makedirs("logfiles")

# Setting up logfile and getting date
columns = ["ID", "Age", "Gender", "Vid_1", "Button_Estimate_1", "Written_Estimate_1", "Vid_2", "Button_Estimate_2", "Written_Estimate_2"]
logfile = pd.DataFrame(columns = columns)

# Creating dialogue box
DialogueBox = gui.Dlg(title = "Time experiment")
DialogueBox.addText('Please fill in the following fields:')
# Adding information fields
DialogueBox.addField('Participant ID:', color = "blue")
DialogueBox.addField('Age:', color = "green")
DialogueBox.addField('Gender:', choices = ["female", "male", "other"], color = "red")
# Showing dialogue box
DialogueBox.show()

# Collecting participant information
if DialogueBox.OK:
    ID = DialogueBox.data[0]
    Age = DialogueBox.data[1]
    Gender = DialogueBox.data[2]
elif DialogueBox.Cancel:
    core.quit()

#Window
win = visual.Window(fullscr = True) #Window

## Text chuncks ##
task_txt1 = '''Press down this button for as long as you felt the stimuli lasted'''
task_txt2 = '''Please write down how long you think the stimuli lasted (in seconds)'''
intro1= '''Hello! And welcome to this experiment! \n (press space to continue)'''
intro2 = '''In this experiment you will be presented with some stimuli, and it will be your task to estimate how long the stimuli lasted. \n (press space to continue)'''

# End text
end = "Thanks for participating"

## Experiment presentation ##
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


# Appending data to the logfile
logfile = logfile.append({
    "ID": ID,
    "Age": Age,
    "Gender": Gender,
    "Vid_1": video_path,
    "Button_Estimate_1": click_duration,
    "Written_Estimate_1": Written_1,
}, ignore_index=True)

# Save logfile
logfile_name = f"logfiles/logfile_{ID}_{Age}_{Gender}.csv"
logfile.to_csv(logfile_name)

