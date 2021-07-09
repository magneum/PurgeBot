from ʜʏᴘᴇ_ʀᴇᴍᴏᴠᴇʀ_ʙᴏᴛ.config import Development as Config
import telegram.ext as bacon
from loguru import logger
import logging

logging.basicConfig(level=logging.INFO)
FEEDBACK = logging.getLogger(__name__)


TOKEN = Config.TOKEN
LOAD = Config.LOAD
API_ID = Config.API_ID
API_HASH = Config.API_HASH
WORKERS = Config.WORKERS
    
updater = bacon.Updater(TOKEN, workers=WORKERS)
dispatcher = updater.dispatcher