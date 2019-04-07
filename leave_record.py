from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

TYPE, REASON = range(2)


class LeaveRecord:

    def getType(bot, context):
        reply_keyboard = [['Health', 'Family/Home', 'Tired', "Academics", "Duty"]]

        bot.message.reply_text("Sad to know that, you wont be coming to lab today...")
        bot.message.reply_text("What's the general cause?",
                               reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                               one_time_keyboard=True))
        return TYPE

    def getReason(bot, context):
        d = context.user_data
        d['type'] = bot.message.text
        bot.message.reply_text('Hmmm... Can you tell a little more about it?')

        return REASON

    def registerLeave(bot, context):
        d = context.user_data
        d['user'] = bot.message.from_user['username']
        d['reason'] = bot.message.text
        print(d['user'])
        print(d['type'])
        print(d['reason'])
        bot.message.reply_text("Thank you for informing me.")
        bot.message.reply_text("Hope to see you soon again in the lab...")

        return ConversationHandler.END

    def cancel(bot, context):
        bot.message.reply_text('Bye! I hope we can talk again some day.',
                               reply_markup=ReplyKeyboardRemove())
