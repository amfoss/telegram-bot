#!/usr/bin/python3.6
import logging
import os
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from decouple import config


from leave_record import LeaveRecord

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TYPE, REASON = range(2)


def start(bot, context):
    user = bot.message.from_user
    bot.message.reply_text("Hi @" + user['username'] + "!\n I am chowkidar of amFOSS.")
    bot.message.reply_text("/help - for more details")

def help(bot, context):
    bot.message.reply_text(
        "This bot will help you with all the functionalities.\n\n" 
        "/leaverecord - register your leave record"
    )

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    TOKEN = config('BOT_TOKEN')
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    l = LeaveRecord
    leave_handler = ConversationHandler(
        entry_points=[CommandHandler('leaverecord', l.getType)],

        states={
            TYPE: [MessageHandler(Filters.regex('^(Health|Family/Home|Tired|Academics|Duty)$'), l.getReason)],
            REASON: [MessageHandler(Filters.text, l.registerLeave)]
        },

        fallbacks=[CommandHandler('cancel', l.cancel)]
    )

    dp.add_handler(leave_handler)
    dp.add_error_handler(error)
    HOST = config('HOST')
    PORT = config('PORT')
    KEY = config('KEY')
    CERT = config('CERT')
    updater.start_webhook(listen='0.0.0.0',
                      port=PORT,
                      url_path=TOKEN,
                      key=KEY,
                      cert=CERT,
                      webhook_url=HOST+':'+PORT+'/'+TOKEN)
    # updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
