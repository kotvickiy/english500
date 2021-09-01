#!/usr/bin/env python3.9
from os import cpu_count
import telebot
from config import TOKEN
import csv

def list_words():
    with open('./eng_rus.csv', encoding='utf-8') as file:
        order = ['name', 'transcription', 'translate']
        reader = csv.DictReader(file, fieldnames=order)
        return [i for i in reader]

begin = 0
cnt = 0
lst_wrong = []

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    global lst_wrong
    lst_wrong = []
    bot.send_message(message.chat.id, 'Введи номер строки от 1 до 490')
    bot.register_next_step_handler(message, reg_num)


def reg_num(message):
    global begin
    global cnt
    try:
        if not (1 <= int(message.text) <= 490):
            start(message)
        else:
            begin = (int(message.text) - 1)
            cnt = begin
            bot.send_message(message.chat.id, f'{list_words()[begin]["name"]}')
            bot.register_next_step_handler(message, verify_translate)
    except ValueError:
        start(message)


def verify_translate(message):

    global begin
    global lst_wrong
    global cnt  

    if message.text.lower() != list_words()[begin]["translate"].lower():
            lst_wrong.append(list_words()[begin]["name"])

    if begin < (cnt + 9):
        if message.text.lower() == '/start':
            start(message)
        else:
            begin += 1
            bot.send_message(message.chat.id, f'{list_words()[begin]["name"]}')
            bot.register_next_step_handler(message, verify_translate) 

    else:
        if lst_wrong:
            bot.send_message(message.chat.id, 'W R O N G _ A N S W E R S :' + '\n' + '_' * 27 + '\n'+ "\n".join(str(x) for x in lst_wrong) +'\n' + '_' * 27 )
        else:
            bot.send_message(message.chat.id, '👍Красавчик!👍'.upper())
        lst_wrong = []
        start(message)

bot.polling()
