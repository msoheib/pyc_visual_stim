# This hardware definition specifies that 3 pokes are plugged into ports 1-3 and a speaker into
# port 4 of breakout board version 1.2.  The houselight is plugged into the center pokes solenoid socket.

from devices import *
from devices.rotary_encoder import Rotary_encoder

board = Breakout_1_2()

#ports 
trigger_isi = Digital_output(board.port_1.DIO_A) #2
trigger_0 = Digital_output(board.port_2.DIO_A) #3
trigger_45 = Digital_output(board.port_2.DIO_B) #4
trigger_90 = Digital_output(board.port_3.DIO_A) #5
trigger_135 = Digital_output(board.port_3.DIO_B) #6
trigger_180 = Digital_output(board.port_4.DIO_A) #7
trigger_225 = Digital_output(board.port_4.DIO_B) #8
trigger_270 = Digital_output(board.port_5.DIO_A) #9
trigger_315 = Digital_output(board.port_5.DIO_B) #10

photodetector = Digital_input(board.port_6.DIO_B, debounce=1000, rising_event = 'photodetector', pull='down')

#enable for the base
# Instantiate analog input on BNC connector BNC_1.
bnc_1_speed = Analog_input(pin=board.BNC_1, name='Speed', threshold=100, sampling_rate=1000)

# Instantiate analog input on BNC connector BNC_2.
bnc_2_dir = Analog_input(pin=board.BNC_2, name='Direction', threshold=100, sampling_rate=1000)

#dac_2_trigger_PV = Digital_output(board.DAC_2)
dac_2_trigger_PV = Rsync(pin=board.DAC_2, mean_IPI=1000)

#lick = Digital_input('X17', rising_event='lick', pull='up') # pyboard usr button.
LED    = Digital_output('B4') 
