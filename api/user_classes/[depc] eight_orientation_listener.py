#%%
from pyfirmata import ArduinoMega, util
from psychopy import visual, core
import time

# Initialize the board
board = ArduinoMega('COM11') # replace 'COM11' with your Arduino's port

#%%
# Initialize the iterator thread to read the input
it = util.Iterator(board)
it.start()

# for easier access to changing pins on the arduino
pin_10 = board.get_pin('d:10:i')
pin_40 = board.get_pin('d:40:i')
pin_41 = board.get_pin('d:41:i')
pin_42 = board.get_pin('d:42:i')
pin_43 = board.get_pin('d:43:i')
pin_44 = board.get_pin('d:44:i')
pin_45 = board.get_pin('d:45:i')
pin_46 = board.get_pin('d:46:i')
pin_47 = board.get_pin('d:47:i')

# Start the input on pin 52 and 42, set them to pull-up mode
pin_10.enable_reporting()
pin_40.enable_reporting()
pin_41.enable_reporting()
pin_42.enable_reporting()
pin_43.enable_reporting()
pin_44.enable_reporting()
pin_45.enable_reporting()
pin_46.enable_reporting()
pin_47.enable_reporting()

# Create a window
win = visual.Window([1920, 1080], monitor="native", units="degFlat", color=(0,0,0), checkTiming=True)


win.recordFrameIntervals = True

print(win.monitorFramePeriod)
# Create a list of grating stimuli for each orientation
visualGratings = []
visualGratings.append(visual.GratingStim(win, tex='sin', size=300, sf=1, ori=0))
visualGratings.append(visual.GratingStim(win, tex='sin', size=300, sf=1, ori=45))
visualGratings.append(visual.GratingStim(win, tex='sin', size=300, sf=1, ori=90))
visualGratings.append(visual.GratingStim(win, tex='sin', size=300, sf=1, ori=135))
visualGratings.append(visual.GratingStim(win, tex='sin', size=300, sf=1, ori=180))
visualGratings.append(visual.GratingStim(win, tex='sin', size=300, sf=1, ori=225))
visualGratings.append(visual.GratingStim(win, tex='sin', size=300, sf=1, ori=270))
visualGratings.append(visual.GratingStim(win, tex='sin', size=300, sf=1, ori=315))


#Create the box for photodetector
small_box = visual.Rect(win, width=1, height=1, fillColor=(1,1,1), pos=(-3,-3), lineColor=(1,1,1))

visualGratings.append(small_box)
# Create stimuli with spatial frequency of 1 cycle per degree
#visualGratings = visual.GratingStim(win, tex='sin', size=300, sf=1, ori=0)

#set durations
stimuli_duration = 510 #int(8.5 * 60) sec * 60 frames per second
inter_stimuli_interval = 30 #int(1.5 * 60) sec * 60 frames per second

#set temporal frequency
tf = 0.02

# Create a list of buffers for each orientation
buffers = []
for stim in visualGratings:
    buffer = visual.BufferImageStim(win, stim=[stim])
    buffer.draw()
    buffers.append(buffer)


while True:
    if pin_40.read() == 1:
        buffer = buffers[0]
    elif pin_42.read() == 1:
        buffer = buffers[1]
    elif pin_41.read() == 1:
        buffer = buffers[2]
    elif pin_43.read() == 1:
        buffer = buffers[3]

    # Display the grating
    for _ in range(inter_stimuli_interval):  # assume 60 frames per second
        buffer.draw()
        win.flip()
    # Add a short delay
    time.sleep(0.001)