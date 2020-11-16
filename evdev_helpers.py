import re
from evdev import InputDevice, list_devices

# function taken from evtest.py
def select_devices(device_dir='/dev/input'):
    '''
    Select one or more devices from a list of accessible input devices.
    '''

    def devicenum(device_path):
        digits = re.findall(r'\d+$', device_path)
        return [int(i) for i in digits]

    devices = sorted(list_devices(device_dir), key=devicenum)
    devices = [InputDevice(path) for path in devices]
    if not devices:
        msg = 'error: no input devices found (do you have rw permission on %s/*?)'
        print(msg % device_dir, file=sys.stderr)
        sys.exit(1)

    dev_format = '{0:<3} {1.path:<20} {1.name:<35} {1.phys:<35} {1.uniq:<4}'
    dev_lines = [dev_format.format(num, dev) for num, dev in enumerate(devices)]

    print('ID  {:<20} {:<35} {:<35} {}'.format('Device', 'Name', 'Phys', 'Uniq'))
    print('-' * len(max(dev_lines, key=len)))
    print('\n'.join(dev_lines))
    print()

    choices = input('Select device [0-%s]: ' % (len(dev_lines) - 1))

    try:
        choices = choices.split()
        choices = [devices[int(num)] for num in choices]
    except ValueError:
        choices = None

    if not choices:
        msg = 'error: invalid input - please enter one or more numbers separated by spaces'
        print(msg, file=sys.stderr)
        sys.exit(1)

    return choices
