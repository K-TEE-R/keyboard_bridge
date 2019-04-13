#!/bin/bash

cp keyboard_bridge.service /etc/systemd/system/keyboard_bridge.service
systemctl enable keyboard_bridge.service

cp keyboard_gadget.service /etc/systemd/system/keyboard_gadget.service
systemctl enable keyboard_gadget.service

cp usb_gadget_hid_keyboard /usr/bin/usb_gadget_hid_keyboard

mkdir -p /usr/lib/keyboard_bridge
cp keyboard.py keymap.py rainbow.py /usr/lib/keyboard_bridge/

echo "Installation Completed!"

