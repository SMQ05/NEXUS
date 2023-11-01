"""
NEXUS Voice Listener (Speech-to-Text)
Author: Syed Muhammad Qasim
Uses Google Speech Recognition (online)
"""

import speech_recognition as sr
from .core import log

class VoiceListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        with self.microphone as src:
            self.recognizer.adjust_for_ambient_noise(src)
        log.info("NEXUS microphone initialized")

    def capture_voice(self, timeout=5) -> str:
        """Listen and return transcribed text"""
        try:
            with self.microphone as src:
                log.info("NEXUS listening...")
                audio = self.recognizer.listen(src, timeout=timeout, phrase_time_limit=6)
            text = self.recognizer.recognize_google(audio).lower()
            log.info(f"User said: {text}")
            return text
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            log.warning("NEXUS could not understand audio")
            return ""
        except sr.RequestError as e:
            log.error(f"Speech service error: {e}")
            return ""