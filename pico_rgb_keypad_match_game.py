import time
from math import ceil
import random
import picokeypad as keypad

keypad.init()
keypad.set_brightness(1.0)

lit = 0
NUM_PADS = keypad.get_num_pads()
colour_index = [0]*NUM_PADS
current_level = 1
    
colours = [{"r": 0x05, "g":0x05, "b":0x05, "name":"clear"},
           {"r": 0x00, "g":0x20, "b":0x00, "name":"green"},
           {"r": 0x20, "g":0x20, "b":0x00, "name":"orange"},
           {"r": 0x20, "g":0x0, "b":0x00, "name":"red"},
           {"r": 0x20, "g":0x00, "b":0x20, "name":"pink"},
           {"r": 0x00, "g":0x00, "b":0x20, "name":"blue"}, 
           {"r": 0x00, "g":0x20, "b":0x20, "name":"light blue"}
           ]

class Level:    
    def __init__(self,level):
        self.level = level
        self.colour_limit = self._calculate_colour_limit()
        self.square_limit = self._calculate_square_limit()
        self.win_condition_i = random.randint(1, self.colour_limit)
    def _calculate_colour_limit(self):
        return self.level%(len(colours)-1) + 1 if self.level%(len(colours)-1) > 1 else 2
    
    def _calculate_square_limit(self):
        limit =  2*(2**ceil(self.level/len(colours)))
        return limit if limit <= 16 else 16

def clear_pad_lights():
    for i in range(0, NUM_PADS):
        keypad.illuminate(i, 0x05, 0x05, 0x05)
    keypad.update()
    
def update_pad_light(colour_i, i):
    keypad.illuminate(i, colours[colour_i]["r"], colours[colour_i]["g"], colours[colour_i]["b"])
    keypad.update()
    
def randomise_lights(level):
    colour_limit = level.colour_limit
    square_limit = level.square_limit 
    if(colour_limit > len(colours) or colour_limit < 0):
        raise ValueError("{} is not a valid limit".format(colour_limit))
    
    clear_pad_lights()
    colour_index = [0]*NUM_PADS
    populated = 0
    
    while populated < square_limit:
        r_index = random.randint(0,NUM_PADS - 1)
        if colour_index[r_index] == 0:
            random_num = random.randint(1, colour_limit)
            colour_index[r_index] = random_num
            update_pad_light(random_num, r_index)
            populated += 1
    return colour_index

def cycle_colour(colour_index, i, limit):
    colour_index[i] = 1 if  colour_index[i] >= limit else colour_index[i] + 1
    update_pad_light(colour_index[i], i)
    return colour_index

def loop(level):
    colour_index = randomise_lights(level)
    while len([i for i in colour_index if i == level.win_condition_i]) != level.square_limit:
        button_states = keypad.get_button_states()
        button = 0
        for i in range(0, NUM_PADS):
            if button_states & 0x01 > 0:
                if not (button_states & (~0x01)) > 0:
                    if colour_index[i] != 0:
                        colour_index = cycle_colour(colour_index, i, level.colour_limit)
                break
            button_states >>= 1
            button += 1
        time.sleep(1/4)
    
def start_level(level):
    print("Level {}".format(level.level))
    print("Make all squares {}".format(colours[level.win_condition_i]["name"]))
    loop(level)
    print("congratulations! ^.^")

while True:
    start_level(Level(current_level))
    current_level += 1
