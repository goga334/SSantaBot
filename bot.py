import telebot
import config
import modes
import time
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)
people = list()

markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup4 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_empty = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

item1 = types.KeyboardButton('"Почнімо)"')
markup1.add(item1)

item2 = types.KeyboardButton('"Це всі"')
markup2.add(item2)

item4 = types.KeyboardButton('"Так, точно всі"')
item3 = types.KeyboardButton('"Ой, бляха, забули"')
markup3.add(item3, item4)

item5 = types.KeyboardButton('"Давай ще раз"')
item6 = types.KeyboardButton('"Поки на паузі"')
markup4.add(item5, item6)


def shuffle(peo):
    ch_list = list()
    gift_given = [0] * len(peo)
    pick = 0
    exit = 0
    for i in range(0, len(peo)):
        while exit == 0:
            pick = random.randint(0, len(peo) - 1)
            if gift_given[pick] == 0 and pick != i:
                exit = 1
        ch_list.append(peo[pick])
        gift_given[pick] = 1
        exit = 0
    return ch_list


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Вітаю, {0.first_name}!\nЯ - <b>{1.first_name}</b>, "
                                      "бот, у якому ви можете випадковим чином розкидати подарунки між своїми друзями "
                     .format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup1)
    print('has began to play' + str(message.from_user.id))


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id, "Напишіть /start")


@bot.message_handler(content_types=['text'])
def bot_logic(message):
    if message.text[0] == '"':

        if message.text == '"Почнімо)"' or message.text == '"Давай ще раз"' or message.text == '"Ой, бляха, забули"':
            modes.mode = 'receiving'
            bot.send_message(message.chat.id, text="Відправляй мені імена учасників окремими повідомленнями", reply_markup=markup2)


        elif message.text == '"Це всі"':
            bot.send_message(message.from_user.id, "Точно нікого не забули? ", reply_markup=markup3)

        elif message.text == '"Так, точно всі"':
            modes.mode = 'working'
            bot.send_message(message.from_user.id, "Отже...", reply_markup=markup_empty)
            time.sleep(3)
            bot.send_message(message.from_user.id, "Санта потрапив у повітряну яму і всі подарунки перемішались", reply_markup=markup_empty)
            time.sleep(3)
            bot.send_message(message.from_user.id, "Санта проклинає УкрПовітрДор", reply_markup=markup_empty)
            time.sleep(3)
            bot.send_message(message.from_user.id, "Санта міняє оленів", reply_markup=markup_empty)
            time.sleep(3)
            bot.send_message(message.from_user.id, "І під ялинкою такий розклад:", reply_markup=markup_empty)
            time.sleep(3)
            gift = shuffle(people)
            for i in range(0, len(people)):
                bot.send_message(message.from_user.id, (people[i]+' отримує подарунок від '+gift[i]))
                time.sleep(1)
            bot.send_message(message.from_user.id, "Веселого нового року))", reply_markup=markup4)

        elif message.text == '"Поки на паузі"':
            bot.send_message(message.from_user.id, "Жду отвєта як Вова 50 грам. Ну ти цей... тикай /start єслі чо", reply_markup=markup3)

    elif modes.mode == 'receiving':
        people.append(message.text)

    else:
        bot.send_message(message.from_user.id, "Я не розумію, чого саме я не розумію. Напиши /help.", reply_markup=markup_empty)


bot.polling(none_stop=True)
# RUN