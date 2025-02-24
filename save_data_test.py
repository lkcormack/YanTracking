import numpy as np
import pandas as pd
from psychopy import visual, core, event
from psychopy.hardware import mouse

# Create a window
win = visual.Window(size=[800, 600], color='white', units='pix')

# Create a mouse object
mouse_tracker = mouse.Mouse(win=win)

# Create a clock for timing
clock = core.Clock()

# List to store mouse data
mouse_data = []

# ------------------- INSTRUCTIONS -------------------
# Display instructions
instructions = visual.TextStim(win, text='Move your mouse around.\nPress any key to start.', color='black')
instructions.draw()
win.flip()
event.waitKeys()  # Wait for key press to start the task

# ------------------- MOUSE TRACKING -------------------
# Track mouse movements for 5 seconds
clock.reset()  # Reset the clock to 0
while clock.getTime() < 5:
    pos = mouse_tracker.getPos()          # Get current mouse position
    timestamp = clock.getTime()           # Get current time
    mouse_data.append([timestamp, pos[0], pos[1]])  # Store time and position

    # Draw a red dot at the mouse position
    dot = visual.Circle(win, radius=5, pos=pos, fillColor='red', lineColor='red')
    dot.draw()
    win.flip()

# ------------------- END MESSAGE -------------------
# Display a thank-you message
end_text = visual.TextStim(win, text='Task complete. Thank you!', color='black')
end_text.draw()
win.flip()
core.wait(2)  # Show for 2 seconds

# ------------------- SAVE DATA -------------------
# Convert list to NumPy array
mouse_array = np.array(mouse_data)

# Save as .npy file
np.save('./where_data_goes/tst', mouse_array)

# Also save as .csv file for easy viewing
df = pd.DataFrame(mouse_array, columns=['Time', 'X_Position', 'Y_Position'])
df.to_csv('./where_data_goes/tst.csv', index=False)

print("Mouse data saved as 'mouse_data.npy' and 'mouse_data.csv'.")

# ------------------- CLOSE WINDOW -------------------
win.close()
core.quit()