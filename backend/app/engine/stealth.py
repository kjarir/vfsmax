import random
from typing import Dict, Any


class FingerprintProfile:
    def __init__(self, user_agent: str, viewport: Dict[str, int], device_memory: int, hardware_concurrency: int):
        self.user_agent = user_agent
        self.viewport = viewport
        self.device_memory = device_memory
        self.hardware_concurrency = hardware_concurrency


# A few example profiles to start with
BROWSER_FINGERPRINTS = [
    FingerprintProfile(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        {"width": 1920, "height": 1080},
        8,
        8,
    ),
    FingerprintProfile(
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        {"width": 1440, "height": 900},
        16,
        10,
    ),
    FingerprintProfile(
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        {"width": 1366, "height": 768},
        4,
        4,
    ),
]


def get_random_profile() -> FingerprintProfile:
    return random.choice(BROWSER_FINGERPRINTS)
