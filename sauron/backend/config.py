import os
import pathlib
from dotenv import load_dotenv

load_dotenv()

_BASE_DIR = pathlib.Path(__file__).resolve().parent.parent  # sauron/

LOG_PATH = os.getenv("LOG_PATH", "/var/log/kern.log")
INTERFACE = os.getenv("INTERFACE", "eth0")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{_BASE_DIR / 'database' / 'ids.db'}"
)
