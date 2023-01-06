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

NAME, EMAIL, COURSE, GO_COURSE = range(4)

USER = {

}
new_user = None
def start_command(update, context):
    chat_id = update.message.chat_id
    update.message.reply_text("""Welcome to our Bitcoin for beginners course bot.\n\nClick\n<b>/signup</b> to sign up for the course\n<b>/help</b> to get help\n<b>/start_course</b> to go to course""", parse_mode=ParseMode.HTML)

def help_command(update, context):
    update.message.reply_text(responses.help_message)

def start_course(update, context):
    return GO_COURSE

def signup_command(update, context) -> int:
    global new_user

    user = update.message.from_user
    count = 0
    name = None
    with open("users.json", "r") as file:
        users_list = json.load(file)['users']
        for i in users_list:
            if user['id'] == i['id']:
                name = i['name']
                count += 1
    if count > 0:
        update.message.reply_text(f"Hey {name}, you're already registered")
        new_user = False
        return COURSE

    else:
        update.message.reply_text(f"Hi 👋🏾,\nWelcome to the African Bitcoiners Telegram Course please tell us your name")
        new_user = True
        return EMAIL

def email(update, context) -> int:
    user = update.message.from_user
    name = update.message.text
    user_id = user['id']
    USER["id"] = user_id
    USER['name'] = name
    update.message.reply_text(f"Thank you {name}, please input your email address")
    return COURSE

def course(update, context) -> int:
    global new_user


    if new_user:
        email = update.message.text
        user = update.message.from_user
        user_id = user['id']
        USER['email'] = email
        USER['status'] = None
        responses.save_user(USER)
        day = -1

    if not new_user:
        user = update.message.from_user
        user_id = user['id']
        with open("users.json", encoding="utf-8") as file:
            users_list = json.load(file)['users']
            for user in users_list:
                if user["id"] == user_id:
                    day = user["status"]


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

    # if day == 0:
    #     user = update.message.from_user
    #     user_id = user['id']
    #     time.sleep(10)
    #     update.message.reply_text(contents["day_0"][0])
    #     time.sleep(5)
    #     update.message.reply_text(contents["day_0"][1])
    #     time.sleep(5)
    #     update.message.reply_text(contents["day_0"][2])
    #     time.sleep(5)
    #     update.message.reply_text(contents["day_0"][3])
    #     day += 1
    #     # with open("day.txt", "w") as file:
    #     #     file.write(str(day))
    #     responses.update_status(user_id=user_id, status=day)

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

def cancel(update, context) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.sample_responses(text)

    update.message.reply_text(response)

# def error(update, context):
#     print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("signup", signup_command)],
        states={
            EMAIL: [MessageHandler(Filters.text, email)],
            COURSE: [MessageHandler(Filters.regex("@"), course)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("start_course", course))

    dp.add_handler(MessageHandler(Filters.text, handle_message))
    #
    # dp.add_error_handler(error)

    updater.start_polling(1)
    updater.idle()

main()