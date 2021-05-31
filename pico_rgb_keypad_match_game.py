import time
import random
import picokeypad as keypad

keypad.init()
keypad.set_brightness(1.0)

lit = 0
colour_index = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
current_level = 1

NUM_PADS = keypad.get_num_pads()
    
colours = [{"r": 0x00, "g":0x20, "b":0x00, "name":"green"},
           {"r": 0x20, "g":0x20, "b":0x00, "name":"orange"},
           {"r": 0x20, "g":0x0, "b":0x00, "name":"red"},
           {"r": 0x20, "g":0x00, "b":0x20, "name":"pink"},
           {"r": 0x00, "g":0x00, "b":0x20, "name":"blue"}, 
           {"r": 0x00, "g":0x20, "b":0x20, "name":"light blue"}
           ]

class Level:
    def __init__(self,colour_limit):
        self.limit = colour_limit
        self.win_condition_i = random.randint(0, colour_limit)

def initiate_pad_lights():
    for i in range(0, NUM_PADS):
        keypad.illuminate(i, 0x05, 0x05, 0x05)
    keypad.update()
    
def update_pad_light(colour_i, i):
    keypad.illuminate(i, colours[colour_i]["r"], colours[colour_i]["g"], colours[colour_i]["b"])
    keypad.update()
    
def randomise_lights(limit):
    if(limit > len(colours) or limit < 0):
        raise ValueError("{} is not a valid limit".format(limit))
    for i in range(0,len(colour_index) - 1):
        random_num = random.randint(0, limit)
        colour_index[i] = random_num
    for x in range(0, len(colour_index)):
        update_pad_light(colour_index[x], x)

def cycle_colour(i, limit):
    colour_index[i] = 0 if  colour_index[i] >= limit else colour_index[i] + 1
    update_pad_light(colour_index[i], i)

def loop(level):
    while not (all(i == level.win_condition_i for i in colour_index)):
        button_states = keypad.get_button_states()
        button = 0
        for i in range(0, NUM_PADS):
            if button_states & 0x01 > 0:
                if not (button_states & (~0x01)) > 0:
                    cycle_colour(i, level.limit)
                break
            button_states >>= 1
            button += 1
        time.sleep(1/4)
    

def start_level(level):
    randomise_lights(level.limit)

    print('Make all squares {}'.format(colours[level.win_condition_i]["name"]))
    loop(level)
    print("congratulations! ^.^")

initiate_pad_lights()

while True:
    start_level(Level(current_level))
    current_level = 1 if current_level > len(colours) else current_level + 1 
