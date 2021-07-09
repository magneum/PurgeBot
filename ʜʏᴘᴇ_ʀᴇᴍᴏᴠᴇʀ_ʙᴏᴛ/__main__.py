from ɢᴏᴛᴄʜᴀ import *
from ʜʏᴘᴇ_ʀᴇᴍᴏᴠᴇʀ_ʙᴏᴛ import dispatcher, updater, FEEDBACK
from ʜʏᴘᴇ_ʀᴇᴍᴏᴠᴇʀ_ʙᴏᴛ.modules import ALL_MODULES
from ʜᴏᴍᴇᴅɪʀ.chat_status import is_user_admin
from ʜᴏᴍᴇᴅɪʀ.miscl import paginate_modules

PM_START_TEXT = """
You can find the list of available commands with /help.
"""

BOT_IMAGE = "https://telegra.ph/file/93612a540608640355f20.mp4"

HELP_STRINGS = """
I'm a modular group management bot with a few fun extras! Have a look at the following for an idea of some of \
the things I can help you with.
If you have any questions on how to use me, head over to @PhoenixSupport

*Main* commands available:
 - /start: start the bot
 - /help: PM's you this message.
 - /help <module name>: PM's you info about that module.
 - /donate: information about how to donate!
 - /settings:
   - in PM: will send you your settings for all supported modules.
   - in a group: will redirect you to pm, with all that chat's settings.

And the following:
"""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []

CHAT_SETTINGS = {}
USER_SETTINGS = {}

GDPR = []

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("ʜʏᴘᴇ_ʀᴇᴍᴏᴠᴇʀ_ʙᴏᴛ.modules." + module_name)
    if not hasattr(imported_module, "__element__"):
        imported_module.__element__ = imported_module.__name__
    if not imported_module.__element__.lower() in IMPORTED:
        IMPORTED[imported_module.__element__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")
    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__element__.lower()] = imported_module
    if hasattr(imported_module, "__gdpr__"):
        GDPR.append(imported_module)
    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)


def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(chat_id=chat_id,
                                text=text,
                                parse_mode=ParseMode.MARKDOWN,
                                reply_markup=keyboard)


run_async
def start(update: Update, context: CallbackContext):
    args = context.args
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
        else:
            update.effective_message.reply_animation(
                BOT_IMAGE,
                caption=PM_START_TEXT,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Add to your group.",
                                url="t.me/{}?startgroup=botstart".format(context.bot.username),
                            )
                        ]
                    ]
                ),
            )
    else:
        update.effective_message.reply_text("Yo, why'd you summon me?")


run_async
def help_button(update: Update, context: CallbackContext):
    args = context.args
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    try:
        if mod_match:
            module = mod_match.group(1)
            text = "Here is the help for the *{}* module:\n".format(HELPABLE[module].__element__) \
                   + HELPABLE[module].__help__
            query.message.edit_text(text=text,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=InlineKeyboardMarkup(
                                         [[InlineKeyboardButton(text="Back", callback_data="help_back")]]))

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(HELP_STRINGS,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=InlineKeyboardMarkup(
                                         paginate_modules(curr_page - 1, HELPABLE, "help")))

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(HELP_STRINGS,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=InlineKeyboardMarkup(
                                         paginate_modules(next_page + 1, HELPABLE, "help")))

        elif back_match:
            query.message.edit_text(text=HELP_STRINGS,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help")))
        context.bot.answer_callback_query(query.id)
    except BadRequest as excp:
        if excp.message == "Message is not modified":
            pass
        elif excp.message == "Query_id_invalid":
            pass
        elif excp.message == "Message can't be deleted":
            pass
        else:
            FEEDBACK.exception("Exception in help buttons. %s", str(query.data))


run_async
def get_help(update: Update, context: CallbackContext):
    args = context.args
    chat = update.effective_chat
    if chat.type != chat.PRIVATE:
        update.effective_message.reply_text("Contact me in PM to get the list of possible commands.",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(text="Help",
                                                                       url="t.me/{}?start=help".format(
                                                                           context.bot.username))]]))
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = "Here is the available help for the *{}* module:\n".format(HELPABLE[module].__element__) \
               + HELPABLE[module].__help__
        send_help(chat.id, text, InlineKeyboardMarkup([[InlineKeyboardButton(text="Back", callback_data="help_back")]]))

    else:
        send_help(chat.id, HELP_STRINGS)





def main():
    start_handler = CommandHandler("start", start, pass_args=True)
    help_handler = CommandHandler("help", get_help)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_")


    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(help_callback_handler)

    
    

    
FEEDBACK.info("Using long polling.")
updater.start_polling(timeout=15, read_latency=4)
FEEDBACK.info("Successfully loaded modules: " + str(ALL_MODULES))
main()
FEEDBACK.info("READY")
updater.idle()