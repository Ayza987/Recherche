import os
from dotenv import load_dotenv

load_dotenv()

MASTER_IP = os.getenv(
    "MASTER_IP",
    "192.168.10.10"
)

MASTER_PORT = int(
    os.getenv(
        "MASTER_PORT",
        80
    )
)

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

COLLECTION_INTERVAL = int(
    os.getenv(
        "COLLECTION_INTERVAL",
        2
    )
)

CONNECT_TIMEOUT = 3

READ_TIMEOUT = 5

USERNAME = None

PASSWORD = None

NUM_PORTS = 8

HEALTH_ISDU_PARAMS = [

    {
        "name": "serial_number",
        "index": 21,
        "subindex": 0
    },

    {
        "name": "firmware",
        "index": 23,
        "subindex": 0
    },

    {
        "name": "hardware",
        "index": 24,
        "subindex": 0
    },

    {
        "name": "operating_hours",
        "index": 36,
        "subindex": 0
    },

    {
        "name": "power_on_cycles",
        "index": 37,
        "subindex": 0
    }
]