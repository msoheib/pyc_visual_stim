# Import modules
from pyControl.utility import *
import hardware_definition as hw
from pyControl.utility import *
from devices import *
import time



# Define states
states = ['baseline',
          'end_trial',
          'inter_stimuli_interval',
          'degrees_0',
          'degrees_45',
          'degrees_90',
          'degrees_135',
          'degrees_180',
          'degrees_225',
          'degrees_270',
          'degrees_315'] 

# Define initial state
initial_state = 'baseline'



# Define events
events = ['trigger_0',
        'trigger_45',
        'trigger_90',
        'trigger_135',
        'trigger_180',
        'trigger_225',
        'trigger_270',
        'trigger_315',
        'trigger_isi',
        'dac_2_trigger_PV',
        'photodetector',
        'rsync']

# Define variables

variables = {'trial_number': 0,
             'trials_to_run': 10, # 100 trials
             'go_stimulus': 0, 
             'n_reward': 10, 
             'punishment_duration': 5, 
             'session_duration': 3600,
             'index': 0,
             'orientations_original': ['degrees_0', 'degrees_45','degrees_90','degrees_135'],
             'orientations': []}

v.orientations_original = ['degrees_0', 'degrees_45','degrees_90','degrees_135','degrees_180','degrees_225','degrees_270','degrees_315']


v.trials_to_run = 5
v.orientations_original = v.trials_to_run * v.orientations_original

v.orientations = []
v.index = 0

#v.orientations_original = ['degrees_225']
#v.orientations = v.orientations_original

v.stim_duration = 2*second
v.inter_stimuli_interval = 8*second

#set variable via api here
#v.api_class = 'go_nogo_learning'
v.api_class = 'FLIRRecordingAPI'


# State behaviour

#the pretrial event randomly selects the stimuli to be presented
def baseline(event):
    if event == "entry":
        hw.trigger_isi.on()
        #randomize the orientations
        v.orientations = shuffled(v.orientations_original)
        print(v.orientations)
        hw.trigger_isi.off()
        timed_goto_state('inter_stimuli_interval', 10*second)


def inter_stimuli_interval(event):
    if event == "entry":
        hw.trigger_isi.on()
        if v.index == len(v.orientations):
            timed_goto_state('end_trial', 1*second)
        else:
            timed_goto_state(v.orientations[v.index], v.inter_stimuli_interval)
    if event == "exit":
        v.index = v.index + 1
        hw.trigger_isi.off()

#the stimuli for 0 degrees
def degrees_0(event):
    if event == "entry":
        publish_event('trigger_0')
        hw.trigger_0.on()
        timed_goto_state('inter_stimuli_interval', v.stim_duration)
    elif event == "exit":
        hw.trigger_0.off()

#the stimuli for 45 degrees
def degrees_45(event):
    if event == "entry":
        publish_event('trigger_45')
        hw.trigger_45.on()
        timed_goto_state('inter_stimuli_interval', v.stim_duration)

    elif event == "exit":
        hw.trigger_45.off()

#the stimuli for 90 degrees
def degrees_90(event):
    if event == "entry":
        publish_event('trigger_90')
        hw.trigger_90.on()
        timed_goto_state('inter_stimuli_interval', v.stim_duration)

    elif event == "exit":
        hw.trigger_90.off()

#the stimuli for 135 degrees
def degrees_135(event):
    if event == "entry":
        publish_event('trigger_135')
        hw.trigger_135.on()
        timed_goto_state('inter_stimuli_interval', v.stim_duration)

    elif event == "exit":
        hw.trigger_135.off()

#the stimuli for 180 degrees
def degrees_180(event):
    if event == "entry":
        publish_event('trigger_180')
        hw.trigger_180.on()
        timed_goto_state('inter_stimuli_interval', v.stim_duration)

    elif event == "exit":
        hw.trigger_180.off()
#the stimuli for 225 degrees
def degrees_225(event):
    if event == "entry":
        publish_event('trigger_225')
        hw.trigger_225.on()
        timed_goto_state('inter_stimuli_interval', v.stim_duration)

    elif event == "exit":
        hw.trigger_225.off()
#the stimuli for 270 degrees
def degrees_270(event):
    if event == "entry":
        publish_event('trigger_270')
        hw.trigger_270.on()
        timed_goto_state('inter_stimuli_interval', v.stim_duration)

    elif event == "exit":
        hw.trigger_270.off()
#the stimuli for 315 degrees
def degrees_315(event):
    if event == "entry":
        publish_event('trigger_315')
        hw.trigger_315.on()
        timed_goto_state('inter_stimuli_interval', v.stim_duration)

    elif event == "exit":
        hw.trigger_315.off()

def end_trial(event):
    if event == "entry":
        #hw.dac_2_trigger_PV.on()
        stop_framework()  # Turn off hardware at end of run.
