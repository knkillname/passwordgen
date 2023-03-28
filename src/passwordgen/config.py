"""Configuration variables for passwordgen."""
from pathlib import Path

USER_DATA_DIR = Path.home() / ".passwordgen"
USER_DATA_DIR.mkdir(exist_ok=True)

RESOURCE_PATH = Path(__file__).parent / "data"
