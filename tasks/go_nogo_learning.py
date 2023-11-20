# Import modules
import time
import hardware_definition as hw
from devices import *
from pyControl.utility import *

# Define states
states = ['init',
          'pretrial',
          'decay',
          'stimuli_horizontal',
          'stimuli_vertical',
          'go_response_window',
          'nogo_response_window',
          'reward', 
          'punishment',
          'end_trial',
          'reward_nogo',
          'punishment_nogo',
          'delay_go',
          'delay_nogo'] 

# Define initial state
initial_state = 'init'

# Define events
events = ['lick', 
          'horizontal', 
          'vertical',
          'dac_1_reward',
          'photodetector',
           'rsync',
           'lick',
           'hit',
           'miss',
           'fa',
           'cr'
          ]


#variable to store
v.trial_number = 0
v.trials_to_run = 50
v.stimuli_duration = 2
v.response_duration = 3
v.reward_duration = 1
v.punishment_duration = 1
v.hori_or_vert = []
v.timer_sec = [5, 7, 10, 12]
v.licks = 0
v.hr = 0
v.far = 0
v.hits = 0
v.misses = 1
v.fa = 1
v.cr = 0

# api variable
v.api_class = 'FLIRRecordingAPI'

# State behaviour

def init(event):
    if event == "entry":
        v.hori_or_vert = ["stimuli_horizontal", "stimuli_vertical"]
        #v.hori_or_vert = ["stimuli_vertical"]
        timed_goto_state('pretrial', 10*second)
def decay(event):
    if event == "entry":
            v.hr = v.hits/(v.hits + v.misses)
            v.far = v.fa/(v.fa + v.cr)
            print_variables(['hr', 'hits', 'misses', 'trial_number'])
            print_variables(['far', 'cr', 'fa', 'trial_number'])
            selected_time = choice(v.timer_sec)
            timed_goto_state('pretrial', 2*second) 

#the pretrial event randomly selects the stimuli to be presented
def pretrial(event):
    if event == "entry":
        v.trial_number += 1
        if v.trial_number <= v.trials_to_run:
            select = choice(v.hori_or_vert)
            timed_goto_state(select, 2*second)
        else:
            timed_goto_state('end_trial', 1)

#the stimuli_horizontal event presents a horizontal stimulus
def stimuli_horizontal(event):
    v.counter = 0
    if event == "entry":
        hw.horizontal.pulse(1000, 75, 3)
        publish_event('horizontal')
        timed_goto_state('delay_nogo', v.stimuli_duration*second)

    elif event == "exit":
        hw.horizontal.off()

#the stimuli_vertical event presents a vertical stimulus
def stimuli_vertical(event):
    v.counter = 0
    if event == "entry":
        hw.vertical.pulse(1000, 75, 3)
        publish_event('vertical')
        timed_goto_state('delay_go', v.stimuli_duration*second)

    elif event == "exit":
        hw.vertical.off()


def delay_nogo(event):
        if event == "entry":
            timed_goto_state('nogo_response_window', 0.5*second)
        elif event == "exit":
            hw.tone.pulse(1000, 75, 3)   


def delay_go(event):
        if event == "entry":
            timed_goto_state('go_response_window', 0.5*second)
        elif event == "exit":
            hw.tone.pulse(1000, 75, 3)            

#the go_response_window event is the response window for the go stimulus
def go_response_window(event):
    if event == "entry":
        timed_goto_state('punishment', v.response_duration*second)
    if event == "lick":
        if v.counter == 0:
            publish_event('hit')
            v.hits += 1
            v.counter += 1
            goto_state('reward')

#the nogo_response_window event is the response window for the nogo stimulus
def nogo_response_window(event):
    if event == "entry":
        timed_goto_state('reward_nogo', v.response_duration*second)
    if event == "lick":
        if v.counter == 0:
            publish_event('fa')
            v.fa += 1
            v.counter += 1
            goto_state('punishment_nogo')
    
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
    timed_goto_state('decay', v.reward_duration*second)

#the reward event delivers a rewardx
def reward_nogo(event):
    if event == "entry":
        publish_event('cr')
        v.cr += 1
        hw.LED.toggle()
    elif event == "exit":
        hw.LED.toggle
    timed_goto_state('decay', v.reward_duration*second)

#the punishment event delivers a punishment
def punishment(event):
    if event == "entry":
        publish_event('miss')
        v.misses += 1
        timed_goto_state('decay', v.punishment_duration*second)

#the punishment event delivers a punishment
def punishment_nogo(event):
    if event == "entry":
        publish_event('fa')
        hw.airpuff.on()
        timed_goto_state('decay', v.punishment_duration*second)
    elif event == "exit":
        hw.airpuff.off()

def end_trial(event): 
    stop_framework()
