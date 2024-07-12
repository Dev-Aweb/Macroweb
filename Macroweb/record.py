import pyautogui
import winsound
import keyboard
from pynput.keyboard import Controller, Key
import time
from PIL import Image
import cv2
import numpy as np

def check(times, cooldown):
    for i in range(times):
        time.sleep(cooldown)
        print(pyautogui.position())
        winsound.Beep(1000, 100)

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


#save_keystrokes(record_keystrokes(), 'Records/sss.txt')
check(1, 3)
