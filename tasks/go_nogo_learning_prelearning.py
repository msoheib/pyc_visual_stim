# Import modules
import time
import hardware_definition as hw
from devices import *
from pyControl.utility import *

# Define states
states = ['init',
          'pretrial',
          'stimuli_horizontal',
          'stimuli_vertical',
          'go_response_window',
          'nogo_response_window',
          'reward', 
          'punishment',
          'end_trial',
          'results'] 

# Define initial state
initial_state = 'init'

# Define events
events = ['lick', 
          'horizontal', 
          'vertical',
          'dac_1_reward',
          'dac_2_trigger_PV',
          'photodetector',
          'reward_dispensed_dac2',
          'timeout',
           'rsync',
           'hit',
           'false_positive',
          ]

# Define variables

variables = {'trial_number': 0,
             'trials_to_run': 100, # 100 trials
             'go_stimulus': 0, 
             'nogo_stimulus': 0,
             'n_punishment': 0,
             'n_reward': 0,
             'stimuli_duration': 2,
             'response_duration': 3,
             'reward_duration': 5,
             'punishment_duration': 20} 

#variable to store
v.trial_number = 0
v.trials_to_run = 100
v.go_stimulus = 0
v.nogo_stimulus = 0
v.n_punishment = 0
v.n_reward = 0
v.stimuli_duration = 2
v.response_duration = 3
v.reward_duration = 1
v.punishment_duration = 1
v.hori_or_vert = []
v.timer_sec = [5, 7, 10, 12]
v.licks = 1
v.hr = 0
v.hits = 0
v.fa = 1
v.p_counter = 0
v.counter = 0

# api variable
v.api_class = 'FLIRRecordingAPI'



# State behaviour

def init(event):
    if event == "entry":
        v.hori_or_vert = ["stimuli_vertical"]
        timed_goto_state('pretrial', 10*second)

#the pretrial event randomly selects the stimuli to be presented
def pretrial(event):

    if event== 'entry':
        v.p_counter = 0
        v.trial_number += 1
        if v.trial_number <= v.trials_to_run:
            v.hr = v.hits/(v.hits + v.fa)
            print_variables(['hr', 'hits', 'fa', 'trial_number'])
            
            select = choice(v.hori_or_vert)
            selected_time = choice(v.timer_sec)
            
            timed_goto_state(select, selected_time*second) 
        else:
            timed_goto_state('end_trial', 1)

    if event == "lick":
        if v.p_counter == 0:
            publish_event('false_positive')
            v.fa += 1
            v.p_counter += 1


#the stimuli_vertical event presents a vertical stimulus
def stimuli_vertical(event):
    v.counter = 0
    if event == "entry":
        hw.vertical.pulse(60, 75, 5)
        publish_event('vertical')
        timed_goto_state('go_response_window', v.stimuli_duration*second)
    if event == "lick":
        if v.counter == 0:
            publish_event('hit')
            v.hits += 1
            v.counter += 1
            goto_state('reward')

    elif event == "exit":
        hw.vertical.off()

def go_response_window(event):
    if event == "entry":
        timed_goto_state('punishment', v.response_duration*second)
    if event == "lick":
        if v.counter == 0:
            publish_event('hit')
            v.hits += 1
            v.counter += 1
            goto_state('reward')

    elif event == "exit":
        v.go_stimulus += 1
        hw.vertical.off()
        v.n_reward += 1
        print('reward ended')
        hw.dac_1_reward.pulse(60, 75, 5)
        time.sleep(0.002)
        hw.dac_1_reward.off()
        hw.LED.toggle
    timed_goto_state('pretrial', v.stimuli_duration*second)

#the reward event delivers a rewardx
def reward(event):
    if event == "entry":
        hw.LED.toggle()
        
        #first pulse to start
        hw.dac_1_reward.pulse(60, 75, 5)
        time.sleep(0.002)
        hw.dac_1_reward.off()

    elif event == "exit":
        hw.vertical.off()
        hw.dac_1_reward.pulse(60, 75, 5)
        time.sleep(0.002)
        hw.dac_1_reward.off()
        hw.LED.toggle
    timed_goto_state('pretrial', v.reward_duration*second)

def end_trial(event):  # Turn off hardware at end of run.
    stop_framework()
