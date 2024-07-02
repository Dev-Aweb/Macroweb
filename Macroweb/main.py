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
    if vip:
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
    filename = 'screenshot.png'
    autoit.mouse_click("left", int(pyautogui.size().width * 100 / 5052), int(pyautogui.size().height * 100 / 308))

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

    autoit.mouse_click("left", int(pyautogui.size().width * 100 / 5052), int(pyautogui.size().height * 100 / 225))
    autoit.mouse_click("left", int(pyautogui.size().width * 100 / 151), int(pyautogui.size().height * 100 / 363))

    inv = pyautogui.screenshot(region=(0, 0, pyautogui.size().width, pyautogui.size().height))
    inv.save(filename)

    image_url, message_id = upload_image_to_discord(webhook_url, filename)

    title = "Potion Inventory"
    description = ""
    color = 11119017

    result = send_discord_embed(webhook_url, title, description, color, None, image_url)
    print(result)

    autoit.mouse_click("left", int(pyautogui.size().width * 100 / 5052), int(pyautogui.size().height * 100 / 245))

    # Clean up the local file
    os.remove(filename)

def load_known_auras(file):
    known_auras = {}
    try:
        with open(file, 'r') as f:
            for line in f:
                name, color, rarity = line.strip().split(',')
                known_auras[name] = (int(color), int(rarity))
    except FileNotFoundError:
        # Initialize with some predefined known auras if the file doesn't exist
        known_auras = {
            "Powered": (16777215, 1000),
            "Aquatic": (5015039, 5000),
            "Nautilus": (5595647, 9999),
            "Permaforst": (8257503, 7500),
            "Stormal": (8947848, 6000),
            "Exotic": (3721688, 8500),
            "Comet": (12505855, 4500),
            "Jade": (616503, 2000),
            "Bounded": (2447103, 3000),
            "Celestial": (9937663, 7000),
            "Kyawthuite": (2627218, 1500),
            "Arcane": (6986495, 3500),
            "Magnetic: Reverse Polarity": (8324735, 4000),
            "Undefined": (3158064, 10000),
            "Astral": (7746247, 2500)
        }
    return known_auras

known_auras = load_known_auras("known_auras.txt")

COLOR_TOLERANCE = 5

def color_distance(color1, color2):
    return np.linalg.norm(np.array(color1) - np.array(color2))

def detect_aura(webhook):
    filename = 'screenshot_aura.png'
    if pyautogui.pixel(int(pyautogui.size().width * 100 / 212), int(pyautogui.size().height * 100 / 3375)) == (0, 0, 0):
        print("Aura cutscene detected")
        time.sleep(1)
        pixel_color = pyautogui.pixel(int(pyautogui.size().width / 2), int(pyautogui.size().height / 2))
        decimal_color = pixel_color[0] * 256 * 256 + pixel_color[1] * 256 + pixel_color[2]
        print(f"Color: {decimal_color}")

        # Convert pixel color to tuple
        pixel_color_tuple = (pixel_color[0], pixel_color[1], pixel_color[2])

        # List to store the closest auras
        closest_auras = []

        # Detect closest aura colors
        for aura_name, (aura_color, rarity) in known_auras.items():
            aura_color_tuple = ((aura_color >> 16) & 255, (aura_color >> 8) & 255, aura_color & 255)
            distance = color_distance(pixel_color_tuple, aura_color_tuple)
            closest_auras.append((aura_name, distance, rarity))

        # Sort by distance and get the top 3 closest auras
        closest_auras.sort(key=lambda x: x[1])
        top_auras = closest_auras[:3]

        # Print the top 3 closest auras
        for aura_name, distance, rarity in top_auras:
            print(f"Possible Aura: {aura_name} (Distance: {distance}, Rarity: {rarity})")

        # Check if the closest match is within the tolerance
        if top_auras[0][1] <= COLOR_TOLERANCE:
            #winsound.Beep(1000, 100)
            print(f"Detected Aura: {top_auras[0][0]} (Distance: {top_auras[0][1]}, Rarity: {top_auras[0][2]})")
            inv = pyautogui.screenshot(region=(0, 0, pyautogui.size().width, pyautogui.size().height))
            inv.save(filename)

            if webhook['auraImage']:
                image_url, message_id = upload_image_to_discord(webhook['webhookUrl'], filename)
            else:
                image_url = None

            title = "YOU ROLLED " + top_auras[0][0]
            color = decimal_color

            if top_auras[0][2] > webhook['pingMin']:
                description = f"Rarity: {top_auras[0][2]}, <@{webhook['userId']}>"
            else:
                description = f"Rarity: {top_auras[0][2]}"

            if top_auras[0][2] > webhook['sendMin']:
                send_discord_embed(webhook['webhookUrl'], title, description, color, None, image_url)
        else:
            #winsound.Beep(500, 500)
            print("No matching aura found within tolerance")
            print(f"Closest guess: {top_auras[0][0]} (Distance: {top_auras[0][1]})")
    else:
        print("Searching")

def macro_process(macro, webhook, settings):
    getting_ready(settings['gamepass'], settings['azerty'])

    if bool(macro['doObby']):
        obby(bool(settings['gamepass']), settings['azerty'])
        lastObby = time.time()

    if bool(webhook['screenshotInventory']) and bool(webhook['enableWebhook']):
        screenshot_inventory(webhook)
        lastInventory = time.time()

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

def detection_check(webhook):
    while True:
        detect_aura(webhook)
        time.sleep(0.5)

class App:
    def __init__(self):
        # Window
        self.root = tk.Tk()
        self.root.geometry(f"400x500")
        self.root.title("Macroweb")

        self.manager = Manager()
        self.macro = self.manager.dict({
            'doObby': 0,
            'obbyEvery': 0,
            'doGlide': 0,
            'glideEvery': 0,
        })
        self.webhook = self.manager.dict({
            'enableWebhook': 0,
            'webhookUrl': "",
            'userId': "",
            'screenshotInventory': 0,
            'inventoryEvery': 0,
            'sendMin': 0,
            'pingMin': 0,
            'auraImage': 0,
        })
        self.settings = self.manager.dict({
            'start': False,
            'gamepass': 1,
            'azerty': 0,
            'version': "0.1",
        })

        # Notebook (Tabs)
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[15, 4], font=('Arial', 12))

        self.mainFrame = tk.LabelFrame(self.root, padx=5, pady=5)
        self.mainFrame.pack(padx=5, pady=5)

        self.notebook = ttk.Notebook(self.mainFrame, width=400)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Macro')

        # Macro
        self.create_obby_frame()

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
        self.start.place(x=90,y=465)

        self.end = tk.Button(self.root, text="End (F3)", font=('', 10), command=self.end_func, width=10)
        self.end.place(x=220,y=465)

        keyboard.add_hotkey('F1', self.start_func)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
            self.root.destroy()
            quit()

    def start_func(self):
        try:
            if self.settings['start']:
                return
            self.settings['start'] = True

            # Macro values type checks
            self.macro['doObby'] = int(self.isObby.get()) if isinstance(self.isObby.get(), int) else 0
            self.macro['obbyEvery'] = int(self.every.get()) if isinstance(self.every.get(), int) else 0

            # Webhook values type checks
            self.webhook['enableWebhook'] = int(self.isWebhook.get()) if isinstance(self.isWebhook.get(), int) else 0
            self.webhook['webhookUrl'] = str(self.webhookLink.get()) if isinstance(self.webhookLink.get(), str) else ""
            self.webhook['userId'] = str(self.userid.get()) if isinstance(self.userid.get(), str) else ""
            self.webhook['screenshotInventory'] = int(self.isInventory.get()) if isinstance(self.isInventory.get(),
                                                                                            int) else 0
            self.webhook['inventoryEvery'] = int(self.isInventory.get()) if isinstance(self.isInventory.get(),
                                                                                       int) else 0
            self.webhook['sendMin'] = int(self.minAura.get()) if isinstance(self.minAura.get(), int) else 0
            self.webhook['pingMin'] = int(self.pingMinAura.get()) if isinstance(self.pingMinAura.get(), int) else 0
            self.webhook['auraImage'] = int(self.sendAuraImages.get()) if isinstance(self.sendAuraImages.get(),
                                                                                     int) else 0

            # Settings values type checks
            self.settings['gamepass'] = int(self.isVip.get()) if isinstance(self.isVip.get(), int) else 1
            self.settings['azerty'] = int(self.isAzerty.get()) if isinstance(self.isAzerty.get(), int) else 0

            print(self.settings['azerty'], self.isAzerty.get())
            print("starting")

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
            if bool(self.webhook['enableWebhook']):
                self.detectionProcess = mp.Process(target=detection_check, args=(self.webhook,))
                self.detectionProcess.start()

        except Exception as e:
            # Print an error message and stop the execution
            print(f"An error occurred: {e}")
            self.settings['start'] = False

    def end_func(self):
        if not self.settings['start']: return
        self.settings['start'] = False
        self.macroProcess.terminate()
        self.macroProcess.join()
        if bool(self.webhook['enableWebhook']):
            self.detectionProcess.terminate()
            self.detectionProcess.join()

        gw.getWindowsWithTitle('Macroweb')[0].activate()
        keyboard.add_hotkey('F1', self.start_func)

    def create_obby_frame(self):
        self.obby = tk.LabelFrame(self.tab1, text="Obby", padx=10, pady=10)
        self.obby.grid(row=0, column=0, padx=6, pady=10)

        self.isObby = tk.IntVar()

        self.doObby = tk.Checkbutton(self.obby, text="Do Obby", variable=self.isObby, command=self.toggle_entry)
        self.doObby.grid(row=0, column=0, columnspan=3, sticky='w')

        self.everylabel1 = tk.Label(self.obby, text="Every:")
        self.everylabel1.grid(row=1, column=0, sticky='e')
        self.every = tk.Entry(self.obby, width=5)
        self.every.grid(row=1, column=1, padx=5)
        self.everylabel2 = tk.Label(self.obby, text="minutes      ")
        self.everylabel2.grid(row=1, column=2, sticky='w')

        self.toggle_entry()

    def toggle_entry(self):
        if self.isObby.get() == 1:
            self.every.config(state='normal')
            self.everylabel1.config(state='normal')
            self.everylabel2.config(state='normal')
        else:
            self.every.config(state='disabled')
            self.everylabel1.config(state='disabled')
            self.everylabel2.config(state='disabled')

    def create_webhook_frame(self):
        self.webhookframe = tk.LabelFrame(self.tab2, text="Webhook", padx=10, pady=10)
        self.webhookframe.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.isWebhook = tk.IntVar()

        self.doWebhook = tk.Checkbutton(self.webhookframe, text="Enable Webhook", variable=self.isWebhook, command=self.toggle_webhook)
        self.doWebhook.grid(row=0, column=0, columnspan=3, sticky='w')

        self.webhookLabel = tk.Label(self.webhookframe, text="Webhook URL:")
        self.webhookLabel.grid(row=1, column=0, sticky='w')
        self.webhookLink = tk.Entry(self.webhookframe, width=55)
        self.webhookLink.grid(row=2, column=0, columnspan=3, sticky='w')

        self.useridLabel = tk.Label(self.webhookframe, text="Discord User ID For Pings:")
        self.useridLabel.grid(row=3, column=0, sticky='w')
        self.userid = tk.Entry(self.webhookframe, width=55)
        self.userid.grid(row=4, column=0, columnspan=3, sticky='w')

        self.isInventory = tk.IntVar()

        self.doInventory = tk.Checkbutton(self.webhookframe, text="Screenshot Inventory", variable=self.isInventory, command=self.toggle_inventory)
        self.doInventory.grid(row=5, column=0, columnspan=1, sticky='w')

        self.inventoryFrame = tk.Frame(self.webhookframe)
        self.inventoryFrame.grid(row=6, column=0, columnspan=3, sticky='w')

        self.inventoryEveryLabel = tk.Label(self.inventoryFrame, text="Every:")
        self.inventoryEveryLabel.grid(row=0, column=0, sticky='w')
        self.inventoryInterval = tk.Entry(self.inventoryFrame, width=10)
        self.inventoryInterval.grid(row=0, column=1, sticky='w')
        self.inventoryMinutesLabel = tk.Label(self.inventoryFrame, text="minutes")
        self.inventoryMinutesLabel.grid(row=0, column=2, sticky='w')

        self.minAuraLabel = tk.Label(self.webhookframe, text="Send minimum Aura:")
        self.minAuraLabel.grid(row=7, column=0, sticky='w')
        self.minAura = tk.Entry(self.webhookframe, width=55)
        self.minAura.grid(row=8, column=0, columnspan=3, sticky='w')

        self.pingMinAuraLabel = tk.Label(self.webhookframe, text="Ping minimum aura:")
        self.pingMinAuraLabel.grid(row=9, column=0, sticky='w')
        self.pingMinAura = tk.Entry(self.webhookframe, width=55)
        self.pingMinAura.grid(row=10, column=0, columnspan=3, sticky='w')

        self.sendAuraImages = tk.IntVar()

        self.doSendAuraImages = tk.Checkbutton(self.webhookframe, text="Send Aura Images", variable=self.sendAuraImages)
        self.doSendAuraImages.grid(row=11, column=0, columnspan=3, sticky='w')

        self.toggle_webhook()
        self.toggle_inventory()

    def toggle_webhook(self):
        state = 'normal' if self.isWebhook.get() == 1 else 'disabled'
        self.webhookLink.config(state=state)
        self.webhookLabel.config(state=state)
        self.useridLabel.config(state=state)
        self.userid.config(state=state)
        self.doInventory.config(state=state)
        self.minAura.config(state=state)
        self.pingMinAura.config(state=state)
        self.minAuraLabel.config(state=state)
        self.pingMinAuraLabel.config(state=state)
        self.doSendAuraImages.config(state=state)

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

        self.isAzerty = tk.IntVar()

        self.doAzerty = tk.Checkbutton(self.general, text="AZERTY keyboard", variable=self.isAzerty, padx=28)
        self.doAzerty.grid(row=0, column=1, sticky='e')

    def create_other_frame(self):
        self.general = tk.LabelFrame(self.tab3, text="Other", padx=10, pady=5)
        self.general.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.version = tk.Label(self.general, text="Version: " + self.settings['version'])
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
        wb.open_new_tab("https://discord.gg/SHRQ44am")

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
        wb.open_new_tab("https://discord.gg/wH3XHXca")

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

