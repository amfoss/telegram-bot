#!/usr/bin/python3.6
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from graphqlclient import GraphQLClient
import json
from decouple import config

TYPE, REASON = range(2)

def get_cms_token():
    api_url = config('API_URL')
    client = GraphQLClient(api_url)
    query = """
    mutation TokenAuth($username: String!, $password: String!) {
      tokenAuth(username: $username, password: $password) {
        token
      }
    }
    """
    admin_user = config('ADMIN_USER')
    admin_pass = config('ADMIN_PASS')
    variables = {
        "username":admin_user,
        "password": admin_pass
    }
    result = json.loads(client.execute(query, variables))
    return result["data"]["tokenAuth"]["token"]

def getType(t):
    if t == "Health":
        return "M"
    elif t == "Family/Home":
        return "F"
    elif t == "Academics":
        return "A"
    return "T"

def mutate_cms(d):
    api_url = config('API_URL')
    client = GraphQLClient(api_url)
    query ="""
        mutation RecordLeaveToday($userId: String!, $reason: String!, $type: String!, $botToken: String!, $token: String!)
        {
          RecordLeaveToday(userId: $userId, reason: $reason, type: $type, botToken: $botToken, token: $token)
          {
            id
          }
        }
    """
    token = config('BOT_TOKEN')
    variables = {
        "userId": d['user'],
        "reason": d['reason'],
        "type": getType(d['type']),
        "botToken": token,
        "token": get_cms_token()
    }
    print(variables)
    client.execute(query, variables)

class LeaveRecord:

    def getType(bot, context):
        reply_keyboard = [['Health', 'Family/Home', 'Tired', "Academics"]]

        bot.message.reply_text("Sad to know that, you wont be coming to lab today...\n"
                                "What's the general cause?",
                               reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                               one_time_keyboard=True))
        return TYPE

    def getReason(bot, context):
        d = context.user_data
        d['type'] = bot.message.text
        bot.message.reply_text('Hmmm... Can you tell a little more about it?', reply_markup=ReplyKeyboardRemove())

        return REASON


    def registerLeave(bot, context):
        d = context.user_data
        d['user'] = bot.message.from_user['id']
        d['reason'] = bot.message.text
        bot.message.reply_text("Thank you for informing me.")
        bot.message.reply_text("Hope to see you soon again in the lab...")
        mutate_cms(d)

        return ConversationHandler.END

    def cancel(bot, context):
        bot.message.reply_text('Bye! I hope we can talk again some day.',
                               reply_markup=ReplyKeyboardRemove())
        
        return ConversationHandler.END
