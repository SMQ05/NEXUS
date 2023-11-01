"""
NEXUS Command Center
Author: Syed Muhammad Qasim
Handles all voice commands with personalized logic
"""

import os, subprocess, webbrowser, pyautogui, psutil, requests
from .core import load_config, log

cfg = load_config()

# === Media Control Helper ===
def _terminate_media_apps():
    for proc in psutil.process_iter(['name']):
        name = proc.info['name'].lower()
        if name in {"wmplayer.exe", "vlc.exe", "mpc-hc64.exe", "chrome.exe", "firefox.exe"}:
            proc.terminate()
            log.info(f"Terminated: {name}")

# === Command Functions ===
def google_search(query: str):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Searching Google for {query}"

def launch_file(filename: str):
    full_path = os.path.abspath(filename)
    if os.path.exists(full_path):
        os.startfile(full_path)
        return f"Launching {filename}"
    else:
        return f"File not found: {filename}"

def play_local_media(file: str, media_type: str = "music"):
    folder = cfg["media_folder"] if media_type == "music" else cfg["video_folder"]
    path = os.path.join(folder, file)
    if os.path.exists(path):
        os.startfile(path)
        return f"Playing {media_type}: {file}"
    else:
        return f"{media_type.capitalize()} not found"

def stop_all_media():
    _terminate_media_apps()
    return "All media stopped"

def refresh_active_window():
    pyautogui.hotkey('ctrl', 'r')
    return "Page refreshed"

def initiate_shutdown():
    subprocess.run(["shutdown", "/s", "/t", "10"])
    return "System shutdown in 10 seconds"

def navigate_to_website(site: str):
    sites = {
        "google": "https://google.com",
        "youtube": "https://youtube.com",
        "github": "https://github.com",
        "passau": "https://www.uni-passau.de"
    }
    url = sites.get(site.lower(), f"https://www.{site}.com")
    webbrowser.open(url)
    return f"Opening {site}"

def play_youtube_track(song: str):
    query = song.replace(' ', '+') + "+official+music+video"
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    return f"Playing {song} on YouTube"

def fetch_weather_data(location: str):
    key = cfg.get("openweather_api_key")
    if not key or key == "YOUR_API_KEY_HERE":
        return "Weather API key not configured in config.yaml"
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={key}"
    try:
        resp = requests.get(url, timeout=6)
        resp.raise_for_status()
        data = resp.json()
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        desc = data["weather"][0]["description"]
        return f"{location.capitalize()}: {desc}, {temp}°C, feels like {feels}°C, humidity {humidity}%."
    except requests.RequestException as e:
        log.error(f"Weather fetch failed: {e}")
        return "Weather service unavailable. Check internet or API key."

# === Command Router ===
COMMAND_TRIGGERS = {
    "search": google_search,
    "open file": launch_file,
    "play video": lambda x: play_local_media(x, "video"),
    "play music": lambda x: play_local_media(x, "music"),
    "stop music": lambda _: stop_all_media(),
    "stop video": lambda _: stop_all_media(),
    "refresh": lambda _: refresh_active_window(),
    "shutdown": lambda _: initiate_shutdown(),
    "go to": navigate_to_website,
    "play on youtube": play_youtube_track,
    "weather in": fetch_weather_data,
}

def execute_command(user_input: str):
    """Route command to correct handler"""
    cmd = user_input.strip().lower()
    for trigger, action in COMMAND_TRIGGERS.items():
        if cmd.startswith(trigger):
            argument = cmd[len(trigger):].strip()
            return action(argument)
    return "Command not recognized. Try 'weather in berlin' or 'play music song.mp3'."
