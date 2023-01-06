import json
import datetime
import time

from course_contents import contents
import keys
from telegram.ext import *
from telegram import ParseMode

import responses
import responses as R
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

print("Bot started...")

def help_command(update, context):
    update.message.reply_text(responses.help_message)

def start_command(update, context) -> int:

    day = -1


    current_time = str(datetime.datetime.now()).split()[1].split('.')[0]



    if day == -1:
        user = update.message.from_user
        user_id = user['id']
        pic = "Images/welcome.png"
        update.message.reply_photo(open(pic, "rb"))
        update.message.reply_text(contents["welcome"][0], parse_mode=ParseMode.HTML)
        time.sleep(5)
        update.message.reply_text(contents["welcome"][1], parse_mode=ParseMode.HTML)
        day += 1
        # with open("day.txt", "w") as file:
        #     file.write(str(day))
        responses.update_status(user_id=user_id, status=day)

    # elif day > 22 and current_time == "05:00:00":
    if day > -1:
        user = update.message.from_user
        user_id = user['id']
        while day < 22:
            if day == 0:
                time.sleep(10)
                if current_time == "05:00:00":
                    user = update.message.from_user
                    user_id = user['id']
                    update.message.reply_text(contents["day_0"][0], parse_mode=ParseMode.HTML)
                    time.sleep(5)
                    update.message.reply_text(contents["day_0"][1], parse_mode=ParseMode.HTML)
                    time.sleep(5)
                    update.message.reply_text(contents["day_0"][2], parse_mode=ParseMode.HTML)
                    time.sleep(5)
                    update.message.reply_text(contents["day_0"][3], parse_mode=ParseMode.HTML)
                    day += 1
                    # with open("day.txt", "w") as file:
                    #     file.write(str(day))
                    responses.update_status(user_id=user_id, status=day)

            else:
                if current_time == "05:00:00":
                    update.message.reply_text(contents[f"day_{day}"][0], parse_mode=ParseMode.HTML)
                    time.sleep(5)
                    update.message.reply_text(contents[f"day_{day}"][1], parse_mode=ParseMode.HTML)
                    time.sleep(5)
                    update.message.reply_text(contents[f"day_{day}"][2], parse_mode=ParseMode.HTML)

                    day += 1
                    # with open("day.txt", "w") as file:
                    #     file.write(str(day))
                    responses.update_status(user_id=user_id, status=day)
                    #
                    # time.sleep(10)

    else:
        update.message.reply_text(contents[f"Thank you for completing the course!"], parse_mode=ParseMode.HTML)
        return ConversationHandler.END



def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.sample_responses(text)

    update.message.reply_text(response)

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling(1)
    updater.idle()

main()