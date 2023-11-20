#%%
from pyfirmata import ArduinoMega, util
from psychopy import visual, core, monitors, sound
import time

mon = monitors.Monitor(name='non_native')
mon.setSizePix((1920, 1080))
mon.setWidth(31)
mon.setDistance(10)
mon.saveMon()


# Initialize the board
board = ArduinoMega('COM10') # Arduino's port

#%%
# Initialize the iterator thread to read the input
it = util.Iterator(board)
it.start()

# for easier access to changing pins on the arduino
pin_10 = board.get_pin('d:11:i') #iti
pin_40 = board.get_pin('d:30:i') #0
pin_41 = board.get_pin('d:41:i') #90
pin_42 = board.get_pin('d:32:i') #45
pin_43 = board.get_pin('d:43:i') #135
pin_44 = board.get_pin('d:44:i') #270
pin_45 = board.get_pin('d:45:i') #180
pin_46 = board.get_pin('d:46:i') #315
pin_47 = board.get_pin('d:47:i') #225

# Start the input pins and set them to pull-up mode
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
win = visual.Window([800, 600], monitor="non_native", fullscr=True, screen=1, units="degFlatPos", color=(0,0,0))

#Create the box for photodetector
small_box = visual.Rect(win, width=10, height=10, pos=[-41,-200], fillColor=(1,1,1), lineColor=(1,1,1))

sf = 0.1

# Create stimuli with spatial frequency of 1 cycle per degree
visualGratings = visual.GratingStim(win, tex='sin', size=200, sf=sf, ori=0)

#set durations
stimuli_duration = 120 #int(2 * 60) sec * 60 frames per second
inter_stimuli_interval = 480 #int(8 * 60) sec * 60 frames per second

#set temporal frequency
tf = 0.02

while True:
    # If there's a pulse
    if pin_10.read() == 1:
        for _ in range(inter_stimuli_interval):  # assume 60 frames per second
            win.flip()

    # 0
    elif pin_40.read() == 1:
        visualGratings.ori = 0
        # Display the grating
        for _ in range(stimuli_duration):  # assume 60 frames per second
            visualGratings.phase += tf # increment by 1/50th of a cycle
            visualGratings.draw()
            small_box.draw()
            win.flip()

    # 45
    elif pin_42.read() == 1:
        visualGratings.ori = 45
        # Display the grating
        for _ in range(stimuli_duration):  # assume 60 frames per second
            visualGratings.phase += tf # increment by 1/50th of a cycle
            visualGratings.draw()
            small_box.draw()
            win.flip()

    # 90
    elif pin_41.read() == 1:
        visualGratings.ori = 90
        # Display the grating
        for _ in range(stimuli_duration):  # assume 60 frames per second
            visualGratings.phase += tf # increment by 1/50th of a cycle
            visualGratings.draw()
            small_box.draw()
            win.flip()

    # 135
    elif pin_43.read() == 1:
        visualGratings.ori = 135
        # Display the grating
        for _ in range(stimuli_duration):  # assume 60 frames per second
            visualGratings.phase += tf # increment by 1/50th of a cycle
            visualGratings.draw()
            small_box.draw()
            win.flip()

    # 270
    elif pin_44.read() == 1:
        visualGratings.ori = 270
        # Display the grating
        for _ in range(stimuli_duration):
            visualGratings.phase += tf
            visualGratings.draw()
            small_box.draw()
            win.flip()
    
    # 180
    elif pin_45.read() == 1:
        visualGratings.ori = 180
        # Display the grating
        for _ in range(stimuli_duration):
            visualGratings.phase += tf
            visualGratings.draw()
            small_box.draw()
            win.flip()
    
    # 315
    elif pin_46.read() == 1:
        visualGratings.ori = 315
        # Display the grating
        for _ in range(stimuli_duration):
            visualGratings.phase += tf
            visualGratings.draw()
            small_box.draw()
            win.flip()
    
    # 225
    elif pin_47.read() == 1:
        visualGratings.ori = 225
        # Display the grating
        for _ in range(stimuli_duration):
            visualGratings.phase += tf
            visualGratings.draw()
            small_box.draw()
            win.flip()

    # Add a short delay
    win.flip()
    core.wait(0.001)
