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
    bot.send_message(message.chat.id, 'Введи номер строки от 1 до 490')
    bot.register_next_step_handler(message, reg_num)


def reg_num(message):
    global begin
    global cnt
    begin = (int(message.text) - 1)
    cnt = begin
    bot.send_message(message.chat.id, f'{list_words()[begin]["name"]}')
    bot.register_next_step_handler(message, verify_translate)


def verify_translate(message):

    global begin
    global lst_wrong
    global cnt

    if message.text.lower() != list_words()[begin]["translate"].lower():
            lst_wrong.append(list_words()[begin]["name"])

    if begin < (cnt + 9):
        begin += 1
        bot.send_message(message.chat.id, f'{list_words()[begin]["name"]}')
        bot.register_next_step_handler(message, verify_translate) 

    else:
        if lst_wrong:
            bot.send_message(message.chat.id, 'wrong_answers:\n------------------------\n     {}\n------------------------'.format("\n     ".join(str(x) for x in lst_wrong)))
        else:
            bot.send_message(message.chat.id, '👍Красавчик!👍'.upper())
        lst_wrong = []
        bot.send_message(message.chat.id, 'Введи номер строки от 1 до 490')
        bot.register_next_step_handler(message, reg_num)

bot.polling()
