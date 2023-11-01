"""
NEXUS Virtual Assistant - Final Year Project 2023
Author: Syed Muhammad Qasim
Date: November 2023
A voice-controlled Windows assistant with web, media, system, and weather control.
"""

import sys
from nexus.listener import VoiceListener
from nexus.speaker import VoiceEngine
from nexus.commander import execute_command
from nexus.core import load_config, log

# Load configuration
cfg = load_config()
listener = VoiceListener()
speaker = VoiceEngine()

def startup_greeting():
    speaker.speak("NEXUS online. Say 'hey nexus' to activate.")

def main_loop():
    startup_greeting()
    wake_phrase = cfg["wake_word"]
    
    while True:
        command = listener.capture_voice(timeout=3)
        if not command:
            continue
            
        if wake_phrase in command:
            speaker.speak("Listening, sir.")
            user_cmd = listener.capture_voice(timeout=6)
            if user_cmd:
                response = execute_command(user_cmd)
                if response:
                    speaker.speak(response)
                    
        elif "exit" in command or "quit" in command or "goodbye" in command:
            speaker.speak("NEXUS shutting down. Goodbye, sir.")
            break

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        speaker.speak("Emergency shutdown initiated.")
        sys.exit(0)