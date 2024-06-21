import telebot

try:
    with open('token_telegram.txt', 'r') as f:
        bot_token = f.read().strip()
        bot = telebot.TeleBot(bot_token)
except FileNotFoundError:
    bot_token = input("Введите ваш токен Telegram ")
    bot = telebot.TeleBot(bot_token)
    with open('token_telegram.txt', 'w') as f:
        f.write(bot_token)
        bot = telebot.TeleBot(bot_token)

owner_id = 1234567890#Введите свой айди(enter you id)
user_states = {}

print(f'Bot: {bot_token} started')

@bot.message_handler(commands=['start'])
def start(message):
    # Создаем кнопки
    chat_id = message.chat.id

    if chat_id == owner_id:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
        btn1 = telebot.types.KeyboardButton('Помощь')
        btn2 = telebot.types.KeyboardButton('Отправить ответ')
        markup.add(btn1, btn2)
    else:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
        btn1 = telebot.types.KeyboardButton('Помощь')
        btn2 = telebot.types.KeyboardButton('Отправить запрос')
        btn3 = telebot.types.KeyboardButton('Правила')
        markup.add(btn1, btn2, btn3)  # Добавляем кнопки на клавиатуру
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Отправить запрос')
def request_data(message):
    user_id = message.chat.id
    bot.reply_to(message, 'Введите запрос')
    user_states[user_id] = 'waiting_request'

@bot.message_handler(func=lambda message: message.text == 'Правила')
def rules(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Правила: \n- записи с нецензурной лексикой не принимаются \n- записи с пропагандой и/или конентом 18+ не принимаются \n- записи нарушающие закон РФ не принимаются \n- записи не по теме сообщества не принимаются")

@bot.message_handler(func=lambda message: message.text == 'Отправить ответ')
def reply(message):
    user_id = message.chat.id
    bot.reply_to(message, 'Введите что нужно отправить')
    user_states[user_id] = 'waiting_reply'

@bot.message_handler(func=lambda message: message.text == 'Помощь')
def help_get(message):
    user_id = message.chat.id
    bot.send_message(user_id, '1. Нажать /start и запустить бота\n2. Нажать "отправить запрос"\n3. Выбрать медиа или текстовый файл\n4. Отправить медиа или текстовый файл\n5. Ждать одобрения вашей записи (если она не нарушает правила) ')

@bot.message_handler(func=lambda message: True)  # Ловим все текстовые сообщения
def handle_message(message):
    user_id = message.chat.id
    user_username = message.from_user.username
    try:
        if user_states[user_id] == 'waiting_request':
            user_states[user_id] = None
            text = f'Запрос: {message.text} \nId запросившего: {user_id} \nНикнейм запросившего: {user_username}'
            bot.reply_to(message, 'Спасибо за запрос, ожидайте ответа')
            bot.send_message(owner_id, text)

        elif user_states[user_id] == 'waiting_reply':
            user_states[user_id] = None
            try:
                parts = message.text.split(' ', 1)
                reply_id = parts[0].strip()
                text = parts[1].strip()
                bot.send_message(reply_id, f'Отправил: Владелец\n{text}')
                bot.reply_to(message, 'Успешно отправлено')
            except IndexError:
                bot.reply_to(message, 'Неправильно использование команды. \nПравильное: (id кому нужно отправить) (текст)')
    except KeyError:
        bot.send_message(user_id, 'Вы не выбрали функцию и отправили сообщение в пустую')
bot.polling()