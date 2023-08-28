import random
import telebot

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)


def generate_question(operation, num1, num2):
    if operation == 'addition':
        question = f"What is {num1} + {num2}?"
    elif operation == 'subtraction':
        question = f"What is {num1} - {num2}?"
    elif operation == 'multiplication':
        question = f"What is {num1} * {num2}?"
    elif operation == 'division':
        question = f"What is {num1} / {num2}?"
    return question


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Welcome to the Math Quiz Bot! Use commands like /addition, /subtraction, /multiplication, /division to play.")


@bot.message_handler(commands=['addition', 'subtraction', 'multiplication', 'division'])
def handle_operation(message):
    operation = message.text[1:]
    if operation == 'addition':
        bot.send_message(message.chat.id, "You've selected addition.")
        difficulty_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        difficulty_keyboard.add(telebot.types.KeyboardButton("1-10"), telebot.types.KeyboardButton("1-100000"))
        bot.send_message(message.chat.id, "Choose difficulty:", reply_markup=difficulty_keyboard)
    elif operation == 'subtraction':
        bot.send_message(message.chat.id, "You've selected subtraction.")
        difficulty_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        difficulty_keyboard.add(telebot.types.KeyboardButton("1-1000"), telebot.types.KeyboardButton("1-100000"))
        bot.send_message(message.chat.id, "Choose difficulty:", reply_markup=difficulty_keyboard)
    elif operation == 'multiplication':
        bot.send_message(message.chat.id, "You've selected multiplication.")
        difficulty_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        difficulty_keyboard.add(telebot.types.KeyboardButton("1-10"))
        bot.send_message(message.chat.id, "Choose difficulty:", reply_markup=difficulty_keyboard)
    elif operation == 'division':
        bot.send_message(message.chat.id, "You've selected division.")
        difficulty_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        difficulty_keyboard.add(telebot.types.KeyboardButton("1-10"))
        bot.send_message(message.chat.id, "Choose difficulty:", reply_markup=difficulty_keyboard)


@bot.message_handler(func=lambda message: True)
def handle_difficulty(message):
    difficulty = message.text
    if '-' in difficulty:
        min_num, max_num = map(int, difficulty.split('-'))
        question = generate_question(min_num, max_num)
        bot.send_message(message.chat.id, question)
      

if __name__ == "__main__":
    bot.polling()
