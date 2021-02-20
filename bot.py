import telebot
from config import tg_token, token
from telebot import types
from main import OkDesk


bot = telebot.TeleBot(tg_token)
list_tt = OkDesk(token)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, "Количество заявок без ответа, МОЛИСЬ ГАДЁНЫШЬ ЧТОБЫ ИХ БЫЛО '0': ")
        keyboard = types.InlineKeyboardMarkup()
        key_tt = types.InlineKeyboardButton(text='GET', callback_data='PASS')
        keyboard.add(key_tt)
        bot.send_message(message.from_user.id, text='Что ж утырок жмакай кнопку', reply_markup=keyboard)
    elif message.text == '/help':
        bot.send_message(message.from_user.id, 'Напиши Привет')
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'PASS':
        if list_tt.count_tt() > 0:
            bot.send_message(call.message.chat.id, text='Готовь очко!!!')
            bot.send_message(call.message.chat.id, list_tt.count_tt(), reply_markup=add_keyboard())


@bot.callback_query_handler(func=lambda call: True)
def add_keyboard(call):
    if call.data == 'GET':
        bot.send_message(call.message.chat.id, text='Ждите...')
        bot.send_message(call.message.chat.id, list_tt.get_link())


bot.polling(none_stop=True, interval=0)
