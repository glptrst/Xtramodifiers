# Turn normal keys into modifiers when held.

from evdev import UInput, InputDevice, categorize, ecodes, list_devices
from evdev_helpers import select_devices
import argparse
import time
import sys
import importlib.util

ui = UInput()

parser = argparse.ArgumentParser(
    description="Make normal keys behave like modifiers when held.")
parser.add_argument("-c", "--config", help="Specify configuration file")
parser.add_argument("-d", "--device", help="Specify device")
args = parser.parse_args()

if args.config:
    path_to_config = args.config
    spec = importlib.util.spec_from_file_location("module.name", path_to_config)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
else: # if no config arg is given, assume there is a config.py in the same dir
    try:
        import config
    except ModuleNotFoundError:
        print("Error: You should either create an extramod_config.py in the same directly or specify a path using the '-c' option.")
        sys.exit()

if args.device:
    dev = InputDevice(args.device)
else:
    # interactivey choose device
    devices = select_devices()
    dev = devices[0]

# Config vars
mod1 = config.config['mod1']
mod1_secondary_function = config.config['mod1_secondary_function']
mod2 = config.config['mod2']
mod2_secondary_function = config.config['mod2_secondary_function']
max_delay = config.config['max_delay']

# Flags
last_input_was_special_combination = False
mod1_down_or_held = False
mod2_down_or_held = False

# Variables for calculating delay
mod1_last_time_down = 0
mod2_last_time_down = 0

dev.grab() # intercept inputs from dev

for event in dev.read_loop(): # reading events from keyboard
    if event.type == ecodes.EV_KEY:
        key_event = categorize(event)
        # print(key_event)
        if key_event.keycode == mod1: # MOD1 EVENT
            if key_event.keystate == 1:
                mod1_down_or_held = True
                print('mod1_down_or_held = True')
                last_input_was_special_combination = False # NECESSARY?
                print('last_input_was_special_combination = False')
                mod1_last_time_down = time.monotonic()
                print('mod1_last_time_down = time.monotonic()')
            elif key_event.keystate == 2:
                mod1_down_or_held = True
                print('mod1_down_or_held = True')
                last_input_was_special_combination = False # NECESSARY?
                print('last_input_was_special_combination = False')
            else: # key_event.keystate == 0
                mod1_down_or_held = False
                print('mod1_down_or_held = False')
                if (mod2_down_or_held):
                    last_input_was_special_combination = True
                    print('last_input_was_special_combination = True')
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[mod2_secondary_function], 1)
                    print(f'{mod2_secondary_function} DOWN')
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[mod1], 1)
                    print(f'{mod1} DOWN')
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[mod1], 0)
                    print(f'{mod1} UP')
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[mod2_secondary_function], 0)
                    ui.syn()
                else:
                    if (last_input_was_special_combination):
                        ui.write(ecodes.EV_KEY, ecodes.ecodes[mod1_secondary_function], 0)
                        print(f'{mod1_secondary_function} UP')
                        ui.syn()
                    else:
                        if (time.monotonic() - mod1_last_time_down < max_delay):
                            ui.write(ecodes.EV_KEY, ecodes.ecodes[mod1], 1)
                            print(f'{mod1} DOWN')
                            ui.write(ecodes.EV_KEY, ecodes.ecodes[mod1], 0)
                            print(f'{mod1} UP')
                            ui.syn()
                        else:
                            pass
        elif key_event.keycode == mod2: # MOD2 EVENT
            if key_event.keystate == 1:
                mod2_down_or_held = True
                print('mod2_down_or_held = True')
                last_input_was_special_combination = False # NECESSARY?
                print('last_input_was_special_combination = False')
                mod2_last_time_down = time.monotonic()
                print('mod2_last_time_down = time.monotonic()')
            elif key_event.keystate == 2:
                mod2_down_or_held = True
                print('mod2_down_or_held = True')
                last_input_was_special_combination = False # NECESSARY?
                print('last_input_was_special_combination = False')
            else: # key_event.keystate == 0
                mod2_down_or_held = False
                print('mod2_down_or_held = False')
                if (mod1_down_or_held):
                    last_input_was_special_combination = True
                    print('last_input_was_special_combination = True')
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[mod1_secondary_function], 1)
                    print(f'{mod1_secondary_function} DOWN')
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[mod2], 1)
                    print(f'{mod2} DOWN')
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[mod2], 0)
                    print(f'{mod2} UP')
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[mod1_secondary_function], 0)
                    ui.syn()
                else:
                    if (last_input_was_special_combination):
                        ui.write(ecodes.EV_KEY, ecodes.ecodes[mod2_secondary_function], 0)
                        print(f'{mod2_secondary_function} UP')
                        ui.syn()
                    else:
                        if (time.monotonic() - mod2_last_time_down < max_delay):
                            ui.write(ecodes.EV_KEY, ecodes.ecodes[mod2], 1)
                            print(f'{mod2} DOWN')
                            ui.write(ecodes.EV_KEY, ecodes.ecodes[mod2], 0)
                            print(f'{mod2} UP')
                            ui.syn()
                        else:
                            pass
        else: # ANY OTHER KEYS
            if key_event.keystate == 1:
                if (mod1_down_or_held):
                    last_input_was_special_combination = True
                    print('last_input_was_special_combination = True')
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[mod1_secondary_function], 1)
                    print(f'{mod1_secondary_function} DOWN')
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[key_event.keycode], 1)
                    print(f'{key_event.keycode} DOWN')
                    ui.syn()
                elif (mod2_down_or_held):
                    last_input_was_special_combination = True
                    print('last_input_was_special_combination = True')
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[mod2_secondary_function], 1)
                    print(f'{mod2_secondary_function} DOWN')
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[key_event.keycode], 1)
                    print(f'{key_event.keycode} DOWN')
                    ui.syn()
                else:
                    last_input_was_special_combination = False
                    print('last_input_was_special_combination = False')
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[key_event.keycode], 1)
                    print(f'{key_event.keycode} DOWN')
                    ui.syn()
            elif key_event.keystate == 2:
                if (mod1_down_or_held):
                    last_input_was_special_combination = True
                    print('last_input_was_special_combination = True')
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[mod1_secondary_function], 1) # NECESSARY?
                    print(f'{mod1_secondary_function} DOWN')
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[key_event.keycode], 2)
                    print(f'{key_event.keycode} HOLD')
                    ui.syn()
                elif (mod2_down_or_held):
                    last_input_was_special_combination = True
                    print('last_input_was_special_combination = True')
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[mod2_secondary_function], 1) # NECESSARY?
                    print(f'{mod2_secondary_function} DOWN')
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[key_event.keycode], 2)
                    print(f'{key_event.keycode} HOLD')
                    ui.syn()
                else:
                    last_input_was_special_combination = False
                    print('last_input_was_special_combination = False')
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[key_event.keycode], 2)
                    print(f'{key_event.keycode} HOLD')
                    ui.syn()
            else: # key_event.keystate == 0
                ui.write(ecodes.EV_KEY, ecodes.ecodes[key_event.keycode], 0)
                print(f'{key_event.keycode} UP')
                ui.syn()
