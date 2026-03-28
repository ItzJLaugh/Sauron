import os
from dotenv import load_dotenv

load_dotenv()

LOG_PATH = os.getenv("LOG_PATH", "/var/log/kern.log")
INTERFACE = os.getenv("INTERFACE", "eth0")
