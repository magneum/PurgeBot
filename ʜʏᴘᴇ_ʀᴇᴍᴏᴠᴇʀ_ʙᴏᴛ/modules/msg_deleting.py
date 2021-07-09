from Import import *
from ʜʏᴘᴇ_ʀᴇᴍᴏᴠᴇʀ_ʙᴏᴛ import dispatcher, FEEDBACK
from MISCL.chat_status import user_admin, can_delete

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
