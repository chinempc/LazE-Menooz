import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
#from app.Schemas.schemas import serials

load_dotenv(".env-local")
uri = os.getenv("MONGO_URI")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())

laze_menus_db = client.laze
laze = laze_menus_db.laze

# Menus DB
menu_db = client.menu_data

# Menu Collections
weekly_menu = laze.weekly_menu
daily_menu = laze.daily_menu
meal_period = laze.meal_period

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
