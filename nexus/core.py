"""
NEXUS Core Utilities
Author: Syed Muhammad Qasim
Handles config, logging, paths
"""

import logging, os, yaml, pathlib

# Setup logging with file + console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("nexus.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

# Config path
CONFIG_FILE = pathlib.Path(__file__).parent.parent / "config.yaml"

DEFAULT_CONFIG = {
    "media_folder": str(pathlib.Path.home() / "Music"),
    "video_folder": str(pathlib.Path.home() / "Videos"),
    "voice_rate": 165,
    "wake_word": "hey nexus",
    "openweather_api_key": ""
}

def load_config() -> dict:
    """Load user config or return defaults"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            user_cfg = yaml.safe_load(f) or {}
        config = {**DEFAULT_CONFIG, **user_cfg}
        log.info("Configuration loaded from config.yaml")
    else:
        config = DEFAULT_CONFIG.copy()
        log.warning("config.yaml not found. Using defaults.")
    return config