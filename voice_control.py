import speech_recognition as sr
import pyttsx3
import pyautogui
import keyboard
import os
import webbrowser
import time
import threading
from datetime import datetime
from tkinter import *
from tkinter import scrolledtext
from fuzzywuzzy import fuzz
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import shutil
import subprocess
import psutil
import requests

# ------------------ Voice Engine ------------------ #
def speak(text):
    """Non-blocking speech function"""
    def _speak():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 170)
            engine.setProperty('volume', 1.0)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
            del engine
        except Exception as e:
            print(f"Speech error: {e}")
    
    update_status(f" {text}")
    threading.Thread(target=_speak, daemon=True).start()

# ------------------ Volume Control ------------------ #
volume = None
try:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    print("✓ Volume control initialized")
except Exception as e:
    print(f"⚠ Volume control unavailable: {e}")
    volume = None

def set_volume(level):
    """Set system volume (0.0 to 1.0)"""
    try:
        if volume:
            volume.SetMasterVolumeLevelScalar(level, None)
            return True
        else:
            current_vol = 0.5
            if level > current_vol:
                for _ in range(5):
                    keyboard.press_and_release('volume up')
                    time.sleep(0.05)
            elif level < current_vol:
                for _ in range(5):
                    keyboard.press_and_release('volume down')
                    time.sleep(0.05)
            return True
    except Exception as e:
        print(f"Volume error: {e}")
        return False

# ------------------ GUI ------------------ #
root = Tk()
root.title("AI Voice Assistant")
root.geometry("900x650")
root.configure(bg='#0a0e27')
root.resizable(False, False)

# Gradient-like header with animated effect
header_frame = Frame(root, bg='#6366f1', height=100)
header_frame.pack(fill=X)
header_frame.pack_propagate(False)

# Title with modern font
title_label = Label(
    header_frame, 
    text="🎙️ AI VOICE ASSISTANT",
    font=("Segoe UI", 28, "bold"),
    bg='#6366f1',
    fg='white'
)
title_label.pack(pady=10)

subtitle_label = Label(
    header_frame,
    text='Say "Computer" or "Assistant" to activate • Semester Project 2025',
    font=("Segoe UI", 10),
    bg='#6366f1',
    fg='#e0e7ff'
)
subtitle_label.pack()

# Main container with cards
main_frame = Frame(root, bg='#0a0e27')
main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

# Left panel - Status and Controls
left_panel = Frame(main_frame, bg='#1e293b', relief=FLAT, bd=0)
left_panel.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

# Status card
status_card = Frame(left_panel, bg='#1e293b', relief=FLAT)
status_card.pack(fill=X, pady=(0, 15))

status_title = Label(
    status_card,
    text="STATUS",
    font=("Segoe UI", 11, "bold"),
    bg='#1e293b',
    fg='#94a3b8',
    anchor='w'
)
status_title.pack(fill=X, padx=15, pady=(15, 5))

# Status indicator with animation
status_frame = Frame(status_card, bg='#0f172a', relief=FLAT)
status_frame.pack(fill=X, padx=15, pady=(0, 15))

status_dot = Label(
    status_frame,
    text="●",
    font=("Arial", 20),
    bg='#0f172a',
    fg='#10b981'
)
status_dot.pack(side=LEFT, padx=(10, 5), pady=10)

status_var = StringVar()
status_var.set("Ready to listen...")

status_label = Label(
    status_frame,
    textvariable=status_var,
    font=("Segoe UI", 12),
    bg='#0f172a',
    fg='#e2e8f0',
    anchor='w'
)
status_label.pack(side=LEFT, fill=X, expand=True, pady=10, padx=(0, 10))

# Quick commands card
commands_card = Frame(left_panel, bg='#1e293b', relief=FLAT)
commands_card.pack(fill=BOTH, expand=True)

commands_title = Label(
    commands_card,
    text="QUICK COMMANDS",
    font=("Segoe UI", 11, "bold"),
    bg='#1e293b',
    fg='#94a3b8',
    anchor='w'
)
commands_title.pack(fill=X, padx=15, pady=(15, 10))

commands_scroll = Frame(commands_card, bg='#0f172a')
commands_scroll.pack(fill=BOTH, expand=True, padx=15, pady=(0, 15))

quick_commands = [
    ("🕐", "What time", "Get current time"),
    ("📅", "What date", "Get today's date"),
    ("📝", "Open Notepad", "Launch notepad"),
    ("🧮", "Open Calculator", "Launch calculator"),
    ("🌐", "Open Chrome", "Launch browser"),
    ("🔊", "Volume up/down", "Control volume"),
    ("📸", "Screenshot", "Take screenshot"),
    ("🎵", "Play/Pause", "Media control"),
    ("🔒", "Lock computer", "Lock screen"),
    ("❌", "Close window", "Close active window"),
]

for icon, cmd, desc in quick_commands:
    cmd_frame = Frame(commands_scroll, bg='#1e293b', relief=FLAT)
    cmd_frame.pack(fill=X, pady=3, padx=5)
    
    icon_label = Label(cmd_frame, text=icon, font=("Segoe UI", 12), bg='#1e293b', fg='#6366f1', width=3)
    icon_label.pack(side=LEFT, padx=(5, 10))
    
    text_frame = Frame(cmd_frame, bg='#1e293b')
    text_frame.pack(side=LEFT, fill=X, expand=True)
    
    Label(text_frame, text=cmd, font=("Segoe UI", 10, "bold"), bg='#1e293b', fg='#e2e8f0', anchor='w').pack(fill=X)
    Label(text_frame, text=desc, font=("Segoe UI", 8), bg='#1e293b', fg='#64748b', anchor='w').pack(fill=X)

# Right panel - Activity Log
right_panel = Frame(main_frame, bg='#1e293b', relief=FLAT, bd=0)
right_panel.pack(side=RIGHT, fill=BOTH, expand=True)

log_title = Label(
    right_panel,
    text="ACTIVITY LOG",
    font=("Segoe UI", 11, "bold"),
    bg='#1e293b',
    fg='#94a3b8',
    anchor='w'
)
log_title.pack(fill=X, padx=15, pady=(15, 10))

# Log box with custom styling
log_frame = Frame(right_panel, bg='#0f172a', relief=FLAT)
log_frame.pack(fill=BOTH, expand=True, padx=15, pady=(0, 15))

log_box = scrolledtext.ScrolledText(
    log_frame,
    bg='#0f172a',
    fg='#94a3b8',
    font=("Consolas", 10),
    wrap=WORD,
    relief=FLAT,
    borderwidth=0,
    insertbackground='#6366f1',
    selectbackground='#6366f1',
    selectforeground='white'
)
log_box.pack(fill=BOTH, expand=True, padx=2, pady=2)

# Configure text tags for colored output
log_box.tag_config('user', foreground='#60a5fa')
log_box.tag_config('assistant', foreground='#34d399')
log_box.tag_config('system', foreground='#a78bfa')
log_box.tag_config('error', foreground='#f87171')
log_box.tag_config('time', foreground='#64748b')

def update_status(text):
    """Update status and log with color coding"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # Update status label
    if "Listening" in text:
        status_var.set("🎤 Listening...")
        status_dot.config(fg='#3b82f6')  # Blue
    elif "Processing" in text:
        status_var.set("⚙️ Processing...")
        status_dot.config(fg='#f59e0b')  # Orange
    elif "Assistant:" in text or "🤖" in text:
        status_var.set("💬 Speaking...")
        status_dot.config(fg='#10b981')  # Green
    elif "error" in text.lower() or "❌" in text:
        status_var.set("⚠️ Error occurred")
        status_dot.config(fg='#ef4444')  # Red
    else:
        status_var.set("✓ Ready")
        status_dot.config(fg='#10b981')  # Green
    
    # Add to log with colors
    log_box.insert(END, f"[{timestamp}] ", 'time')
    
    if "👤" in text or "You said:" in text:
        log_box.insert(END, f"{text}\n", 'user')
    elif "🤖" in text or "Assistant:" in text:
        log_box.insert(END, f"{text}\n", 'assistant')
    elif "❌" in text or "error" in text.lower():
        log_box.insert(END, f"{text}\n", 'error')
    else:
        log_box.insert(END, f"{text}\n", 'system')
    
    log_box.see(END)
    root.update()

# Footer with gradient effect
footer_frame = Frame(root, bg='#1e293b', height=50)
footer_frame.pack(fill=X, side=BOTTOM)
footer_frame.pack_propagate(False)

footer_text = Label(
    footer_frame,
    text="Tip: Speak clearly and wait for the beep • Press Ctrl+C in terminal to stop",
    font=("Segoe UI", 9),
    bg='#1e293b',
    fg='#94a3b8'
)
footer_text.pack(expand=True)

# ------------------ Speech Recognizer ------------------ #
r = sr.Recognizer()
r.energy_threshold = 300
r.dynamic_energy_threshold = True
r.pause_threshold = 0.8

def take_command(timeout=5, phrase_time_limit=5):
    """Listen and recognize speech"""
    with sr.Microphone() as source:
        update_status("👂 Listening...")
        try:
            r.adjust_for_ambient_noise(source, duration=0.3)
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            
            update_status("🔄 Processing...")
            command = r.recognize_google(audio).lower()
            update_status(f"👤 You said: {command}")
            print(f"Recognized: '{command}'")
            return command
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            update_status("❌ Could not understand")
            return ""
        except sr.RequestError as e:
            update_status("❌ Network error")
            print(f"Request error: {e}")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""

# ------------------ Command Handler ------------------ #
def handle_command(command):
    """Process voice commands"""
    command = command.lower().strip()
    print(f"🔍 Processing: '{command}'")
    
    def match(keywords):
        """Enhanced matching with priority"""
        # First check exact substring match
        for keyword in keywords:
            if keyword in command:
                print(f"✓ Exact match: '{keyword}'")
                return True
        # Then fuzzy match
        for keyword in keywords:
            if fuzz.partial_ratio(command, keyword) > 75:
                print(f"✓ Fuzzy match: '{keyword}'")
                return True
        return False

    # --- APPLICATION LAUNCHERS ---
    if match(["notepad"]) and not match(["close"]):
        try:
            os.startfile("notepad.exe")
            speak("Opening Notepad")
        except Exception as e:
            speak("Could not open Notepad")
    
    elif match(["chrome", "browser"]) and not match(["close"]):
        try:
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
            opened = False
            for path in chrome_paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    speak("Opening Chrome")
                    opened = True
                    break
            if not opened:
                webbrowser.open('http://www.google.com')
                speak("Opening browser")
        except Exception as e:
            speak("Could not open Chrome")
    
    elif match(["calculator", "calc"]) and not match(["close"]):
        try:
            os.startfile("calc.exe")
            speak("Opening Calculator")
        except Exception as e:
            speak("Could not open Calculator")
    
    elif match(["word", "microsoft word"]):
        word_paths = [
            r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
            r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE"
        ]
        opened = False
        for path in word_paths:
            if os.path.exists(path):
                os.startfile(path)
                speak("Opening Microsoft Word")
                opened = True
                break
        if not opened:
            speak("Word not found")
    
    elif match(["excel"]):
        excel_paths = [
            r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
            r"C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE"
        ]
        opened = False
        for path in excel_paths:
            if os.path.exists(path):
                os.startfile(path)
                speak("Opening Excel")
                opened = True
                break
        if not opened:
            speak("Excel not found")
    
    elif match(["powerpoint", "presentation"]):
        ppt_paths = [
            r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
            r"C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE"
        ]
        opened = False
        for path in ppt_paths:
            if os.path.exists(path):
                os.startfile(path)
                speak("Opening PowerPoint")
                opened = True
                break
        if not opened:
            speak("PowerPoint not found")
    
    elif match(["file explorer", "explorer", "files"]):
        os.startfile("explorer.exe")
        speak("Opening File Explorer")
    
    elif match(["task manager"]):
        os.system("taskmgr")
        speak("Opening Task Manager")
    
    elif match(["control panel"]):
        os.system("control")
        speak("Opening Control Panel")
    
    elif match(["settings", "system settings"]):
        os.system("start ms-settings:")
        speak("Opening Settings")
    
    elif match(["paint"]):
        os.startfile("mspaint.exe")
        speak("Opening Paint")
    
    # --- WINDOW MANAGEMENT ---
    elif match(["close window", "close this", "close app"]):
        pyautogui.hotkey("alt", "f4")
        speak("Closing window")
    
    elif match(["switch window", "alt tab", "next window"]):
        pyautogui.hotkey("alt", "tab")
        speak("Switching window")
    
    elif match(["minimize window", "minimize"]):
        pyautogui.hotkey("win", "down")
        speak("Minimizing")
    
    elif match(["maximize window", "maximize"]):
        pyautogui.hotkey("win", "up")
        speak("Maximizing")
    
    elif match(["show desktop", "desktop"]):
        pyautogui.hotkey("win", "d")
        speak("Showing desktop")
    
    # --- SCROLLING ---
    elif match(["scroll down", "go down"]):
        pyautogui.scroll(-500)
        speak("Scrolling down")
    
    elif match(["scroll up", "go up"]):
        pyautogui.scroll(500)
        speak("Scrolling up")
    
    elif match(["page down"]):
        pyautogui.press("pagedown")
        speak("Page down")
    
    elif match(["page up"]):
        pyautogui.press("pageup")
        speak("Page up")
    
    # --- VOLUME CONTROL ---
    elif match(["volume up", "increase volume", "louder", "raise volume"]):
        try:
            if volume:
                current = volume.GetMasterVolumeLevelScalar()
                new_vol = min(current + 0.15, 1.0)
                set_volume(new_vol)
                speak(f"Volume {int(new_vol*100)} percent")
            else:
                for _ in range(3):
                    keyboard.press_and_release('volume up')
                    time.sleep(0.1)
                speak("Volume increased")
        except Exception as e:
            speak("Volume control error")
    
    elif match(["volume down", "decrease volume", "quieter", "lower volume"]):
        try:
            if volume:
                current = volume.GetMasterVolumeLevelScalar()
                new_vol = max(current - 0.15, 0.0)
                set_volume(new_vol)
                speak(f"Volume {int(new_vol*100)} percent")
            else:
                for _ in range(3):
                    keyboard.press_and_release('volume down')
                    time.sleep(0.1)
                speak("Volume decreased")
        except Exception as e:
            speak("Volume control error")
    
    elif match(["mute", "silence"]):
        try:
            if volume:
                set_volume(0)
                speak("Muted")
            else:
                keyboard.press_and_release('volume mute')
                speak("Muted")
        except Exception as e:
            speak("Mute error")
    
    elif match(["unmute", "sound on"]):
        try:
            if volume:
                set_volume(0.5)
                speak("Unmuted")
            else:
                keyboard.press_and_release('volume mute')
                speak("Unmuted")
        except Exception as e:
            speak("Unmute error")
    
    # --- MEDIA CONTROLS ---
    elif match(["play", "pause", "play pause"]):
        keyboard.press_and_release('play/pause media')
        speak("Toggled")
    
    elif match(["next track", "next song", "skip"]):
        keyboard.press_and_release('next track')
        speak("Next track")
    
    elif match(["previous track", "previous song", "back"]):
        keyboard.press_and_release('previous track')
        speak("Previous track")
    
    elif match(["stop media", "stop playing"]):
        keyboard.press_and_release('stop media')
        speak("Stopped")
    
    # --- SCREENSHOT ---
    elif match(["screenshot", "capture screen", "take screenshot"]):
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        speak("Screenshot saved")
    
    # --- TYPING ---
    elif "type" in command and "youtube" not in command:
        text = command.replace("type", "").strip()
        if text:
            time.sleep(0.5)
            pyautogui.write(text, interval=0.05)
            speak("Typed")
        else:
            speak("Nothing to type")
    
    elif match(["press enter", "enter"]):
        pyautogui.press("enter")
        speak("Enter")
    
    elif match(["press space", "space"]):
        pyautogui.press("space")
        speak("Space")
    
    elif match(["press tab", "tab"]):
        pyautogui.press("tab")
        speak("Tab")
    
    elif match(["press escape", "escape"]):
        pyautogui.press("esc")
        speak("Escape")
    
    elif match(["copy"]):
        pyautogui.hotkey("ctrl", "c")
        speak("Copied")
    
    elif match(["paste"]):
        pyautogui.hotkey("ctrl", "v")
        speak("Pasted")
    
    elif match(["cut"]):
        pyautogui.hotkey("ctrl", "x")
        speak("Cut")
    
    elif match(["undo"]):
        pyautogui.hotkey("ctrl", "z")
        speak("Undone")
    
    elif match(["redo"]):
        pyautogui.hotkey("ctrl", "y")
        speak("Redone")
    
    elif match(["select all"]):
        pyautogui.hotkey("ctrl", "a")
        speak("Selected all")
    
    elif match(["save"]):
        pyautogui.hotkey("ctrl", "s")
        speak("Saved")
    
    # --- WEB SEARCH & SITES ---
    elif "search google" in command or "google search" in command:
        query = command.replace("search google", "").replace("google search", "").replace("google", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"Searching for {query}")
        else:
            speak("What should I search?")
    
    elif "search youtube" in command or "youtube search" in command:
        query = command.replace("search youtube", "").replace("youtube search", "").replace("youtube", "").strip()
        if query:
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            speak(f"Searching YouTube for {query}")
        else:
            speak("What should I search?")
    
    elif match(["open youtube"]) and "search" not in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
    
    elif match(["open google"]) and "search" not in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")
    
    elif match(["open gmail", "gmail", "email"]):
        webbrowser.open("https://mail.google.com")
        speak("Opening Gmail")
    
    elif match(["open facebook", "go to facebook"]) and "calculator" not in command:
        webbrowser.open("https://www.facebook.com")
        speak("Opening Facebook")
    
    elif match(["open twitter", "go to twitter"]):
        webbrowser.open("https://www.twitter.com")
        speak("Opening Twitter")
    
    elif match(["open instagram", "go to instagram"]):
        webbrowser.open("https://www.instagram.com")
        speak("Opening Instagram")
    
    # --- SYSTEM INFO ---
    elif match(["what time", "tell time", "current time", "time"]) and "youtube" not in command:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")
    
    elif match(["what date", "today date", "current date", "date"]):
        current_date = datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {current_date}")
    
    elif match(["battery", "battery status", "battery level"]):
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = "plugged in" if battery.power_plugged else "not plugged in"
            speak(f"Battery is at {percent} percent and {plugged}")
        else:
            speak("Battery info not available")
    
    elif match(["cpu usage", "processor usage"]):
        cpu = psutil.cpu_percent(interval=1)
        speak(f"CPU usage is {cpu} percent")
    
    elif match(["memory usage", "ram usage"]):
        memory = psutil.virtual_memory()
        speak(f"Memory usage is {memory.percent} percent")
    
    # --- JOKES ---
    elif match(["tell joke", "joke", "make me laugh"]):
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why did the computer go to therapy? It had too many bytes of emotional baggage!",
            "What do you call a computer that sings? A Dell!",
            "Why was the computer cold? It left its Windows open!",
            "How do you comfort a JavaScript bug? You console it!"
        ]
        import random
        speak(random.choice(jokes))
    
    # --- SYSTEM CONTROL ---
    elif match(["lock computer", "lock screen", "lock"]):
        speak("Locking computer")
        os.system("rundll32.exe user32.dll,LockWorkStation")
    
    elif match(["sleep", "sleep mode"]):
        speak("Going to sleep")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    
    elif match(["shutdown", "shut down", "power off"]):
        speak("Shutting down in 10 seconds")
        time.sleep(3)
        os.system("shutdown /s /t 10")
    
    elif match(["restart", "reboot"]):
        speak("Restarting in 10 seconds")
        time.sleep(3)
        os.system("shutdown /r /t 10")
    
    elif match(["cancel shutdown", "cancel", "stop shutdown"]):
        os.system("shutdown /a")
        speak("Cancelled")
    
    # --- HELP ---
    elif match(["help", "what can you do", "commands"]):
        speak("I can open apps, control volume, search the web, manage windows, tell time, check battery, and much more")
    
    # --- EXIT ---
    elif match(["stop listening", "exit", "quit", "goodbye", "bye"]):
        speak("Goodbye, Take care, Have a nice day!")
        time.sleep(1)
        root.quit()
        os._exit(0)
    
    else:
        print(f"No match for: '{command}'")
        update_status(f"Unknown: {command}")
        speak("Command not recognized")

# ------------------ Test Mode ------------------ #
def test_microphone():
    """Test microphone"""
    try:
        with sr.Microphone() as source:
            print("Microphone detected")
            r.adjust_for_ambient_noise(source, duration=1)
            print(f"✓ Energy threshold: {r.energy_threshold}")
            return True
    except Exception as e:
        print(f"Microphone error: {e}")
        return False

# ------------------ Background Listening ------------------ #
listening = True

def assistant_loop():
    """Main loop"""
    speak("Voice assistant activated")
    update_status("Ready to assist")
    
    while listening:
        try:
            command = take_command(timeout=10)
            
            if command == "":
                time.sleep(0.5)
                continue
            
            # Check for activation words
            if any(word in command for word in ["computer", "assistant", "hey"]):
                speak("Yes")
                time.sleep(0.3)
                command = take_command()
                if command:
                    handle_command(command)
            else:
                handle_command(command)
                
            time.sleep(0.5)  # Prevent rapid looping
        
        except Exception as e:
            print(f"Loop error: {e}")
            time.sleep(1)

# ------------------ Run ------------------ #
print("\n=== AI Voice Assistant ===")
if test_microphone():
    print("✓ System ready\n")
else:
    print("⚠ Warning: Mic issues detected\n")

update_status("Initializing...")
threading.Thread(target=assistant_loop, daemon=True).start()
root.mainloop()