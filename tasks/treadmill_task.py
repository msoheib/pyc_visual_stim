from pyControl.utility import *

# import pyControl.utility as pc
from devices import *

# Instantiate breakout board object.
board = Breakout_1_2()

# Instantiate analog input on BNC connector BNC_1.
analog_input_1  = Analog_input(pin=board.BNC_1, name='Speed', sampling_rate=1000)

# Instantiate analog input on BNC connector BNC_2.
analog_input_2  = Analog_input(pin=board.BNC_2, name='Direction', sampling_rate=1000)

states = ['trial_start'
          ]

events = ['started_running',
          'stopped_running'
          ]

initial_state = 'trial_start'
