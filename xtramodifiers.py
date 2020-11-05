# Turn normal keys into modifiers when held.

from evdev import UInput, InputDevice, categorize, ecodes, list_devices
import time

devices = [InputDevice(path) for path in list_devices()]

for index, device in enumerate(devices):
    print(str(index) + ": ", device.path, device.name, device.phys)

choice = input(f'\nChoice device: [0-{len(devices)-1}]\n')

# print(devices[int(choice)].path)

#dev = InputDevice('/dev/input/event3')
dev = InputDevice(devices[int(choice)].path)
ui = UInput()
dev.grab()

# Config
mod1 = 'KEY_CAPSLOCK'
mod1_secondary_function = 'KEY_LEFTCTRL'
mod2 = 'KEY_ENTER'
mod2_secondary_function = 'KEY_RIGHTCTRL'
max_delay = 0.3

# Flags
last_input_was_special_combination = False
mod1_down_or_held = False
mod2_down_or_held = False

# Variables for calculating delay
mod1_last_time_down = 0
mod2_last_time_down = 0

for event in dev.read_loop(): # reading events from keyboard
    if event.type == ecodes.EV_KEY:
        key_event = categorize(event)
        print(key_event)
        if key_event.keycode == mod1: # MOD1 EVENT
            if key_event.keystate == 1:
                mod1_down_or_held = True
                last_input_was_special_combination = False # NECESSARY?
                mod1_last_time_down = time.monotonic()
            elif key_event.keystate == 2:
                mod1_down_or_held = True
                last_input_was_special_combination = False # NECESSARY?
            else: # key_event.keystate == 0
                mod1_down_or_held = False
                if (last_input_was_special_combination):
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[mod1_secondary_function], 0)
                    ui.syn()
                else:
                    if (time.monotonic() - mod1_last_time_down < max_delay):
                        ui.write(ecodes.EV_KEY, ecodes.ecodes[mod1], 1)
                        ui.write(ecodes.EV_KEY, ecodes.ecodes[mod1], 0)
                        ui.syn()
                    else:
                        pass
        elif key_event.keycode == mod2: # MOD2 EVENT
            if key_event.keystate == 1:
                mod2_down_or_held = True
                last_input_was_special_combination = False # NECESSARY?
                mod2_last_time_down = time.monotonic()
            elif key_event.keystate == 2:
                mod2_down_or_held = True
                last_input_was_special_combination = False # NECESSARY?
            else: # key_event.keystate == 0
                mod2_down_or_held = False
                if (last_input_was_special_combination):
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[mod2_secondary_function], 0)
                    ui.syn()
                else:
                    if (time.monotonic() - mod2_last_time_down < max_delay):
                        ui.write(ecodes.EV_KEY, ecodes.ecodes[mod2], 1)
                        ui.write(ecodes.EV_KEY, ecodes.ecodes[mod2], 0)
                        ui.syn()
        else: # ANY OTHER KEYS
            if key_event.keystate == 1:
                if (mod1_down_or_held):
                    last_input_was_special_combination = True
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[mod1_secondary_function], 1)
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[key_event.keycode], 1)
                    ui.syn()
                elif (mod2_down_or_held):
                    last_input_was_special_combination = True
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[mod2_secondary_function], 1)
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[key_event.keycode], 1)
                    ui.syn()
                else:
                    last_input_was_special_combination = False
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[key_event.keycode], 1)
                    ui.syn()
            elif key_event.keystate == 2:
                if (mod1_down_or_held):
                    last_input_was_special_combination = True
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[mod1_secondary_function], 1) # NECESSARY?
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[key_event.keycode], 2)
                    ui.syn()
                elif (mod2_down_or_held):
                    last_input_was_special_combination = True
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[mod2_secondary_function], 1) # NECESSARY?
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[key_event.keycode], 2)
                    ui.syn()
                else:
                    last_input_was_special_combination = False
                    ui.write(ecodes.EV_KEY, ecodes.ecodes[key_event.keycode], 2)
                    ui.syn()
            else: # key_event.keystate == 0
                ui.write(ecodes.EV_KEY, ecodes.ecodes[key_event.keycode], 0)
                ui.syn()

# BUGS:
#
# - it resets xkb config when it starts; can be avoided?
#
# - hold mod1, then hold mod1_secondary_function's key, release mod1,
#   hit a key, say 'k'. The input sent is /not/
#   mod1_secondary_function's key + 'k', but 'k'.
#
