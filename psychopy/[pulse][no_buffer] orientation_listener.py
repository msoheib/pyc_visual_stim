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
#pin_iti = board.get_pin('d:2:i') #iti
pin_0 = board.get_pin('d:3:i') #0
pin_45 = board.get_pin('d:4:i') #45
pin_90 = board.get_pin('d:5:i') #90
pin_135 = board.get_pin('d:6:i') #135
pin_180 = board.get_pin('d:7:i') #180
pin_225 = board.get_pin('d:8:i') #225
pin_270 = board.get_pin('d:9:i') #270
pin_315 = board.get_pin('d:10:i') #315

# Start the input pins and set them to pull-up mode
#pin_iti.enable_reporting()
pin_0.enable_reporting()
pin_45.enable_reporting()
pin_90.enable_reporting()
pin_135.enable_reporting()
pin_180.enable_reporting()
pin_225.enable_reporting()
pin_270.enable_reporting()
pin_315.enable_reporting()

# Create a window
win = visual.Window([800, 600], monitor="non_native", fullscr=True, screen=1, units="degFlatPos", color=(0,0,0))

#Create the box for photodetector
small_box = visual.Rect(win, width=8, height=8, pos=[-42,-202], fillColor='black', lineColor=(1,1,1))

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
    #if pin_iti.read() == 1:
    #    for _ in range(inter_stimuli_interval):  # assume 60 frames per second
    #        win.flip()

    # 0
    if pin_0.read() == 1:
        visualGratings.ori = 0
        # Display the grating
        for _ in range(stimuli_duration):  # assume 60 frames per second
            if _ < 5 or _ > 115:
                visualGratings.phase += tf # increment by 1/50th of a cycle
                visualGratings.draw()
                small_box.color = 'white'
                small_box.draw()
                win.flip()
            else:
                visualGratings.phase += tf # increment by 1/50th of a cycle
                visualGratings.draw()
                small_box.color = 'black'
                small_box.draw()
                win.flip()

    # 45
    elif pin_45.read() == 1:
        visualGratings.ori = 45
        # Display the grating
        for _ in range(stimuli_duration):  # assume 60 frames per second
            if _ < 5 or _ > 115:
                visualGratings.phase += tf # increment by 1/50th of a cycle
                visualGratings.draw()
                small_box.color = 'white'
                small_box.draw()
                win.flip()
            else:           
                visualGratings.phase += tf # increment by 1/50th of a cycle
                visualGratings.draw()
                small_box.color = 'black'
                small_box.draw()
                win.flip()

    # 90
    elif pin_90.read() == 1:
        visualGratings.ori = 90
        # Display the grating
        for _ in range(stimuli_duration):  # assume 60 frames per second
            if _ < 5 or _ > 115:
                visualGratings.phase += tf # increment by 1/50th of a cycle
                visualGratings.draw()
                small_box.color = 'white'
                small_box.draw()
                win.flip()
            else:
                visualGratings.phase += tf # increment by 1/50th of a cycle
                visualGratings.draw()
                small_box.color = 'black'
                small_box.draw()
                win.flip()


    # 135
    elif pin_135.read() == 1:
        visualGratings.ori = 135
        # Display the grating
        for _ in range(stimuli_duration):  # assume 60 frames per second
            if _ < 5 or _ > 115:
                visualGratings.phase += tf # increment by 1/50th of a cycle
                visualGratings.draw()
                small_box.color = 'white'
                small_box.draw()
                win.flip()
            else:    
                visualGratings.phase += tf # increment by 1/50th of a cycle
                visualGratings.draw()
                small_box.color = 'black'
                small_box.draw()
                win.flip()

    # 180
    elif pin_180.read() == 1:
        visualGratings.ori = 180
        # Display the grating
        for _ in range(stimuli_duration):
            if _ < 5 or _ > 115:
                visualGratings.phase += tf # increment by 1/50th of a cycle
                visualGratings.draw()
                small_box.color = 'white'
                small_box.draw()
                win.flip()
            else: 
                visualGratings.phase += tf
                visualGratings.draw()
                small_box.color = 'black'
                small_box.draw()
                win.flip()

    # 225
    elif pin_225.read() == 1:
        visualGratings.ori = 225
        # Display the grating
        for _ in range(stimuli_duration):
            if _ < 5 or _ > 115:
                visualGratings.phase += tf # increment by 1/50th of a cycle
                visualGratings.draw()
                small_box.color = 'white'
                small_box.draw()
                win.flip()
            else:
                visualGratings.phase += tf
                visualGratings.draw()
                small_box.color = 'black' 
                small_box.draw()
                win.flip()

    # 270
    elif pin_270.read() == 1:
        visualGratings.ori = 270
        # Display the grating
        for _ in range(stimuli_duration):
            if _ < 5 or _ > 115:
                visualGratings.phase += tf # increment by 1/50th of a cycle
                visualGratings.draw()
                small_box.color = 'white'
                small_box.draw()
                win.flip()
            else:
                visualGratings.phase += tf
                visualGratings.draw()
                small_box.color = 'black' 
                small_box.draw()
                win.flip()
    # 315
    elif pin_315.read() == 1:
        visualGratings.ori = 315
        # Display the grating
        for _ in range(stimuli_duration):
            if _ < 5 or _ > 115:
                visualGratings.phase += tf # increment by 1/50th of a cycle
                visualGratings.draw()
                small_box.color = 'white'
                small_box.draw()
                win.flip()
            else: 
                visualGratings.phase += tf
                visualGratings.draw()
                small_box.color = 'black'
                small_box.draw()
                win.flip()
    
    # Add a short delay
    win.flip()
    core.wait(0.001)
