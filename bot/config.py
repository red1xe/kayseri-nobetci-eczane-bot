import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN= os.getenv("BOT_TOKEN")
PHARMACIES_DATA_URL = os.getenv("PHARMACIES_DATA_URL")