#!/usr/bin/env python3
import telebot
from config import TOKEN
import csv
from random import randint

def list_words():
    with open('./eng_rus.csv', encoding='utf-8') as file:
        order = ['name', 'transcription', 'translate']
        reader = csv.DictReader(file, fieldnames=order)
        return [i for i in reader]

begin = 0
lst_wrong = []
cropped_shuffled_list =[]
tmp = []
x = 0

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    global lst_wrong
    lst_wrong = []
    bot.send_message(message.chat.id, 'Введи номер строки от 1 до 490')
    bot.register_next_step_handler(message, reg_num)


def reg_num(message):
    global begin
    global cropped_shuffled_list
    global x
    global tmp
    try:
        if not (1 <= int(message.text) <= 490):
            start(message)
        else:
            begin = (int(message.text) - 1)
            
            x = randint(0, 9)
            tmp.append(x)
            
            cropped_shuffled_list = list_words()[begin:begin+10]

            bot.send_message(message.chat.id, f'{cropped_shuffled_list[x]["name"].upper()}{cropped_shuffled_list[x]["transcription"]}')
            bot.register_next_step_handler(message, verify_translate)
    except ValueError:
        start(message)


def verify_translate(message):
    global begin
    global lst_wrong
    global cropped_shuffled_list
    global tmp
    global x

    if ';' in cropped_shuffled_list[x]["translate"].lower():
        if message.text.lower() != cropped_shuffled_list[x]["translate"].lower().split(';')[0] and message.text.lower() != cropped_shuffled_list[x]["translate"].lower().split(';')[1]:
            lst_wrong.append(cropped_shuffled_list[x]["name"])
    
    elif message.text.lower() != cropped_shuffled_list[x]["translate"].lower():
        lst_wrong.append(cropped_shuffled_list[x]["name"])

    if len(tmp) < 10:
        if message.text.lower() == '/start':
            start(message)
        else:
            begin += 1
            while True:
                x = randint(0, 9)
                if x not in tmp:
                    tmp.append(x)
                    break
            bot.send_message(message.chat.id, f'{cropped_shuffled_list[x]["name"].upper()}{cropped_shuffled_list[x]["transcription"]}')
            bot.register_next_step_handler(message, verify_translate) 

    else:
        if lst_wrong:
            bot.send_message(message.chat.id, 'W R O N G _ A N S W E R S :' + '\n' + '_' * 27 + '\n'+ "\n".join(str(x) for x in lst_wrong) +'\n' + '_' * 27)
        else:
            bot.send_message(message.chat.id, '👍Красавчик!👍'.upper())
        begin = 0
        lst_wrong = []
        cropped_shuffled_list =[]
        tmp = []
        x = 0
        start(message)
bot.polling()
