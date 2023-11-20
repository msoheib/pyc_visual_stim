#%%
from pyfirmata import ArduinoMega, util
from psychopy import visual, core
import time

# Initialize the board
board = ArduinoMega('COM11') # replace 'COM3' with your Arduino's port

#%%
# Initialize the iterator thread to read the input
it = util.Iterator(board)
it.start()

# for easier access to changing pins on the arduino
horizontal_pin = board.get_pin('d:52:i')
vertical_pin = board.get_pin('d:53:i')

# Start the input on pin 52 and 42, set them to pull-up mode
pin52 = horizontal_pin
pin53 = vertical_pin
pin52.enable_reporting()
pin53.enable_reporting()

# Create a window
win = visual.Window([1920, 1080], monitor="native", units="degFlat", color=(-1,-1,-1))

# Create stimuli
grating_horizontal = visual.GratingStim(win, tex='sin', size=300, sf=1, ori=0)
grating_vertical = visual.GratingStim(win, tex='sin', size=300, sf=1, ori=90)

while True:
    # If there's a pulse
    if pin53.read() == 1:
        # Display the horizontal grating
        for _ in range(60 * 5):  # assume 60 frames per second
            grating_horizontal.phase += 0.02  # increment by 1/50th of a cycle
            grating_horizontal.draw()
            win.flip()
        # Show blank screen
        win.flip()
            
    elif pin52.read() == 1:
        # Display the vertical grating
        for _ in range(60 * 5):
            grating_vertical.phase += 0.02
            grating_vertical.draw()
            win.flip()
        # Show blank screen
        win.flip()
    # Add a short delay
    time.sleep(0.001)