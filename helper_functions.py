from pathlib import Path
import logging
import shlex
import subprocess
import sys

# Returns the URIs of all the files inside 'path'.
def get_uri_list(path: Path) -> list:
    uri_list = []

    for file in path.iterdir():
        if file.is_file():
            uri_list.append(file.as_uri())

    if uri_list == []:
        logging.error(f'Please insert a wallpaper inside "{path}".')
        sys.exit(1)

    return uri_list

def run_command_with_arg(command: str, wallpaper: str) -> None:
    # Split the command into tokens and append the properly formatted wallpaper URI.
    subprocess.run(shlex.split(command) + [wallpaper.replace(' ', '%20')])

# Checks if folders inside directory tree exist, and if not, creates them.
def check_dir_tree_exists(dir_list: list) -> None:
    for dir in dir_list:
        if type(dir) is list:
            check_dir_tree_exists(dir)

        elif not dir.exists():
            logging.warning(f'Folder {dir} does not exist! Creating it now...')
            dir.mkdir(parents=True, exist_ok=True)

# Checks if the log file exists inside the specified folder, and if not, creates it.
def check_log_file_exists(log_file_dir: Path):
    if not log_file_dir.exists():
        logging.warning(f'No log file found in {log_file_dir}! Creating it now...')
        log_file_dir.parent.mkdir(parents=True, exist_ok=True)
        log_file_dir.touch(exist_ok=True)

# Appends the "root" wallpaper path to each mode's path.
def append_wallpaper_path(root: Path, mode_list: list) -> None:
    for mode in mode_list:
        for n, path in enumerate(mode.path_list):
            mode.path_list[n] = root.joinpath(path)