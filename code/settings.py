from typing import Literal

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FPS = 30

NORMAL: Literal["normal"] = "normal"
DEV: Literal["dev"] = "dev"  # Use only when testing or adding new features
MODE: Literal["normal", "dev"] = DEV
