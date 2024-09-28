import logging  

from pyrogram import Client 

from telegram.ext import Application
from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger("pyrate_limiter").setLevel(logging.ERROR)
LOGGER = logging.getLogger(name)

OWNER_ID = "7526369190"
sudo_users = ["6961287189", "7526369190", "5920352309"]
GROUP_ID = "-1002119873436"
TOKEN = "7367511450:AAFb78v-duwLXS0IZraAU33CEPxdg5SVCs0"
mongo_url = "mongodb+srv://tiwarireeta004:peqxLEd36RAg7ors@cluster0.furypd3.mongodb.net/?retryWrites=true&w=majority"
PHOTO_URL = ["https://telegra.ph/file/a17bbdf36197b0f0eb2c1.jpg", "https://telegra.ph/file/4754711cd88be32baf5b4.jpg", "https://telegra.ph/file/46b1151c6088fabc62250.jpg", "https://telegra.ph/file/4ed692d4e678216f87083.jpg"]
SUPPORT_CHAT = "waifexanime"
UPDATE_CHAT = "dynamic_gangs"
BOT_USERNAME = "Collectionwaife_bot"
CHARA_CHANNEL_ID = "-1002174533790"
api_id = "23255238"
api_hash = "009e3d8c1bdc89d5387cdd8fd182ec15"

application = Application.builder().token(TOKEN).build()
Grabberu = Client("Grabber", api_id, api_hash, bot_token=TOKEN)
client = AsyncIOMotorClient(mongo_url)
db = client['Character_catcher']
collection = db['anime_characters']
user_totals_collection = db['user_totals']
user_collection = db["user_collection"]
group_user_totals_collection = db['group_user_total']
top_global_groups_collection = db['top_global_groups']
