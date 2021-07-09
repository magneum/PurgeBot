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
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import BadRequest,ChatMigrated,NetworkError,TelegramError,TimedOut,Unauthorized
from telegram.ext import CallbackContext,CallbackQueryHandler,CommandHandler,Filters,MessageHandler
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def split_message(msg: str) -> List[str]:
    if len(msg) < MAX_MESSAGE_LENGTH:
        return [msg]

    lines = msg.splitlines(True)
    small_msg = ""
    result = []
    for line in lines:
        if len(small_msg) + len(line) < MAX_MESSAGE_LENGTH:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line
    else:
        # Else statement at the end of the for loop, so append the leftover string.
        result.append(small_msg)

    return result


def paginate_modules(page_n: int, module_dict: Dict, prefix, chat=None) -> List:
    if not chat:
        AWAY = sorted(
            [
                EqInlineKeyboardButton(
                    x.__element__,
                    callback_data="{}_module({})".format(
                        prefix, x.__element__.lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )
    else:
        AWAY = sorted(
            [
                EqInlineKeyboardButton(
                    x.__element__,
                    callback_data="{}_module({},{})".format(
                        prefix, chat, x.__element__.lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )

    pairs = [AWAY[i * 3 : (i + 1) * 3] for i in range((len(AWAY) + 3 - 1) // 3)]

    round_num = len(AWAY) / 3
    calc = len(AWAY) - round(round_num)
    if calc in [1, 2]:
        pairs.append((AWAY[-1],))
    return pairs


def send_to_list(
    bot: Bot, send_to: list, message: str, markdown=False, html=False
) -> None:
    if html and markdown:
        raise Exception("Can only send with either markdown or HTML!")
    for user_id in set(send_to):
        try:
            if markdown:
                bot.send_message(user_id, message, parse_mode=ParseMode.MARKDOWN)
            elif html:
                bot.send_message(user_id, message, parse_mode=ParseMode.HTML)
            else:
                bot.send_message(user_id, message)
        except TelegramError:
            pass  # ignore users who fail


def build_keyboard(buttons):
    keyb = []
    for btn in buttons:
        if btn.same_line and keyb:
            keyb[-1].append(InlineKeyboardButton(btn.name, url=btn.url))
        else:
            keyb.append([InlineKeyboardButton(btn.name, url=btn.url)])

    return keyb


def revert_buttons(buttons):
    res = ""
    for btn in buttons:
        if btn.same_line:
            res += "\n[{}](buttonurl://{}:same)".format(btn.name, btn.url)
        else:
            res += "\n[{}](buttonurl://{})".format(btn.name, btn.url)

    return res


def build_keyboard_parser(bot, chat_id, buttons):
    keyb = []
    for btn in buttons:
        if btn.url == "{rules}":
            btn.url = "http://t.me/{}?start={}".format(bot.username, chat_id)
        if btn.same_line and keyb:
            keyb[-1].append(InlineKeyboardButton(btn.name, url=btn.url))
        else:
            keyb.append([InlineKeyboardButton(btn.name, url=btn.url)])

    return keyb


def is_module_loaded(name):
    return name


def delete(delmsg, timer):
    sleep(timer)
    try:
        delmsg.delete()
    except:
        return
