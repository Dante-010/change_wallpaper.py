# dynamic_wallpaper.py
----------
This is a really small and simple script to automatically change your wallpaper.

## Usage
```
usage: change_wallpaper [-h] [-v] [-m ID] [--log LEVEL]

options:
  -h, --help        show this help message and exit
  -v, --version     show program's version number and exit
  -m ID, --mode ID  choose a mode from the following list:
                    0: RANDOM (selects a random wallpaper)
                    1: DAY AND NIGHT (switches between two wallpapers, depending on whether its day or night)
                    2: TIMES OF THE DAY (switches between four wallpapers as the day progresses)
  --log LEVEL       select logging level: [DEBUG|INFO|WARNING|ERROR|CRITICAL] (default is ERROR)
```

## Directory tree
`wallpapers_dir/`
- `random/`
- `day_and_night/`
  - `day/`
  - `night/`
- `times_of_day/`
  - `morning/`
  - `afternoon/`
  - `evening/`
  - `night/`

Please note that the value of `wallpapers_dir` is located inside `change_wallpaper.config`.
If the option is not given, its default value is `/home/$USER/Pictures/Wallpapers`

If you want the script to work properly, you should respect this file structure.
Inside each folder there should be one or more images (if more than one image is present, a random image is chosen each time).
Just in case, the script ignores other directories inside the ones listed.

## Config, env, and log files
- `change_wallpaper.config` contains the following options:

```
[Directories]
wallpapers_dir
log_file_path

[Commands]
command_light (*)
command_dark (*)

[Other]
default_mode_id (*)
```

Options marked with `(*)` are required for the program to function correctly.

In directory paths, `PROJECT_DIR` is replaced by the directory where the script is located.

- A log file named `change_wallpaper.log` will be created inside the script's directory by default. You can change its location in the config file.

- `env_variables.env` contains environment variables that are set by the script on runtime. This allows the script to run in situations where these environment variables are not always set (e.g., when rebooting). You can change them however you like, but keep in mind this could alter the program's behaviour.

## Running on reboot, wakeup and hourly
There are many ways to accomplish this. In my personal setup, I have decided to use **cron**, a **systemd** service, and GNOME's **Startup Applications** app. 

### cron
This is how my crontab looks like:
```
@hourly /home/dante/scripts/change_wallpaper/change_wallpaper.py
```
### systemd
In order to make this service, I followed [this StackExchange answer](https://unix.stackexchange.com/a/492497/448805). The following service runs on wakeup:
```
[Unit]
Description=Run change_wallpaper.py
After=suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target

[Service]
User=dante
ExecStart=/home/dante/scripts/change_wallpaper/change_wallpaper.py

[Install]
WantedBy=suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target
```

### Startup Applications
In order to run this script on boot, I added an entry to the Startup Applications app, consisting only of `change_wallpaper`
(this is possible because I created a soft symbolic link to this script inside `$HOME/.local/bin`, although you are not required to do so).

## Running script directly
If you want to run the script directly (e.g., without adding `python3` each time), remember to use `sudo chmod +x change_walpaper.py`.

If you want to be able to run the script without entering its full location each time, you can add it to your `$PATH` variable. One way to do this is to create a symbolic link inside `~/.local/bin`, using `ln -s change_wallpaper.py ~/.local/bin/change_wallpaper`.

## Developing

Future me will probably regret having said this, but the code is pretty self explanatory. The only part I should have to explain is mode creation.

In order to create a new mode, follow these three simple steps:

1. Create a **list of paths**, which contains `Path` objects, *'pointing'* to the folders your mode is going to use. 
   Please note that this list should **not** contain string representations of the paths, nor should it contain other lists (to represent subdirectories, for example), because the program breaks otherwise.
2. Define a function, which takes in **no arguments**, and returns the **URI of the file** you are going to set as the wallpaper, represented as a string.
3. Create an instance of `Mode`, with the following syntax: `my_mode = Mode(name, description, path_list, mode_function)`.

For example:
```
random_path = [Path('random/')]
def random_func() -> str:
    uri_list = get_uri_list(random_path[0])
    return random.choice(uri_list)

mode_random = Mode('RANDOM', 'selects a random wallpaper', random_path, random_func)
```

This new mode is then added to `global_mode_list`, which is used to append the wallpaper path to each mode's directories, dynamically generate a new help message, check the directory tree,
and, finally, iterate through all modes, executing the corresponding function if the provided `ID` is valid.

----------
## Notes
I've only tested this on my machine, which runs on Ubuntu 22.04.1 LTS, with GNOME 42.2 and Wayland. I don't expect it to run anywhere else.

This is just a fun little personal project.
