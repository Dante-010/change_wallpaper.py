from helper_functions import get_uri_list

from pathlib import Path
import datetime as dt
import itertools
import random

# I know global variables are evil, but I think this use case justifies it.
# I didn't want to overengineer the whole thing (although one could argue that I did), and
# this allows me and any contributor to add new modes easily and without digging much into the code.

# All you need to know is that this list is only accesed by 'change_wallpaper.py'

# Could I come up with a solution that does not involve this nasty variable? Probably. But I will stick
# to this choice either way (Feel free to come up with a better solution if you want!).

global_mode_list = []

class Mode:
    __current_id = itertools.count()

    def __init__(self, name: str, description: str, path_list: list, mode_function):
        self.id = next(self.__current_id)
        self.name = name
        self.description = description
        self.path_list = path_list # Does not allow nested lists.
        self.mode_function = mode_function
        global_mode_list.append(self)

# Random mode
random_path = [Path('random/')]
def random_func() -> str:
    uri_list = get_uri_list(random_path[0])
    return random.choice(uri_list)

mode_random = Mode('RANDOM', 'selects a random wallpaper', random_path, random_func)

# Day and Night mode
day_night_list = [(Path('day_and_night/', dir)) for dir in ['day/', 'night/']]
def day_night_func() -> str:
    hour = dt.datetime.today().hour
    chosen_dir = []

    if hour >= 8 and hour <= 19:
        chosen_dir = day_night_list[0]
    else:
        chosen_dir = day_night_list[1]

    uri_list = get_uri_list(chosen_dir)
    return random.choice(uri_list)

mode_day_night = Mode('DAY AND NIGHT', 'switches between two wallpapers, depending on whether its day or night', day_night_list, day_night_func)

# Times of Day mode
times_of_day_list = [(Path('times_of_day/', dir)) for dir in ['morning/', 'afternoon/', 'evening/', 'night/']]
def times_of_day_func() -> str:
    hour = dt.datetime.today().hour

    if hour > 6 and hour <= 11: # Morning
        chosen_dir = times_of_day_list[0]
    
    elif hour > 11 and hour <= 17: # Afternoon
        chosen_dir = times_of_day_list[1]

    elif hour > 17 and hour <= 20: # Evening
        chosen_dir = times_of_day_list[2]

    elif hour > 20 or hour <= 6: # Night
        chosen_dir = times_of_day_list[3]

    uri_list = get_uri_list(chosen_dir)
    return random.choice(uri_list)

mode_times_of_day = Mode('TIMES OF THE DAY', 'switches between four wallpapers as the day progresses', times_of_day_list, times_of_day_func)