# dynamic_wallpaper.py
----------
This is a really small and simple script to automatically change your wallpaper.

I've only tested this on my machine, which runs on Ubuntu 22.04.1 LTS, with GNOME 42.2 and Wayland.

You have three modes available:

0. Random           (Selects a random wallpaper) [DEFAULT].
1. Day and Night    (Switches between two wallpapers, depending if its day or night).
2. Times of Day     (Switches between four wallpapers as the day progresses).

To select a mode, use `dynamic_wallpaper.py -m $MODE_NUMBER`.

Version 1.0 stores wallpapers on hardcoded directories (for now). Here is the directory tree:

Root: `/home/$USER/Pictures/Wallpapers/`
- `random/`
- `day_and_night/`
  - `day/`
  - `night/`
- `times_of_day/`
  - `morning/`
  - `afternoon/`
  - `evening/`
  - `night/`
  
Inside each folder there should be one or more images (if more than one image is present, a random image is chosen each time). Just in case, the script ignores other directories inside the ones listed.

If you want to see a full list of options, just use `dynamic_wallpaper.py -h`.

A configuration file will be added in the future, making it easier to modify certain parameters.