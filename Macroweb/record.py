# Imports
import pyautogui
import keyboard
from pynput.keyboard import Controller, Key
import tkinter as tk
from tkinter import ttk, messagebox
import requests

import winsound
import time

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
save_keystrokes(recorded_keys, 'Records/Obby.txt')

print("Keystrokes recorded and saved to recorded_keys.txt")
