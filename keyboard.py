#!/usr/bin/python
#coding: utf-8

import evdev
import time
import keymap
from rainbow import Rainbow

modkey = [0, 0, 0, 0, 0, 0, 0, 0]

while True:
    hidg_dev = open('/dev/hidg0', mode='wb')
    if hidg_dev != None:
        print('Found HID gadget device')
        break
    print('Waiting for HID gadget device')
    time.sleep(1)

while True:
    try:
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        if len(devices) == 0:
            print('No input devices are found. Waiting for next detection')
            time.sleep(1)
            
        for device in devices:
            key = 0
            print(device.fn, device.name, device.phys)
            if 'keyboard' in device.name.lower():
                print('Keyboard device {} is found.'.format(device.name))
            else:
                print('Waiting for keyboard device')
                time.sleep(1)
                continue
            device = evdev.InputDevice(device.fn)
            rainbow = Rainbow()
            for event in device.read_loop():
                print('type={}, code={}, value={}'.format(event.type, event.code, event.value))
                if event.type == evdev.ecodes.EV_KEY:
                     if event.value != 2:
                         key = event.code
                         evdev_code = evdev.ecodes.KEY[key]
                         modkey_element = keymap.modkey(evdev_code)

                         if modkey_element > 0:
                             if event.value == 1:
                                 modkey[modkey_element] = 1
                             else:
                                 modkey[modkey_element] = 0
                             continue

                         bin_str = ""          
                         for bit in modkey:
                             bin_str += str(bit)

                         modbyte = int(bin_str, 2)

                         if event.value == 0:
                            key = 0
                         else:
                            key = event.code
                            rainbow.increment()
                             
                         evdev_code = evdev.ecodes.KEY[key]
                         modkey_element = keymap.modkey(evdev_code)

                         if event.value == 0:
                             key = 0
                         else:
                             key = event.code

                         barray = bytearray([modbyte, 0, keymap.keytable[evdev_code], 0, 0, 0, 0, 0])
                         hidg_dev.write(barray)
                         hidg_dev.flush()
    except IOError as ioe:
        print(type(ioe))
    finally:
        print('No input devices are found. Waiting for next detection')
    

hidg_dev.close()
