#!/usr/bin/python3

from helper_functions import *
import modes

from dotenv import load_dotenv
from enum import Enum
from os.path import expandvars
from pathlib import Path
from setuptools import config
from time import sleep
import argparse
import configparser
import datetime as dt
import logging
import sys

#TODO: Write some tests.

VERSION = '1.1'

PROGRAM_NAME = 'change_wallpaper'
PROJECT_DIR = Path(__file__).resolve().parent
CONFIG_FILE = Path(PROJECT_DIR, 'change_wallpaper.config')
ENV_FILE = Path(PROJECT_DIR, 'env_variables.env')

default_values_dict = {
    'wallpapers_dir': expandvars('/home/$USER/Pictures/Wallpapers/'), # This should be a str
    'log_file_path': PROJECT_DIR.joinpath('change_wallpaper.log').as_posix(), # This should also be a str
    'log_level': 'WARNING' # This can be any log level as it's specified in the usage message.
}

# Set up environment variables located inside the 'env_variables.env' file
dotenv_path = ENV_FILE.as_posix()
load_dotenv(dotenv_path)

# Get configuration variables from 'change_wallpaper.config'.
config = configparser.RawConfigParser()
config_file_path = CONFIG_FILE.as_posix()
config.read(config_file_path)

directories_dict = dict(config.items('Directories'))
commands_dict = dict(config.items('Commands'))
other_dict = dict(config.items('Other'))

# [Directories] options
for key, value in directories_dict.copy().items():
    # Replace 'PROJECT_DIR' with its appropiate value for each directory.
    directories_dict[key] = expandvars(value.replace('PROJECT_DIR', PROJECT_DIR.as_posix()))

wallpapers_dir = Path(directories_dict.get('wallpapers_dir', default_values_dict['wallpapers_dir']))
# Add 'wallpapers_dir' to the start of each mode's path.
append_wallpaper_path(wallpapers_dir, modes.global_mode_list)

log_file_path = Path(directories_dict.get('log_file_path', default_values_dict['log_file_path']))
# This may sound trivial, but if no log file exists, the warning message this function issues won't be logged into a file.
check_log_file_exists(log_file_path)

# [Commands] options
command_dark = commands_dict.get('command_dark')
command_light = commands_dict.get('command_dark')

if command_dark is None or command_light is None:
    logging.error("Missing 'command_dark' or 'command_light' from config file. Exiting...")
    sys.exit(1)

# Set up argument parser.
parser = argparse.ArgumentParser(prog=PROGRAM_NAME, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument(
'-v', '--version',
action='version',
version=f'%(prog)s ' + VERSION,
)

# Dynamically generate help message.    
mode_help_message = 'choose a mode from the following list:\n'
for mode in modes.global_mode_list:
    mode_help_message = mode_help_message + f'{mode.id}: {mode.name} ({mode.description})\n'

parser.add_argument(
    '-m', '--mode',
    dest='mode_id',
    action='store',
    type=int,
    help= mode_help_message,
    metavar='ID'
)

parser.add_argument(
    '--log',
    dest='log_level',
    action='store',
    type=str,
    help='select logging level: [DEBUG|INFO|WARNING|ERROR|CRITICAL] (default is WARNING)',
    metavar='LEVEL',
    default=default_values_dict['log_level']
)

# Turn arguments into a dictionary.
args = vars(parser.parse_args()) 

mode_id = args.get('mode_id')
if mode_id is None: # Command line option was not given.
    mode_id = other_dict.get('default_mode_id')

    if mode_id is None: # Option 'default_mode_id' is not set.
        logging.error("Missing value 'default_mode_id' inside config file. Exiting...")
        sys.exit(1)

mode_id = int(mode_id)

log_level = args.get('log_level')

# Set up logging
numeric_level = getattr(logging, log_level.upper(), None)
logging.basicConfig(
    encoding='utf-8',
    level=numeric_level,
    format='%(levelname)s %(asctime)s %(message)s',
    # This makes the logger log both to a stream and to a log file.
    handlers = [logging.FileHandler(log_file_path), logging.StreamHandler()]
)

# Dynamically create a list of all the paths for each mode.
path_list = [mode.path_list for mode in modes.global_mode_list]
check_dir_tree_exists(path_list)

# Main program logic
wallpaper_uri = ''

for mode in modes.global_mode_list:
    if mode.id == mode_id:
        wallpaper_uri = mode.mode_function()

#FIXME: Changes both light and dark mode wallpapers, should be changed in the future.
run_command_with_arg(command_dark, wallpaper_uri)
run_command_with_arg(command_light, wallpaper_uri)