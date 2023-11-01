"""
NEXUS Voice Engine (Text-to-Speech)
Author: Syed Muhammad Qasim
Uses pyttsx3 for offline speech
"""

import pyttsx3
from .core import load_config, log

class VoiceEngine:
    def __init__(self):
        cfg = load_config()
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', cfg['voice_rate'])
        voices = self.tts.getProperty('voices')
        self.tts.setProperty('voice', voices[0].id)  # Default system voice

    def speak(self, message: str):
        """Speak text with logging"""
        log.info(f"NEXUS says: {message}")
        self.tts.say(message)
        self.tts.runAndWait()