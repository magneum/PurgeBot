import logging
import os
import sys
import telegram.ext as tg
from loguru import logger
from pyrogram import Client

class InterceptHandler(logging.Handler):
    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR",
        logging.WARNING: "WARNING",
        logging.INFO: "INFO",
        logging.DEBUG: "DEBUG"
    }

    def _get_level(self, record):
        return self.LEVELS_MAP.get(record.levelno, record.levelno)

    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info, ansi=True, lazy=True)
        logger_opt.log(self._get_level(record), record.getMessage())


logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
FEEDBACK = logging.getLogger(__name__)

from ʜʏᴘᴇ_ʀᴇᴍᴏᴠᴇʀ_ʙᴏᴛ.config import Development as Config
TOKEN = Config.TOKEN
LOAD = Config.LOAD
API_ID = Config.API_ID
API_HASH = Config.API_HASH
WORKERS = Config.WORKERS
    
updater = tg.Updater(TOKEN, workers=WORKERS)
dispatcher = updater.dispatcher

