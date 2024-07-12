# Imports
import pyautogui
import autoit
import keyboard
from pynput.keyboard import Controller, Key
import tkinter as tk
from tkinter import ttk, messagebox
import requests
import pygetwindow as gw
#import pydirectinput as pdi
#import win32api
import numpy as np
import multiprocessing as mp
from multiprocessing import Manager
from PIL import ImageGrab
import ctypes
from tkinter import filedialog
import shutil

import webbrowser as wb
from configparser import ConfigParser
import os

#import winsound
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

def getting_ready(vip, azerty):
    autoit.mouse_wheel("up", 100)
    autoit.mouse_wheel("down", 10)
    play_keystrokes('Records/GettingReady.txt', azerty)
    time.sleep(1)
    autoit.mouse_click("left", int(pyautogui.size().width * 100 / 5485), int(pyautogui.size().height * 100 / 258))
    time.sleep(0.25)
    autoit.mouse_click("left", int(pyautogui.size().width * 100 / 711), int(pyautogui.size().height * 100 / 864))
    time.sleep(0.25)
    pyautogui.moveTo(pyautogui.size().width / 2, pyautogui.size().height / 2)
    time.sleep(0.25)
    if vip:
        play_keystrokes('Records/VipCamera.txt', azerty)
    else:
        play_keystrokes('Records/Camera.txt', azerty)

def main_position(vip, azerty):
    if bool(vip):
        play_keystrokes('Records/VipMainPosition.txt', azerty)
    else:
        play_keystrokes('Records/MainPosition.txt', azerty)

def loop(vip, azerty):
    if vip:
        main_position(vip, azerty)
        play_keystrokes('Records/VipHill.txt', azerty)
        time.sleep(1)
        main_position(vip, azerty)
        play_keystrokes('Records/VipLeaderboard.txt', azerty)
        time.sleep(1)
        main_position(vip, azerty)
        play_keystrokes('Records/VipHouse.txt', azerty)
    else:
        main_position(vip, azerty)
        play_keystrokes('Records/Hill.txt', azerty)
        time.sleep(1)
        main_position(vip, azerty)
        play_keystrokes('Records/Leaderboard.txt', azerty)
        time.sleep(1)
        main_position(vip, azerty)
        play_keystrokes('Records/House.txt', azerty)

def obby(vip, azerty):
    main_position(vip, azerty)
    if vip:
        play_keystrokes('Records/VipObby.txt', azerty)
    else:
        play_keystrokes('Records/Obby.txt', azerty)

def send_discord_embed(webhook_url, title, description, color, fields=None, image_url=None):
    embed = {
        "title": title.strip(),
        "description": description.strip(),
        "color": color
    }

    if fields is not None:
        embed["fields"] = fields

    if image_url is not None:
        embed["image"] = {"url": image_url.strip()}

    payload = {
        "embeds": [embed]
    }

    try:
        response = requests.post(webhook_url.strip(), json=payload)

        if response.status_code == 204:
            return "Embed message sent successfully."
        else:
            return f"Failed to send embed message. Status code: {response.status_code}, Response: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

def upload_image_to_discord(webhook_url, file_path):
    with open(file_path, 'rb') as f:
        response = requests.post(webhook_url, files={'file': f})
    if response.status_code == 200:
        response_data = response.json()
        message_id = response_data['id']
        image_url = response_data['attachments'][0]['url']
        return image_url, message_id
    else:
        raise Exception(f"Failed to upload image. Status code: {response.status_code}, Response: {response.text}")

def screenshot_inventory(webhook):
    time.sleep(0.5)
    filename = 'screenshot.png'
    autoit.mouse_click("left", int(pyautogui.size().width * 100 / 5052), int(pyautogui.size().height * 100 / 308))
    time.sleep(0.2)

    inv = pyautogui.screenshot(region=(0, 0, pyautogui.size().width, pyautogui.size().height))
    inv.save(filename)

    webhook_url = webhook['webhookUrl']

    image_url, message_id = upload_image_to_discord(webhook_url, filename)

    title = "Aura Storage"
    description = ""
    color = 11119017

    result = send_discord_embed(webhook_url, title, description, color, None, image_url)
    print(result)

    os.remove(filename)
    time.sleep(0.2)

    autoit.mouse_click("left", int(pyautogui.size().width * 100 / 5052), int(pyautogui.size().height * 100 / 225))
    autoit.mouse_click("left", int(pyautogui.size().width * 100 / 151), int(pyautogui.size().height * 100 / 363))
    time.sleep(0.2)

    inv = pyautogui.screenshot(region=(0, 0, pyautogui.size().width, pyautogui.size().height))
    inv.save(filename)

    image_url, message_id = upload_image_to_discord(webhook_url, filename)

    title = "Potion Inventory"
    description = ""
    color = 11119017

    result = send_discord_embed(webhook_url, title, description, color, None, image_url)
    print(result)

    autoit.mouse_click("left", int(pyautogui.size().width * 100 / 5052), int(pyautogui.size().height * 100 / 225))

    # Clean up the local file
    os.remove(filename)

def craft_potions(vip, azerty, macro):
    main_position(vip, azerty)
    if vip:
        play_keystrokes('Records/VipStella.txt', azerty)
    else:
        play_keystrokes('Records/Stella.txt', azerty)
    #craft
    if bool(macro['fortuneOne']):
        autoit.mouse_move(int(pyautogui.size().width * 100 / 581), int(pyautogui.size().height * 100 / 675))
        autoit.mouse_move(int(pyautogui.size().width * 100 / 286), int(pyautogui.size().height * 100 / 675))
        autoit.mouse_click('left', int(pyautogui.size().width * 100 / 286), int(pyautogui.size().height * 100 / 270))
        for i in range(5):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 240))
        for i in range(1):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 222))
        for i in range(5):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 208))
        for i in range(1):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 194))
        autoit.mouse_click('left', int(pyautogui.size().width * 100 / 215), int(pyautogui.size().height * 100 / 158))
        #autoit.mouse_click('left', int(pyautogui.size().width * 100 / 166), int(pyautogui.size().height * 100 / 158)) autoadd
    if bool(macro['fortuneTwo']):
        autoit.mouse_move(int(pyautogui.size().width * 100 / 581), int(pyautogui.size().height * 100 / 675))
        autoit.mouse_move(int(pyautogui.size().width * 100 / 286), int(pyautogui.size().height * 100 / 675))
        autoit.mouse_click('left', int(pyautogui.size().width * 100 / 286), int(pyautogui.size().height * 100 / 204))
        for i in range(1):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 240))
        for i in range(10):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 222))
        for i in range(5):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 208))
        for i in range(10):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 194))
        for i in range(2):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 183))
        autoit.mouse_click('left', int(pyautogui.size().width * 100 / 215), int(pyautogui.size().height * 100 / 158))
    if bool(macro['fortuneThree']):
        autoit.mouse_move(int(pyautogui.size().width * 100 / 581), int(pyautogui.size().height * 100 / 675))
        autoit.mouse_move(int(pyautogui.size().width * 100 / 286), int(pyautogui.size().height * 100 / 675))
        autoit.mouse_click('left', int(pyautogui.size().width * 100 / 286), int(pyautogui.size().height * 100 / 164))
        for i in range(1):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 240))
        for i in range(15):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 222))
        for i in range(10):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 208))
        for i in range(15):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 194))
        for i in range(5):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 183))
        autoit.mouse_click('left', int(pyautogui.size().width * 100 / 215), int(pyautogui.size().height * 100 / 158))
    if bool(macro['hasteOne']):
        autoit.mouse_move(int(pyautogui.size().width * 100 / 581), int(pyautogui.size().height * 100 / 372))
        autoit.mouse_move(int(pyautogui.size().width * 100 / 286), int(pyautogui.size().height * 100 / 372))
        autoit.mouse_click('left', int(pyautogui.size().width * 100 / 286), int(pyautogui.size().height * 100 / 270))
        for i in range(5):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 240))
        for i in range(1):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 222))
        for i in range(5):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 208))
        for i in range(1):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 194))
        autoit.mouse_click('left', int(pyautogui.size().width * 100 / 215), int(pyautogui.size().height * 100 / 158))
    if bool(macro['hasteTwo']):
        autoit.mouse_move(int(pyautogui.size().width * 100 / 581), int(pyautogui.size().height * 100 / 372))
        autoit.mouse_move(int(pyautogui.size().width * 100 / 286), int(pyautogui.size().height * 100 / 372))
        autoit.mouse_click('left', int(pyautogui.size().width * 100 / 286), int(pyautogui.size().height * 100 / 204))
        for i in range(1):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 240))
        for i in range(10):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 222))
        for i in range(10):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 208))
        for i in range(15):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 194))
        for i in range(2):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 183))
        autoit.mouse_click('left', int(pyautogui.size().width * 100 / 215), int(pyautogui.size().height * 100 / 158))
    if bool(macro['hasteThree']):
        autoit.mouse_move(int(pyautogui.size().width * 100 / 581), int(pyautogui.size().height * 100 / 372))
        autoit.mouse_move(int(pyautogui.size().width * 100 / 286), int(pyautogui.size().height * 100 / 372))
        autoit.mouse_click('left', int(pyautogui.size().width * 100 / 286), int(pyautogui.size().height * 100 / 164))
        for i in range(1):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 240))
        for i in range(20):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 222))
        for i in range(15):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 208))
        for i in range(25):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 194))
        for i in range(4):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 183))
        autoit.mouse_click('left', int(pyautogui.size().width * 100 / 215), int(pyautogui.size().height * 100 / 158))
    if bool(macro['heavenlyOne']):
        autoit.mouse_move(int(pyautogui.size().width * 100 / 581), int(pyautogui.size().height * 100 / 257))
        autoit.mouse_move(int(pyautogui.size().width * 100 / 286), int(pyautogui.size().height * 100 / 257))
        autoit.mouse_click('left', int(pyautogui.size().width * 100 / 286), int(pyautogui.size().height * 100 / 270))
        for i in range(100):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 240))
        for i in range(50):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 222))
        for i in range(20):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 208))
        for i in range(1):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 194))
        autoit.mouse_click('left', int(pyautogui.size().width * 100 / 215), int(pyautogui.size().height * 100 / 158))
    if bool(macro['heavenlyTwo']):
        autoit.mouse_move(int(pyautogui.size().width * 100 / 581), int(pyautogui.size().height * 100 / 257))
        autoit.mouse_move(int(pyautogui.size().width * 100 / 286), int(pyautogui.size().height * 100 / 257))
        autoit.mouse_click('left', int(pyautogui.size().width * 100 / 286), int(pyautogui.size().height * 100 / 204))
        for i in range(2):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 240))
        for i in range(125):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 222))
        for i in range(75):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 208))
        for i in range(50):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 194))
        for i in range(1):
            autoit.mouse_click('left', int(pyautogui.size().width * 100 / 158), int(pyautogui.size().height * 100 / 183))
        autoit.mouse_click('left', int(pyautogui.size().width * 100 / 215), int(pyautogui.size().height * 100 / 158))
    autoit.mouse_click('left', int(pyautogui.size().width * 100 / 563), int(pyautogui.size().height * 100 / 1611))
    play_keystrokes('Records/Reset.txt', azerty)

def sc_br():
    autoit.mouse_click("left", int(pyautogui.size().width * 100 / 5052), int(pyautogui.size().height * 100 / 225))
    autoit.mouse_click("left", int(pyautogui.size().width * 100 / 151), int(pyautogui.size().height * 100 / 363))
    autoit.mouse_click("left", int(pyautogui.size().width * 100 / 272), int(pyautogui.size().height * 100 / 180))
    autoit.mouse_click("left", int(pyautogui.size().width * 100 / 5052), int(pyautogui.size().height * 100 / 225))

def macro_process(macro, webhook, settings):
    getting_ready(settings['gamepass'], settings['azerty'])

    if bool(macro['doObby']):
        obby(bool(settings['gamepass']), settings['azerty'])
        lastObby = time.time()

    if bool(webhook['screenshotInventory']) and bool(webhook['enableWebhook']):
        screenshot_inventory(webhook)
        lastInventory = time.time()

    if bool(macro['doScbr']):
        sc_br()
        lastScbr = time.time()

    lastCraft = time.time()

    while True:
        loop(settings['gamepass'], settings['azerty'])

        if bool(macro['doObby']):
            if time.time() - lastObby > int(macro['obbyEvery']) * 60:
                obby(bool(settings['gamepass']), settings['azerty'])
                lastObby = time.time()

        if bool(webhook['screenshotInventory']) and bool(webhook['enableWebhook']):
            if time.time() - lastInventory > int(webhook['inventoryEvery']) * 60:
                screenshot_inventory(webhook)
                lastInventory = time.time()

        if bool(macro['doScbr']):
            if time.time() - lastScbr > 20 * 60:
                sc_br()
                lastScbr = time.time()

        if bool(macro['doCraft']):
            if time.time() - lastCraft > int(webhook['craftEvery']) * 60:
                craft_potions(settings['gamepass'], settings['azerty'], macro)
                lastCraft = time.time()

class App:
    def __init__(self):
        # Window
        self.root = tk.Tk()
        self.root.geometry(f"400x550")
        self.root.title("Macroweb")

        self.manager = Manager()
        self.macro = self.manager.dict({
            'doObby': 0,
            'obbyEvery': 0,
            'doScbr': 0,
            'doCraft': 0,
            'craftEvery': 0,
            'fortuneOne': 0,
            'fortuneTwo': 0,
            'fortuneThree': 0,
            'hasteOne': 0,
            'hasteTwo': 0,
            'hasteThree': 0,
            'heavenlyOne': 0,
            'heavenlyTwo': 0,
        })
        self.webhook = self.manager.dict({
            'enableWebhook': 0,
            'webhookUrl': "",
            'userId': "",
            'screenshotInventory': 0,
            'inventoryEvery': 0,
        })
        self.settings = self.manager.dict({
            'start': False,
            'gamepass': 0,
            'azerty': 0,
            'version': "v0.2.0",
        })

        # Notebook (Tabs)
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[15, 4], font=('Arial', 12))

        self.savefile = 'save.ini'
        self.save = ConfigParser()
        self.save.read(self.savefile)

        self.mainFrame = tk.LabelFrame(self.root, padx=5, pady=5)
        self.mainFrame.pack(padx=5, pady=5)

        self.notebook = ttk.Notebook(self.mainFrame, width=400)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Macro')

        # Macro
        self.create_obby_frame()
        self.create_scbr_frame()
        self.create_potions_frame()

        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='Webhook')

        self.create_webhook_frame()

        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='Settings')

        self.create_general_frame()
        self.create_other_frame()

        self.tab4 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab4, text='Credits')

        self.create_creator_frame()
        self.create_inspiration_frame()
        self.create_donation_frame()

        self.start = tk.Button(self.root, text="Start (F1)", font=('', 10), command=self.start_func, width=10)
        self.start.place(x=90,y=515)

        self.end = tk.Button(self.root, text="End (F3)", font=('', 10), command=self.end_func, width=10)
        self.end.place(x=220,y=515)

        keyboard.add_hotkey('F1', self.start_func)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
            if hasattr(self, 'macroProcess') and self.macroProcess.is_alive():
                self.macroProcess.terminate()
                self.macroProcess.join()
            # Macro values type checks and assignments
            self.macro['doObby'] = int(self.isObby.get()) if isinstance(self.isObby.get(), int) else 0
            self.macro['obbyEvery'] = int(self.every.get()) if isinstance(self.every.get(), str) else 0
            self.macro['doScbr'] = int(self.isScbr.get()) if isinstance(self.isScbr.get(), int) else 0
            self.macro['doCraft'] = int(self.isCraft.get()) if isinstance(self.isCraft.get(), int) else 0
            self.macro['craftEvery'] = int(self.craft.get()) if isinstance(self.craft.get(), str) else 0
            self.macro['fortuneOne'] = int(self.isFortuneOne.get()) if isinstance(self.isFortuneOne.get(), int) else 0
            self.macro['fortuneTwo'] = int(self.isFortuneTwo.get()) if isinstance(self.isFortuneTwo.get(), int) else 0
            self.macro['fortuneThree'] = int(self.isFortuneThree.get()) if isinstance(self.isFortuneThree.get(),
                                                                                      int) else 0
            self.macro['hasteOne'] = int(self.isHasteOne.get()) if isinstance(self.isHasteOne.get(), int) else 0
            self.macro['hasteTwo'] = int(self.isHasteTwo.get()) if isinstance(self.isHasteTwo.get(), int) else 0
            self.macro['hasteThree'] = int(self.isHasteThree.get()) if isinstance(self.isHasteThree.get(), int) else 0
            self.macro['heavenlyOne'] = int(self.isHeavenlyOne.get()) if isinstance(self.isHeavenlyOne.get(),
                                                                                    int) else 0
            self.macro['heavenlyTwo'] = int(self.isHeavenlyTwo.get()) if isinstance(self.isHeavenlyTwo.get(),
                                                                                    int) else 0

            # Webhook values type checks and assignments
            self.webhook['enableWebhook'] = int(self.isWebhook.get()) if isinstance(self.isWebhook.get(), int) else 0
            self.webhook['webhookUrl'] = str(self.webhookLink.get()) if isinstance(self.webhookLink.get(), str) else ""
            self.webhook['userId'] = str(self.userid.get()) if isinstance(self.userid.get(), str) else ""
            self.webhook['screenshotInventory'] = int(self.isInventory.get()) if isinstance(self.isInventory.get(),
                                                                                            int) else 0
            self.webhook['inventoryEvery'] = int(self.inventoryInterval.get()) if isinstance(self.inventoryInterval.get(),
                                                                                          str) else 0

            # Settings values type checks and assignments
            self.settings['gamepass'] = int(self.isVip.get()) if isinstance(self.isVip.get(), int) else 1
            self.settings['azerty'] = int(self.isAzerty.get()) if isinstance(self.isAzerty.get(), int) else 0

            # Save macro values
            self.save.set('macro', 'doObby', str(self.macro['doObby']))
            self.save.set('macro', 'obbyEvery', str(self.macro['obbyEvery']))
            self.save.set('macro', 'doScbr', str(self.macro['doScbr']))
            self.save.set('macro', 'doCraft', str(self.macro['doCraft']))
            self.save.set('macro', 'craftEvery', str(self.macro['craftEvery']))
            self.save.set('macro', 'fortuneOne', str(self.macro['fortuneOne']))
            self.save.set('macro', 'fortuneTwo', str(self.macro['fortuneTwo']))
            self.save.set('macro', 'fortuneThree', str(self.macro['fortuneThree']))
            self.save.set('macro', 'hasteOne', str(self.macro['hasteOne']))
            self.save.set('macro', 'hasteTwo', str(self.macro['hasteTwo']))
            self.save.set('macro', 'hasteThree', str(self.macro['hasteThree']))
            self.save.set('macro', 'heavenlyOne', str(self.macro['heavenlyOne']))
            self.save.set('macro', 'heavenlyTwo', str(self.macro['heavenlyTwo']))

            # Save webhook values
            self.save.set('webhook', 'enableWebhook', str(self.webhook['enableWebhook']))
            self.save.set('webhook', 'webhookUrl', str(self.webhook['webhookUrl']))
            self.save.set('webhook', 'userId', str(self.webhook['userId']))
            self.save.set('webhook', 'screenshotInventory', str(self.webhook['screenshotInventory']))
            self.save.set('webhook', 'inventoryEvery', str(self.webhook['inventoryEvery']))

            # Save settings values
            self.save.set('settings', 'gamepass', str(self.settings['gamepass']))
            self.save.set('settings', 'azerty', str(self.settings['azerty']))

            with open(self.savefile, 'w') as f:
                self.save.write(f)

            self.root.destroy()
            quit()

    def start_func(self):
        try:
            if self.settings['start']:
                return
            self.settings['start'] = True

            # Macro values type checks
            self.macro['doObby'] = int(self.isObby.get()) if isinstance(self.isObby.get(), int) else 0
            self.macro['obbyEvery'] = int(self.every.get()) if isinstance(self.every.get(), str) else 0
            self.macro['doScbr'] = int(self.isScbr.get()) if isinstance(self.isScbr.get(), int) else 0
            self.macro['doCraft'] = int(self.isCraft.get()) if isinstance(self.isCraft.get(), int) else 0
            self.macro['craftEvery'] = int(self.craft.get()) if isinstance(self.craft.get(), str) else 0
            self.macro['fortuneOne'] = int(self.isFortuneOne.get()) if isinstance(self.isFortuneOne.get(), int) else 0
            self.macro['fortuneTwo'] = int(self.isFortuneTwo.get()) if isinstance(self.isFortuneTwo.get(), int) else 0
            self.macro['fortuneThree'] = int(self.isFortuneThree.get()) if isinstance(self.isFortuneThree.get(), int) else 0
            self.macro['hasteOne'] = int(self.isHasteOne.get()) if isinstance(self.isHasteOne.get(), int) else 0
            self.macro['hasteTwo'] = int(self.isHasteTwo.get()) if isinstance(self.isHasteTwo.get(), int) else 0
            self.macro['hasteThree'] = int(self.isHasteThree.get()) if isinstance(self.isHasteThree.get(), int) else 0
            self.macro['heavenlyOne'] = int(self.isHeavenlyOne.get()) if isinstance(self.isHeavenlyOne.get(), int) else 0
            self.macro['heavenlyTwo'] = int(self.isHeavenlyTwo.get()) if isinstance(self.isHeavenlyTwo.get(), int) else 0

            # Webhook values type checks
            self.webhook['enableWebhook'] = int(self.isWebhook.get()) if isinstance(self.isWebhook.get(), int) else 0
            self.webhook['webhookUrl'] = str(self.webhookLink.get()) if isinstance(self.webhookLink.get(), str) else ""
            self.webhook['userId'] = str(self.userid.get()) if isinstance(self.userid.get(), str) else ""
            self.webhook['screenshotInventory'] = int(self.isInventory.get()) if isinstance(self.isInventory.get(),
                                                                                            int) else 0
            self.webhook['inventoryEvery'] = int(self.inventoryInterval.get()) if isinstance(self.inventoryInterval.get(),
                                                                                       str) else 0
            # Settings values type checks
            self.settings['gamepass'] = int(self.isVip.get()) if isinstance(self.isVip.get(), int) else 1
            self.settings['azerty'] = int(self.isAzerty.get()) if isinstance(self.isAzerty.get(), int) else 0

            try:
                gw.getWindowsWithTitle('Roblox')[0].activate()
            except Exception:
                self.settings['start'] = False
                print("please open roblox")
                return

            # Start the macro process
            self.macroProcess = mp.Process(target=macro_process, args=(self.macro, self.webhook, self.settings))
            self.macroProcess.start()

            # Add hotkey for ending the process
            keyboard.add_hotkey('F3', self.end_func)

            # Start the detection process if the webhook is enabled

        except Exception as e:
            # Print an error message and stop the execution
            print(f"An error occurred: {e}")
            self.settings['start'] = False

    def end_func(self):
        if not self.settings['start']: return
        self.settings['start'] = False
        keyboard.add_hotkey('F1', self.start_func)
        self.macroProcess.terminate()
        self.macroProcess.join()

    def create_obby_frame(self):
        self.obby = tk.LabelFrame(self.tab1, text="Obby", padx=55, pady=10)
        self.obby.grid(row=0, column=0, padx=5, pady=10)

        self.isObby = tk.IntVar()

        self.doObby = tk.Checkbutton(self.obby, text="Do Obby", variable=self.isObby, command=self.toggle_entry)
        self.doObby.grid(row=0, column=0)

        if self.save.has_option('macro', 'doObby'):
            self.isObby.set(int(self.save.get('macro', 'doObby')))

        self.space = tk.Label(self.obby, text="    ")
        self.space.grid(row=0, column=1)

        self.every_obby = tk.StringVar()

        self.everylabel1 = tk.Label(self.obby, text="Every:")
        self.everylabel1.grid(row=0, column=2)
        self.every = tk.Entry(self.obby, width=5, textvariable=self.every_obby)
        self.every.grid(row=0, column=3, padx=5)
        self.everylabel2 = tk.Label(self.obby, text="minutes      ")
        self.everylabel2.grid(row=0, column=4)

        if self.save.has_option('macro', 'obbyEvery'):
            self.every_obby.set(self.save.get('macro', 'obbyEvery'))

        self.toggle_entry()

    def create_scbr_frame(self):
        self.scbr = tk.LabelFrame(self.tab1, text="Strange Controller/Biome Randomizer Automation", padx=10, pady=10)
        self.scbr.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')

        self.isScbr = tk.IntVar()

        self.doScbr = tk.Checkbutton(self.scbr, text="Use SC/BR every controller cooldown (20 minutes)", variable=self.isScbr)
        self.doScbr.grid(row=7, column=0, columnspan=1, sticky='w')

        if self.save.has_option('macro', 'doScbr'):
            self.isScbr.set(int(self.save.get('macro', 'doScbr')))

        self.toggle_entry()

    def create_potions_frame(self):
        self.potions_frame = tk.LabelFrame(self.tab1, text="Potions", padx=10, pady=10)
        self.potions_frame.grid(row=2, column=0, padx=10, pady=5, sticky='nsew')

        self.isCraft = tk.IntVar()

        self.doCraft = tk.Checkbutton(self.potions_frame, text="Craft Potions", variable=self.isCraft, command=self.toggle_craft)
        self.doCraft.grid(row=0, column=0, columnspan=1, sticky='w')

        if self.save.has_option('macro', 'doCraft'):
            self.isCraft.set(int(self.save.get('macro', 'doCraft')))

        self.craftFrame = tk.Frame(self.potions_frame)
        self.craftFrame.grid(row=1, column=0, columnspan=3, sticky='w')

        self.every_craft = tk.StringVar()

        self.craftlabel1 = tk.Label(self.craftFrame, text="Every:")
        self.craftlabel1.grid(row=0, column=0, sticky='w')
        self.craft = tk.Entry(self.craftFrame, width=5, textvariable=self.every_craft)
        self.craft.grid(row=0, column=1, sticky='w')
        self.craftlabel2 = tk.Label(self.craftFrame, text="minutes      ")
        self.craftlabel2.grid(row=0, column=2, sticky='w')

        if self.save.has_option('macro', 'craftEvery'):
            self.every_craft.set(self.save.get('macro', 'craftEvery'))

        self.isFortuneOne = tk.IntVar()
        self.doFortuneOne = tk.Checkbutton(self.potions_frame, text="Craft Fortune 1", variable=self.isFortuneOne)
        self.doFortuneOne.grid(row=2, column=0, columnspan=1, sticky='w')

        if self.save.has_option('macro', 'fortuneOne'):
            self.isFortuneOne.set(int(self.save.get('macro', 'fortuneOne')))

        self.isFortuneTwo = tk.IntVar()
        self.doFortuneTwo = tk.Checkbutton(self.potions_frame, text="Craft Fortune 2", variable=self.isFortuneTwo)
        self.doFortuneTwo.grid(row=3, column=0, columnspan=1, sticky='w')

        if self.save.has_option('macro', 'fortuneTwo'):
            self.isFortuneTwo.set(int(self.save.get('macro', 'fortuneTwo')))

        self.isFortuneThree = tk.IntVar()
        self.doFortuneThree = tk.Checkbutton(self.potions_frame, text="Craft Fortune 3", variable=self.isFortuneThree)
        self.doFortuneThree.grid(row=4, column=0, columnspan=1, sticky='w')

        if self.save.has_option('macro', 'fortuneThree'):
            self.isFortuneThree.set(int(self.save.get('macro', 'fortuneThree')))

        self.isHasteOne = tk.IntVar()
        self.doHasteOne = tk.Checkbutton(self.potions_frame, text="Craft Haste 1", variable=self.isHasteOne)
        self.doHasteOne.grid(row=5, column=0, columnspan=1, sticky='w')

        if self.save.has_option('macro', 'hasteOne'):
            self.isHasteOne.set(int(self.save.get('macro', 'hasteOne')))

        self.isHasteTwo = tk.IntVar()
        self.doHasteTwo = tk.Checkbutton(self.potions_frame, text="Craft Haste 2", variable=self.isHasteTwo)
        self.doHasteTwo.grid(row=6, column=0, columnspan=1, sticky='w')

        if self.save.has_option('macro', 'hasteTwo'):
            self.isHasteTwo.set(int(self.save.get('macro', 'hasteTwo')))

        self.isHasteThree = tk.IntVar()
        self.doHasteThree = tk.Checkbutton(self.potions_frame, text="Craft Haste 3", variable=self.isHasteThree)
        self.doHasteThree.grid(row=7, column=0, columnspan=1, sticky='w')

        if self.save.has_option('macro', 'hasteThree'):
            self.isHasteThree.set(int(self.save.get('macro', 'hasteThree')))

        self.isHeavenlyOne = tk.IntVar()
        self.doHeavenlyOne = tk.Checkbutton(self.potions_frame, text="Craft Heavenly 1", variable=self.isHeavenlyOne)
        self.doHeavenlyOne.grid(row=8, column=0, columnspan=1, sticky='w')

        if self.save.has_option('macro', 'heavenlyOne'):
            self.isHeavenlyOne.set(int(self.save.get('macro', 'heavenlyOne')))

        self.isHeavenlyTwo = tk.IntVar()
        self.doHeavenlyTwo = tk.Checkbutton(self.potions_frame, text="Craft Heavenly 2", variable=self.isHeavenlyTwo)
        self.doHeavenlyTwo.grid(row=9, column=0, columnspan=1, sticky='w')

        if self.save.has_option('macro', 'heavenlyTwo'):
            self.isHeavenlyTwo.set(int(self.save.get('macro', 'heavenlyTwo')))

        self.toggle_craft()

    def toggle_entry(self):
        if self.isObby.get() == 1:
            self.every.config(state='normal')
            self.everylabel1.config(state='normal')
            self.everylabel2.config(state='normal')
        else:
            self.every.config(state='disabled')
            self.everylabel1.config(state='disabled')
            self.everylabel2.config(state='disabled')

    def toggle_craft(self):
        state = 'normal' if self.isCraft.get() == 1 else 'disabled'
        self.craftlabel1.config(state=state)
        self.craft.config(state=state)
        self.craftlabel2.config(state=state)
        self.doFortuneOne.config(state=state)
        self.doFortuneTwo.config(state=state)
        self.doFortuneThree.config(state=state)
        self.doHasteOne.config(state=state)
        self.doHasteTwo.config(state=state)
        self.doHasteThree.config(state=state)
        self.doHeavenlyOne.config(state=state)
        self.doHeavenlyTwo.config(state=state)

    def create_webhook_frame(self):
        self.webhookframe = tk.LabelFrame(self.tab2, text="Webhook", padx=10, pady=10)
        self.webhookframe.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.isWebhook = tk.IntVar()

        self.doWebhook = tk.Checkbutton(self.webhookframe, text="Enable Webhook", variable=self.isWebhook, command=self.toggle_webhook)
        self.doWebhook.grid(row=0, column=0, columnspan=3, sticky='w')

        if self.save.has_option('webhook', 'enableWebhook'):
            self.isWebhook.set(int(self.save.get('webhook', 'enableWebhook')))

        self.webhookUrl = tk.StringVar()

        self.webhookLabel = tk.Label(self.webhookframe, text="Webhook URL:")
        self.webhookLabel.grid(row=1, column=0, sticky='w')
        self.webhookLink = tk.Entry(self.webhookframe, width=55, textvariable=self.webhookUrl)
        self.webhookLink.grid(row=2, column=0, columnspan=3, sticky='w')

        if self.save.has_option('webhook', 'webhookUrl'):
            self.webhookUrl.set(self.save.get('webhook', 'webhookUrl'))

        self.userId = tk.StringVar()

        self.useridLabel = tk.Label(self.webhookframe, text="Discord User ID For Pings:")
        self.useridLabel.grid(row=3, column=0, sticky='w')
        self.userid = tk.Entry(self.webhookframe, width=55, textvariable=self.userId)
        self.userid.grid(row=4, column=0, columnspan=3, sticky='w')

        if self.save.has_option('webhook', 'userId'):
            self.userId.set(self.save.get('webhook', 'userId'))

        self.isInventory = tk.IntVar()

        self.doInventory = tk.Checkbutton(self.webhookframe, text="Screenshot Inventory", variable=self.isInventory, command=self.toggle_inventory)
        self.doInventory.grid(row=5, column=0, columnspan=1, sticky='w')

        if self.save.has_option('webhook', 'screenshotInventory'):
            self.isInventory.set(int(self.save.get('webhook', 'screenshotInventory')))

        self.inventoryFrame = tk.Frame(self.webhookframe)
        self.inventoryFrame.grid(row=6, column=0, columnspan=3, sticky='w')

        self.inventory_every = tk.StringVar()

        self.inventoryEveryLabel = tk.Label(self.inventoryFrame, text="Every:")
        self.inventoryEveryLabel.grid(row=0, column=0, sticky='w')
        self.inventoryInterval = tk.Entry(self.inventoryFrame, width=10, textvariable=self.inventory_every)
        self.inventoryInterval.grid(row=0, column=1, sticky='w')
        self.inventoryMinutesLabel = tk.Label(self.inventoryFrame, text="minutes")
        self.inventoryMinutesLabel.grid(row=0, column=2, sticky='w')

        if self.save.has_option('webhook', 'inventoryEvery'):
            self.inventory_every.set(self.save.get('webhook', 'inventoryEvery'))

        self.toggle_webhook()
        self.toggle_inventory()

    def toggle_webhook(self):
        state = 'normal' if self.isWebhook.get() == 1 else 'disabled'
        self.webhookLink.config(state=state)
        self.webhookLabel.config(state=state)
        self.useridLabel.config(state=state)
        self.userid.config(state=state)
        self.doInventory.config(state=state)

    def toggle_inventory(self):
        state = 'normal' if self.isInventory.get() == 1 else 'disabled'
        self.inventoryEveryLabel.config(state=state)
        self.inventoryInterval.config(state=state)
        self.inventoryMinutesLabel.config(state=state)

    def create_general_frame(self):
        self.general = tk.LabelFrame(self.tab3, text="General", padx=10, pady=10)
        self.general.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.isVip = tk.IntVar()

        self.doVip = tk.Checkbutton(self.general, text="VIP Gamepass", variable=self.isVip, padx=28)
        self.doVip.grid(row=0, column=0, sticky='w')

        if self.save.has_option('macro', 'gamepass'):
            self.isVip.set(int(self.save.get('macro', 'gamepass')))

        self.isAzerty = tk.IntVar()

        self.doAzerty = tk.Checkbutton(self.general, text="AZERTY keyboard", variable=self.isAzerty, padx=28)
        self.doAzerty.grid(row=0, column=1, sticky='e')

        if self.save.has_option('macro', 'azerty'):
            self.isAzerty.set(int(self.save.get('macro', 'azerty')))

    def create_other_frame(self):
        self.others = tk.LabelFrame(self.tab3, text="Other", padx=10, pady=5)
        self.others.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.version = tk.Label(self.others, text="Version: " + self.settings['version'])
        self.version.grid(row=0, column=0, sticky='w')

    def create_creator_frame(self):
        self.creator = tk.LabelFrame(self.tab4, text="Creator", padx=10, pady=5)
        self.creator.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        self.name = tk.Label(self.creator, text="Aweb", font=('', 18))
        self.name.grid(row=0, column=0, sticky='w')

        self.dm = tk.Label(self.creator, text="Discord: awebgamedev", font=('', 10))
        self.dm.grid(row=2, column=0, sticky='w')

        self.discord = tk.Button(self.creator, text="Discord Server", font=('', 10), command=self.discord_link)
        self.discord.grid(row=3, column=0, sticky='w')

    def discord_link(self):
        wb.open_new_tab("http://aweb.monsite.dz/")

    def create_inspiration_frame(self):
        self.inspiration = tk.LabelFrame(self.tab4, text="inspiration", padx=10, pady=5)
        self.inspiration.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.name = tk.Label(self.inspiration, text="dolphSols Macro", font=('', 18))
        self.name.grid(row=0, column=0, sticky='w')

        self.ins = tk.Label(self.inspiration, text="Another Sols RNG Macro that inspired me a lot to create" , font=('', 10))
        self.ins.grid(row=1, column=0, sticky='w')

        self.ins = tk.Label(self.inspiration, text="this macro", font=('', 10))
        self.ins.grid(row=2, column=0, sticky='w')

        self.doplh = tk.Button(self.inspiration, text="Discord Server", font=('', 10), command=self.dolph_link)
        self.doplh.grid(row=3, column=0, sticky='w')

    def dolph_link(self):
        wb.open_new_tab("http://aweb.monsite.dz/dolph.html")

    def create_donation_frame(self):
        self.donation = tk.LabelFrame(self.tab4, text="Donate", padx=10, pady=5)
        self.donation.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        self.dis = tk.Label(self.donation, text="This macro will always be free, but donations support us" , font=('', 10))
        self.dis.grid(row=0, column=0, sticky='w')

        self.dis = tk.Label(self.donation, text="and are all appreciated", font=('', 10))
        self.dis.grid(row=1, column=0, sticky='w')

        self.donate = tk.Button(self.donation, text="Support Us", font=('', 10), command=self.donate_link)
        self.donate.grid(row=2, column=0, sticky='w')

        self.supporters = tk.Button(self.donation, text="Awesome Supporters", font=('', 10), command=self.supporters_link)
        self.supporters.grid(row=3, column=0, sticky='w')

    def donate_link(self):
        wb.open_new_tab("https://www.roblox.com/games/18164992037/Macroweb-Support-Hub")

    def supporters_link(self):
        messagebox.showinfo(title="Supporters", message="We don't have supporters yet, be first to support\n\n"
                                                        "After donating create a ticket in our discord server and send proof to be in the list and to have the supporter role")


if __name__ == "__main__":
    print(os.getcwd())
    app = App()

