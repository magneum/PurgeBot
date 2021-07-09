from telegram import Message, Chat, Update, Bot, User
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import Unauthorized, BadRequest, TimedOut, NetworkError, ChatMigrated, TelegramError
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async, DispatcherHandlerStop, Dispatcher
from time import sleep
from telegram.utils.helpers import escape_markdown
import datetime
import importlib
from telegram import bot
import re
import logging
import os
import sys
from loguru import logger
from time import perf_counter
from functools import wraps
from cachetools import TTLCache
from threading import RLock
from ʜʏᴘᴇ_ʀᴇᴍᴏᴠᴇʀ_ʙᴏᴛ import dispatcher
from telegram import Chat, ChatMember, ParseMode, Update
from telegram.ext import CallbackContext
import html
from typing import Dict, List
from telegram import MAX_MESSAGE_LENGTH, Bot, InlineKeyboardButton, ParseMode
from telegram.error import TelegramError
from typing import Optional, List
from telegram import Message, Chat, Update, Bot, User
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import mention_html
import os
import importlib
import time
import re
import sys
from sys import argv
from typing import Optional
from ʜʏᴘᴇ_ʀᴇᴍᴏᴠᴇʀ_ʙᴏᴛ import dispatcher,updater,FEEDBACK
from ʜᴏᴍᴇᴅɪʀ import paginate_modules
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import BadRequest,ChatMigrated,NetworkError,TelegramError,TimedOut,Unauthorized
from telegram.ext import CallbackContext,CallbackQueryHandler,CommandHandler,Filters,MessageHandler
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown
from ʜʏᴘᴇ_ʀᴇᴍᴏᴠᴇʀ_ʙᴏᴛ import dispatcher, FEEDBACK
from ʜᴏᴍᴇᴅɪʀ.chat_status import user_admin, can_delete

run_async
@user_admin
def purge(update: Update, context: CallbackContext):
    args = context.args
    msg = update.effective_message 
    if msg.reply_to_message:
        user = update.effective_user 
        chat = update.effective_chat 
        if can_delete(chat, context.bot.id):
            message_id = msg.reply_to_message.message_id
            delete_to = msg.message_id - 1
            if args and args[0].isdigit():
                new_del = message_id + int(args[0])
                if new_del < delete_to:
                    delete_to = new_del

            for m_id in range(delete_to, message_id - 1, -1):
                try:
                    context.bot.deleteMessage(chat.id, m_id)
                except BadRequest as err:
                    if err.message == "Message can't be deleted":
                        context.bot.send_message(chat.id, "Cannot delete all messages. The messages may be too old, I might "
                                                  "not have delete rights, or this might not be a supergroup.")

                    elif err.message != "Message to delete not found":
                        FEEDBACK.exception("Error while purging chat messages.")

            try:
                msg.delete()
            except BadRequest as err:
                if err.message == "Message can't be deleted":
                    context.bot.send_message(chat.id, "Cannot delete all messages. The messages may be too old, I might "
                                              "not have delete rights, or this might not be a supergroup.")

                elif err.message != "Message to delete not found":
                    FEEDBACK.exception("Error while purging chat messages.")

            context.bot.send_message(chat.id, "Purge complete.")
            return "<b>{}:</b>" \
                   "\n#PURGE" \
                   "\n<b>Admin:</b> {}" \
                   "\nPurged <code>{}</code> messages.".format(html.escape(chat.title),
                                                               mention_html(user.id, user.first_name),
                                                               delete_to - message_id)

    else:
        msg.reply_text("Reply to a message to select where to start purging from.")
    return ""



__element__ = "Purges"

PURGE_HANDLER = CommandHandler("purge", purge, filters=Filters.chat_type.groups, pass_args=True)
dispatcher.add_handler(PURGE_HANDLER)
