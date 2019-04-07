import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

from leave_record import LeaveRecord

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TYPE, REASON = range(2)


def start(bot, context):
    user = bot.message.from_user
    bot.message.reply_text("Hi @" + user['username'] + "!\n I am amFOSS Assistant")
    bot.message.reply_text(
        "Here is what I can do for you - \n"
        "/leaverecord - register your leave record"
    )
    bot.message.reply_text("/help - for more details")


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater("<YOUR BOT TOKEN HERE>", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    l = LeaveRecord
    leave_handler = ConversationHandler(
        entry_points=[CommandHandler('leaverecord', l.getType)],

        states={
            TYPE: [RegexHandler('^(Health|Family/Home|Tired|Academics|Duty)$', l.getReason)],
            REASON: [MessageHandler(Filters.text, l.registerLeave)]
        },

        fallbacks=[CommandHandler('cancel', l.cancel)]
    )

    dp.add_handler(leave_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
