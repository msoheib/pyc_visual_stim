# This hardware definition specifies that 3 pokes are plugged into ports 1-3 and a speaker into
# port 4 of breakout board version 1.2.  The houselight is plugged into the center pokes solenoid socket.

from devices import *
from devices.rotary_encoder import Rotary_encoder

board = Breakout_1_2()

# Instantiate Devices.
lick = Poke(port=board.port_6, rising_event='lick')

#port_2
vertical = Digital_output(board.port_2.DIO_A)

#port_2
horizontal = Digital_output(board.port_2.DIO_B)

#port 6
photodetector = Digital_input(board.port_6.DIO_B, debounce=1000, rising_event = 'photodetector', pull='down')
#port_6
airpuff = Digital_output(board.port_6.POW_A)

#port_3
tone = Digital_output(board.port_3.DIO_A)


# Instantiate analog input on BNC connector BNC_1.
bnc_1_speed = Analog_input(pin=board.BNC_1, name='Speed', threshold=100, sampling_rate=1000)

# Instantiate analog input on BNC connector BNC_2.
bnc_2_dir = Analog_input(pin=board.BNC_2, name='Direction', threshold=100, sampling_rate=1000)


# Instantiate analog input on BNC connector DAC_1.
dac_1_reward = Digital_output(board.DAC_1)

#dac_2_trigger_PV = Digital_output(board.DAC_2)

dac_2_trigger_PV = Rsync(pin=board.DAC_2, mean_IPI=1000)


#lick = Digital_input('X17', rising_event='lick', pull='up') # pyboard usr button.
LED    = Digital_output('B4') 
