import random
# pip install telebot
import telebot

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN' # HTTP API from BotFather in Telegram
bot = telebot.TeleBot(TOKEN)

user_data = {}  # Dictionary to store user data

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    markup.add('/addition', '/subtraction', '/multiplication', '/division')

    bot.send_message(message.chat.id, "Welcome to the Math Quiz Bot!\nChoose an operation:", reply_markup=markup)


@bot.message_handler(commands=['addition', 'subtraction', 'multiplication', 'division'])
def handle_operation(message):
    operation = message.text[1:]
    user_data[message.chat.id] = {'operation': operation, 'correct_count': 0, 'total_count': 0}

    if operation in ['addition', 'subtraction']:
        level_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=5, one_time_keyboard=True)
        levels = list(range(1, 11))
        level_keyboard.add(*[telebot.types.KeyboardButton(str(level)) for level in levels])
        bot.send_message(message.chat.id, "Choose level (1-10):", reply_markup=level_keyboard)
    elif operation == 'multiplication':
        level_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
        levels = [1, 2, 3, 4, 5]
        level_keyboard.add(*[telebot.types.KeyboardButton(str(level)) for level in levels])
        bot.send_message(message.chat.id, "Choose level (1-5):", reply_markup=level_keyboard)
    elif operation == 'division':
        level_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
        levels = [1, 2, 3, 4, 5]
        level_keyboard.add(*[telebot.types.KeyboardButton(str(level)) for level in levels])
        bot.send_message(message.chat.id, "Choose level (1-5):", reply_markup=level_keyboard)


@bot.message_handler(func=lambda message: True)
def handle_level(message):
    level = int(message.text)
    if message.chat.id in user_data:
        operation = user_data[message.chat.id]['operation']

        if operation in ['addition', 'subtraction']:
            min_num = (level - 1) * 10 + 1
            max_num = level * 10
            num_problems = 10  # Set the number of problems for each level
        elif operation in ['multiplication', 'division']:
            min_num = 1
            max_num = 10 if level == 1 else (level + 1) * 10
            num_problems = 5  # Set the number of problems for each level

        user_data[message.chat.id]['num_problems'] = 0
        user_data[message.chat.id]['correct_count'] = 0
        user_data[message.chat.id]['total_count'] = 0

        generate_question(message.chat.id, operation, min_num, max_num, num_problems)


def generate_question(chat_id, operation, min_num, max_num, num_problems):
    if chat_id in user_data:
        if user_data[chat_id]['num_problems'] < num_problems:
            num1 = random.randint(min_num, max_num)
            num2 = random.randint(min_num, max_num)
            question = generate_question_text(operation, num1, num2)

            correct_answer = calculate_correct_answer(operation, num1, num2)
            user_data[chat_id]['correct_answer'] = correct_answer
            user_data[chat_id]['num_problems'] += 1

            bot.send_message(chat_id, question)
        else:
            markup = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
            markup.add('/addition', '/subtraction', '/multiplication', '/division')

            correct_count = user_data[chat_id]['correct_count']
            total_count = user_data[chat_id]['total_count']
            percent_correct = (correct_count / total_count) * 100 if total_count > 0 else 0

            user_data[chat_id]['num_problems'] = 0

            summary = f"Quiz completed!\nCorrect answers: {correct_count}\nTotal questions: {total_count}\nPercent correct: {percent_correct:.2f}%"
            bot.send_message(chat_id, summary, reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    if message.chat.id in user_data:
        correct_answer = user_data[message.chat.id]['correct_answer']

        try:
            user_answer = int(message.text)
            user_data[message.chat.id]['total_count'] += 1

            if user_answer == correct_answer:
                user_data[message.chat.id]['correct_count'] += 1
                bot.send_message(message.chat.id, "Correct!")
            else:
                bot.send_message(message.chat.id, f"Incorrect. The correct answer is {correct_answer}.")

            operation = user_data[message.chat.id]['operation']
            num_problems = user_data[message.chat.id]['num_problems']

            if num_problems < 10:
                generate_question(message.chat.id, operation, 1, 10, num_problems)
            else:
                generate_question(message.chat.id, operation, 1, 10, num_problems)
        except ValueError:
            bot.send_message(message.chat.id, "Invalid input. Please enter a number.")


def generate_question_text(operation, num1, num2):
    if operation == 'addition':
        return f"What is {num1} + {num2}?"
    elif operation == 'subtraction':
        return f"What is {num1} - {num2}?"
    elif operation == 'multiplication':
        return f"What is {num1} * {num2}?"
    elif operation == 'division':
        return f"What is {num1 * num2} / {num1}?"


def calculate_correct_answer(operation, num1, num2):
    if operation == 'addition':
        return num1 + num2
    elif operation == 'subtraction':
        return num1 - num2
    elif operation == 'multiplication':
        return num1 * num2
    elif operation == 'division':
        return num2


bot.polling(none_stop=True)
