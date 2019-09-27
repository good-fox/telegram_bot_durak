import APY
import telebot
import os
import time
import durac_fun
import random
from telebot import types


bot = telebot.TeleBot(APY.token)

@bot.message_handler(commands=['coloda'])
def check_coloda(message):
    coloda = durac_fun.get_coloda()
    coloda_str = ''
    for card in coloda:
        coloda_str += card
    print(coloda_str)
    bot.send_message(message.chat.id, coloda_str)


@bot.message_handler(commands=['add_game'])
def add_game(message):
    text = durac_fun.set_user_add_game(message.chat.id)
    bot.send_message(message.chat.id, text)
        

@bot.message_handler(commands=['end_game'])
def end_game(message):
    text = durac_fun.set_user_end_game(message.chat.id)
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['start_game'])
def start_game(message):
    if message.text == '/start_game':
        list = durac_fun.get_start_game_for_user(message.chat.id)
        if list != None:
            print(list[0])
            markup = durac_fun.generate_markup(message.chat.id)
            bot.send_message(message.chat.id, '{}  🀄️ - {}'.format(list[4], list[3]), reply_markup = markup)
            time.sleep(0)
            markup = durac_fun.generate_markup(list[2])
            print(list[1])
            bot.send_message(list[2], '{}  🀄️ - {}'.format(list[4], list[3]), reply_markup = markup)

    else:
        for id in message.text.split('/start_game '):
            pass
        text, game, text_id = durac_fun.set_user_start_game(message.chat.id, id)
        bot.send_message(message.chat.id, text)
        if game:
            bot.send_message(id, text_id)


@bot.message_handler(content_types=['text'])
def game(message):
    print()
    data = durac_fun.get_game_for_user(message.chat.id, message.text)
    
    if data != None:
        markup = durac_fun.generate_markup(data[0])
        bot.send_message(data[0], data[1], reply_markup = markup)
 

def main():
    bot.polling(none_stop = True)

if __name__ == '__main__':
    main()
