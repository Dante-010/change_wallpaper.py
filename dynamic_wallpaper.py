#!/usr/bin/python3

from enum import Enum
from genericpath import isfile
from time import sleep
import argparse
import datetime as dt
import os
import random
import shlex
import subprocess
import sys

VERSION = '1.0'


# ----- Helper functions and Enums.
class Modes(Enum):
    def __init__(self, id):
        self.id = id

    RANDOM = 0          # Selects a random wallpaper.
    DAY_NIGHT = 1       # Switches between two wallpapers, depending if its day or night.
    TIMES_OF_DAY = 2    # Switches between four wallpapers as the day progresses.


def get_files_uri(dir: str) -> list:
    file_list = os.listdir(dir)
    files_uri = []

    for file in file_list:
        file_path = dir + file
        if os.path.isfile(file_path):
            files_uri.append('file://' + file_path)

    return files_uri

def change_wallpaper(command: str, wallpaper: str) -> None:
    # Split the command into tokens and append the properly formatted wallpaper URI.
    subprocess.run(shlex.split(command_dark_mode) + [wallpaper.replace(' ', '%20')])


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
# -----

# ----- Hardcoded 'constants'.
#TODO: Remove hardcoding (add config file).
wallpapers_dir = '/home/dante/Pictures/Wallpapers/'

day_night_root = wallpapers_dir + 'day_and_night/'
day_night_day_dir = day_night_root + 'day/'
day_night_night_dir = day_night_root + 'night/'

times_of_day_dir = wallpapers_dir + 'times_of_day/'
list_times_of_day = [(times_of_day_dir + time) for time in ['morning', 'afternoon', 'evening', 'night']]

random_dir = wallpapers_dir + 'random/'

command_dark_mode = "gsettings set org.gnome.desktop.background picture-uri-dark"
command_light_mode = "gsettings set org.gnome.desktop.background picture-uri"
# -----

# ---- Set up argument parser.
parser = argparse.ArgumentParser(prog='dynamic_wallpaper.py', description='Dynamically change wallpapers.', formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument(
    '-v', '--version',
    action='version',
    version=f'%(prog)s ' + VERSION,
)

parser.add_argument(
    '-m', '--mode',
    dest='mode',
    action='store',
    help=
'choose a mode from the following list:\n \
    0: Random (Selects a random wallpaper) [DEFAULT]\n \
    1: Day and Night (Switches between two wallpapers, depending if its day or night)\n \
    2: Times of Day (Switches between four wallpapers as the day progresses)',
    metavar='mode',
    type=int,
    default=0
)

parser.add_argument(
    '--sleep',
    dest='sleep_time',
    action='store',
    type=float,
    help='sleep for the specified amount of seconds before executing program. (This may help when running script from wakeup or reboot)',
    metavar='seconds' )
# ----

# Get arguments as a dictionary
args = vars(parser.parse_args()) 

mode = args.get('mode')

sleep_time = args.get('sleep_time')
if sleep_time is not None:
    print(f'Sleeping for {sleep_time} seconds...')
    sleep(sleep_time)

hour = dt.datetime.today().hour
chosen_dir = []

match mode:
    case Modes.RANDOM.id:
        chosen_dir = random_dir

    case Modes.DAY_NIGHT.id:
        if hour >= 8 and hour <= 19: # Between 8AM and 7PM 
            chosen_dir = day_night_day_dir
        else:
            chosen_dir = day_night_night_dir

    case Modes.TIMES_OF_DAY.id:
        if hour > 6 and hour <= 11: # Morning
            chosen_dir = list_times_of_day[0]
        
        elif hour > 11 and hour <= 17: # Afternoon
            chosen_dir = list_times_of_day[1]

        elif hour > 17 and hour <= 20: # Evening
            chosen_dir = list_times_of_day[2]

        elif hour > 20 or hour <= 6: # Night
            chosen_dir = list_times_of_day[3]

    case other:
        eprint('Case undefined.')
        parser.print_usage()
        sys.exit(1)

file_list = get_files_uri(chosen_dir)
if file_list == []:
    eprint(f'Please insert a wallpaper inside "{chosen_dir}"')
    sys.exit(1)

wallpaper = random.choice(file_list)

#FIXME: Does not distinguish between dark mode and light mode (in GNOME).
change_wallpaper(command_dark_mode, wallpaper)
change_wallpaper(command_light_mode, wallpaper)