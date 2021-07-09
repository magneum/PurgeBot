from ʜʏᴘᴇ_ʀᴇᴍᴏᴠᴇʀ_ʙᴏᴛ import dispatcher,FEEDBACK
from ʜʏᴘᴇ_ʀᴇᴍᴏᴠᴇʀ_ʙᴏᴛ import dispatcher, FEEDBACK
from ʜᴏᴍᴇᴅɪʀ.chat_status import user_admin, can_delete
from ᴋᴀᴛᴇ import * 
from FANCY import *
import asyncio

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
                        context.bot.send_message(chat.id, "—🧻••÷[ ɦʏքɛ_քʊʀɢɛ_ɮօȶ ]÷••🧻—\n\nCannot delete all messages. The messages may be too old, I might "
                                                  "not have delete rights, or this might not be a supergroup.")
                        

                    elif err.message != "Message to delete not found":
                        FEEDBACK.exception("Error while cleaning chat messages.")

            try:
                msg.delete()
            except BadRequest as err:
                if err.message == "Message can't be deleted":
                    context.bot.send_message(chat.id, "—🧻••÷[ ɦʏքɛ_քʊʀɢɛ_ɮօȶ ]÷••🧻—\n\nCannot delete all messages. The messages may be too old, I might "
                                              "not have delete rights, or this might not be a supergroup.")
                    

                elif err.message != "Message to delete not found":
                    FEEDBACK.exception("Error while cleaning chat messages.")

            context.bot.send_message(chat.id, "—🧻••÷[ ɦʏքɛ_քʊʀɢɛ_ɮօȶ ]÷••🧻—\n\nCleaning Done.")
            
            return "<b>{}:</b>" \
                   "\n#PURGE" \
                   "\n<b>Admin:</b> {}" \
                   "\nPurged <code>{}</code> messages.".format(html.escape(chat.title),
                                                               mention_html(user.id, user.first_name),
                                                               delete_to - message_id)

    else:
        msg.reply_photo(DEL_TER,"—🧻••÷[ ɦʏքɛ_քʊʀɢɛ_ɮօȶ ]÷••🧻—\n\nReply to a message to select where to start cleaning from.")
        
    return ""



__element__ = "Purge"

PURGE_HANDLER = CommandHandler("purge", purge, filters=Filters.chat_type.groups, pass_args=True)
dispatcher.add_handler(PURGE_HANDLER)
