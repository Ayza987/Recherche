from dotenv import load_dotenv
import os

load_dotenv()

MASTER_1_IP = os.getenv("MASTER_1_IP")
MASTER_2_IP = os.getenv("MASTER_2_IP")

DATABASE_URL = os.getenv("DATABASE_URL")