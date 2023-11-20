#%%
from pyfirmata import ArduinoMega, util
from psychopy import prefs
prefs.hardware['audioLib'] = ['pygame']

from psychopy import visual, core, monitors, sound

mon = monitors.Monitor(name='non_native')
mon.setSizePix((1920, 1080))
mon.setWidth(31)
mon.setDistance(10)
mon.saveMon()


# Initialize the board
board = ArduinoMega('COM10') 

#%%
# Initialize the iterator thread to read the input
it = util.Iterator(board)
it.start()

# for easier access to changing pins on the arduino
horizontal_pin = board.get_pin('d:4:i')
vertical_pin = board.get_pin('d:3:i')
tone_pin = board.get_pin('d:5:i')

# Start the input on pin 30 and 32, set them to pull-up mode

horizontal_pin.enable_reporting()
vertical_pin.enable_reporting()
tone_pin.enable_reporting()

# Create a window
#win = visual.Window([1366, 768], monitor="non_native", screen=1, fullscr=True, units="degFlat", color=(-1,-1,-1))
win = visual.Window([1280, 720], monitor="non_native", fullscr=True, screen=1, units="degFlatPos", color=(0,0,0))

#Create the box for photodetector
square = visual.Rect(win, width=8, height=8, pos=[-42,-202], fillColor='black', lineColor=(1,1,1))


sf = 0.1

#Que tone
tone = sound.Sound(value=512, secs=0.2, sampleRate=44100, stereo=True)

tone2 = sound.Sound(value=256, secs=0.2, sampleRate=44100, stereo=True)

# Create stimuli
#grating_vertical = visual.GratingStim(win, tex='sin', size=300, sf=sf, ori=0)
#grating_horizontal = visual.GratingStim(win, tex='sin', size=300, sf=sf, ori=90)

grating_vertical = visual.GratingStim(win, tex='sin', size=[800,600], sf=sf, ori=90)

grating_horizontal = visual.GratingStim(win, tex='sin', size=[800,600], sf=sf, ori=0)

stimuli_duration = 2

while True:  
    # If there's a pulse
    if vertical_pin.read() == 1:
        for _ in range(60 * stimuli_duration):
            if _ < 5 or _ > 115:
                grating_horizontal.phase += 0.02  # increment by 1/50th of a cycle
                grating_horizontal.draw()
                square.color = 'white'
                square.draw()
                win.flip()
            else:
                # assume 60 frames per second
                grating_horizontal.phase += 0.02  # increment by 1/50th of a cycle
                grating_horizontal.draw()
                square.color = 'black'
                square.draw()
                win.flip()
        # Show blank screen
        win.flip()
            
    elif horizontal_pin.read() == 1:
        for _ in range(60 * stimuli_duration):
            if _ < 5 or _ > 115:
                grating_vertical.phase += 0.02
                grating_vertical.draw()
                square.color = 'white'
                square.draw()
                win.flip()
            else:
                # assume 60 frames per second
                grating_vertical.phase += 0.02
                grating_vertical.draw()
                square.color = 'black'
                square.draw()
                win.flip()
        # Show blank screen
        win.flip()

    if tone_pin.read() == 1:
        # Show blank screen
        win.flip()
        tone.play()

    # Add a short delay
    core.wait(0.001)
