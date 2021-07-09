from ɢᴏᴛᴄʜᴀ import *
from ʜʏᴘᴇ_ʀᴇᴍᴏᴠᴇʀ_ʙᴏᴛ.config import Development as Config




TOKEN = Config.TOKEN
LOAD = Config.LOAD
API_ID = Config.API_ID
API_HASH = Config.API_HASH
WORKERS = Config.WORKERS
    
updater = tg.Updater(TOKEN, workers=WORKERS)
dispatcher = updater.dispatcher

