# Imports
import pyautogui
import keyboard
from pynput.keyboard import Controller, Key
import tkinter as tk
from tkinter import ttk, messagebox
import requests

import winsound
import time

special_keys = {
    'space': Key.space,
    'enter': Key.enter,
    'esc': Key.esc,
    'shift': Key.shift,
    'ctrl': Key.ctrl,
    'alt': Key.alt,
    'tab': Key.tab,
    'backspace': Key.backspace,
    'delete': Key.delete,
    'up': Key.up,
    'down': Key.down,
    'left': Key.left,
    'right': Key.right,
    'home': Key.home,
    'end': Key.end,
    'page_up': Key.page_up,
    'page_down': Key.page_down,
    'caps_lock': Key.caps_lock,
    'cmd': Key.cmd,
    'cmd_r': Key.cmd_r,
    'shift_r': Key.shift_r,
    'ctrl_r': Key.ctrl_r,
    'alt_gr': Key.alt_gr,
    'print_screen': Key.print_screen,
    'scroll_lock': Key.scroll_lock,
    'pause': Key.pause,
    'insert': Key.insert,
    'menu': Key.menu,
    'num_lock': Key.num_lock,
    'f1': Key.f1,
    'f2': Key.f2,
    'f3': Key.f3,
    'f4': Key.f4,
    'f5': Key.f5,
    'f6': Key.f6,
    'f7': Key.f7,
    'f8': Key.f8,
    'f9': Key.f9,
    'f10': Key.f10,
    'f11': Key.f11,
    'f12': Key.f12,
}

azerty_to_qwerty = {
    'q': 'a',
    'z': 'w',
}

keyboard_controller = Controller()

def play_keystrokes(file_path, azerty):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        print("Try rerunning the Macro, if you incounter the issue again please repoti to the discord server")
        return

    for line in lines:
        key, event_type, delay = line.strip().split()
        delay = float(delay)
        time.sleep(delay)

        print(azerty)

        if azerty == 0:
            if key == 'a': key = 'q'
            elif key == 'z': key = 'w'

        if event_type == 'down':
            if key in special_keys:
                keyboard_controller.press(special_keys[key])
            else:
                keyboard_controller.press(key)
        elif event_type == 'up':
            if key in special_keys:
                keyboard_controller.release(special_keys[key])
            else:
                keyboard_controller.release(key)

def record_keystrokes():
    print("Recording... Press END to stop.")
    recorded = []
    start_time = time.time()

    while True:
        event = keyboard.read_event()
        if event.name == 'fin':
            break
        recorded.append((event.name, event.event_type, time.time() - start_time))
        start_time = time.time()

    return recorded


def save_keystrokes(recorded, file_path):
    with open(file_path, 'w') as f:
        for event in recorded:
            f.write(f"{event[0]} {event[1]} {event[2]}\n")

# Record keystrokes
recorded_keys = record_keystrokes()

# Save recorded keys to a file
save_keystrokes(recorded_keys, 'Records/VipCamera.txt')

print("Keystrokes recorded and saved to recorded_keys.txt")
