# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 13:47:21 2022

@author: arsko
"""
import os
import telebot
import urllib
from telebot import types
import pickle
import practice_model

#results = {'бабочка':0,'курица':0,'корова':0,'собака':0,'слон':0,'лошадь':0,'кошачий':0,'овца':0,'паук':0,'белка':0}
result_storage_path = 'images'
token='********:***************************'
bot=telebot.TeleBot(token)

with open('results.pickle', 'rb') as f:
    results = pickle.load(f)
    
def save_image_from_message(message):
    image_id = get_image_id_from_message(message)
    file_path = bot.get_file(image_id).file_path
    image_url = "https://api.telegram.org/file/bot{0}/{1}".format(token, file_path)

    if not os.path.exists(result_storage_path):
        os.makedirs(result_storage_path)

    image_name = "{0}.jpg".format(image_id)
    urllib.request.urlretrieve(image_url, "{0}/{1}".format(result_storage_path, image_name))
    return image_name

def get_image_id_from_message(message):
    return message.photo[len(message.photo) - 1].file_id

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Прислать картинку")
    btn2 = types.KeyboardButton("Информация о боте")
    btn3 = types.KeyboardButton("Кого чаще всего присылают")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я могу определить животное на картинке, попробуем?".format(message.from_user), reply_markup=markup)
    
@bot.message_handler(content_types='text')
def message_reply(message):
    if(message.text == "Прислать картинку"):
        msg = bot.send_message(message.from_user.id, 'Присылайте картинку, я скажу что на ней')
        bot.register_next_step_handler(msg, get_result)
    elif(message.text == "Узнать обо мне"):
        markup = types.InlineKeyboardMarkup()
        btn_docs= types.InlineKeyboardButton(text='Данные, на которых меня обучали', url='https://www.kaggle.com/datasets/alessiocorrado99/animals10')
        markup.add(btn_docs)
        bot.send_message(message.chat.id, text="Я бот, созданный для распознавания животных на картинках. Обучался я на 10000 изображениях разных видов. Я могу определить: собаку, кошку, белку, паука, бабочку, слона, лошадь, овцу, курицу и корову.",reply_markup = markup)
    elif(message.text == "Кого чаще всего присылают"):
        bot.send_message(message.chat.id, "Больше всего я распознавал вид "+max(results))
        
    else:
        bot.send_message(message.chat.id, text="На такую команду я не запрограммировал..")

@bot.message_handler(content_types=['photo'])
def get_result(message):
    image_name = save_image_from_message(message)
    result = practice_model.predict_it('images/'+image_name)
    bot.send_message(message.chat.id, result)
    if result != 'Такое я не могу распознать(':
        results[result.split(' ')[4]] += 1
    os.remove('images/'+image_name)
    with open('results.pickle', 'wb') as f:
        pickle.dump(results, f)
bot.infinity_polling()
