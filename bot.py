import telebot
from telebot import types
from telebot.types import Message
from random import *
import json
import requests


phonebook = {}

bot = telebot.TeleBot('6502873439:AAGeQ7jziDva2HkpuHg5IT9Ur5ye7_qkgUg')

keyboard = telebot.types.InlineKeyboardMarkup()

                        
@bot.message_handler(commands=['start'])
def start_messege(message):
    start_keyboard = types.InlineKeyboardMarkup()
    key_start = types.InlineKeyboardButton(text = 'МЕНЮ', callback_data='menu')
    start_keyboard.add(key_start)
    bot.send_message(message.chat.id, text='Вас приветствует Телефонный справочник!', reply_markup= start_keyboard)

def search_contact(message):
    with open('phonebook.json', 'r', encoding='utf-8') as ph:
        data = json.load(ph)
        message.search_text = message.text.lower()
        result = []
        for contact in data.values():
            if message.search_text in [str(value).lower() for value in contact.values()]:
                result.append(contact)
        if result:
            # if result: len(result) > 0:
            response = "Результат:\n"

            for contact in result:
                response += "\n"
                for key, value in contact.items():
                    response += key + ": " + str(value) + "\n"
            bot.send_message(message.chat.id, text=response)
            show_menu(message.chat.id)

        else:
            bot.send_message(message.chat.id, text='По вашему запросу ничего не найдено.')
            show_menu(message.chat.id)
            


def tel_mobil(message):
    phonebook['ФИО'] = message.text
    bot.send_message(message.chat.id, text="Мобильный телефон: ")
    bot.register_next_step_handler(message, tel_home)
def tel_home(message):
    phonebook['Мобильный'] = message.text
    bot.send_message(message.chat.id, text="Домашний телефон: ")
    bot.register_next_step_handler(message, tel_dop)
def tel_dop(message):
    phonebook['Домашний'] = message.text
    bot.send_message(message.chat.id, text="Дополнительный телефон: ")
    bot.register_next_step_handler(message, b_day)
def b_day(message):
    phonebook['Дополнительный'] = message.text
    bot.send_message(message.chat.id, text="Дата рождения: ")
    bot.register_next_step_handler(message, e_mail)
def e_mail(message):
    phonebook['Дата рождения'] = message.text
    bot.send_message(message.chat.id, text="E-mail: ")
    bot.register_next_step_handler(message, add_new_contact)
def add_new_contact(message):
    phonebook['E-mail'] = message.text

    with open("phonebook.json", "r+", encoding="utf-8") as ph:
        data = json.load(ph)
        data.update({phonebook['ФИО']:phonebook})
        ph.seek(0)
        json.dump(data, ph, ensure_ascii=False, indent=2)

    bot.send_message(message.chat.id, text="Новый контакт добавлен.")
    show_menu(message.chat.id)

def add_contact(message):

    with open('phonebook.json', 'r', encoding='utf-8') as ph:
        data = json.load(ph)
        search_text = message.text

        if search_text in data.keys():
            bot.send_message(message.chat.id, text=f'Контакт с именем "{search_text}" уже существует...')
            show_menu(message.chat.id)
        else:
            tel_mobil(message)
        
def del_contact(message):
    with open('phonebook.json', 'r', encoding='utf-8') as ph:
        data = json.load(ph)
        search_text = message.text

        if search_text in data.keys():
            del data[search_text]
            with open('phonebook.json', 'w', encoding='utf-8') as ph:
                json.dump(data, ph, ensure_ascii=False, indent=2)
            bot.send_message(message.chat.id, text=f"контакт {search_text} удален.")
            show_menu(message.chat.id)

        else:
            bot.send_message(message.chat.id, text=f'Контакта с именем "{search_text}" нет в справочнике...')
            show_menu(message.chat.id)

def edit(message):
    with open('phonebook.json', 'r', encoding='utf-8') as ph:
        data = json.load(ph)
    search_text = message.text

    if search_text in data:
        global edit_contact
        edit_contact = data[search_text]
        bot.send_message(message.chat.id, text="новый фио: ")
        bot.register_next_step_handler(message, edit_name)
    else:
        bot.send_message(message.chat.id, text=f'Контакта с именем "{search_text}" нет в справочнике...')


def edit_name(message):
    new_name = message.text
    global edit_contact  
    with open('phonebook.json', 'r+', encoding='utf-8') as ph:
        data = json.load(ph)
        data[new_name] = data.pop(edit_contact['ФИО'])  
        edit_contact['ФИО'] = new_name  
        ph.seek(0)  
        json.dump(data, ph, ensure_ascii=False, indent=2)  

    bot.send_message(message.chat.id, text="Мобильный телефон: ")
    bot.register_next_step_handler(message, edit_mobile)    
def edit_mobile(message):
    edit_contact['Мобильный'] = message.text
    bot.send_message(message.chat.id, text="Домашний телефон: ")
    bot.register_next_step_handler(message, edit_home)
def edit_home(message):
    edit_contact['Домашний'] = message.text
    bot.send_message(message.chat.id, text="Дополнительный телефон: ")
    bot.register_next_step_handler(message, edit_additional)
def edit_additional(message):
    edit_contact['Дополнительный'] = message.text
    bot.send_message(message.chat.id, text="Дата рождения: ")
    bot.register_next_step_handler(message, edit_birthday)
def edit_birthday(message):
    edit_contact['Дата рождения'] = message.text
    bot.send_message(message.chat.id, text="E-mail: ")
    bot.register_next_step_handler(message, edit_email)
def edit_email(message):
    edit_contact['E-mail'] = message.text
    save_edited_contact(message)
def save_edited_contact(message):
    with open("phonebook.json", "r+", encoding='utf-8') as ph:
        data = json.load(ph)
        data.update({edit_contact['ФИО']: edit_contact})
        ph.seek(0)
        ph.truncate()
        json.dump(data, ph, ensure_ascii=False, indent=2)

    bot.send_message(message.chat.id, text="Контакт обновлен.")
    show_menu(message.chat.id)

def show_menu(chat_id):
    menu_keyboard = telebot.types.InlineKeyboardMarkup()

    key_view = telebot.types.InlineKeyboardButton(text='Весь Список', callback_data='viev')
    menu_keyboard.add(key_view)

    key_search = telebot.types.InlineKeyboardButton(text='Поиск Контакта', callback_data='search')
    menu_keyboard.add(key_search)

    key_add = telebot.types.InlineKeyboardButton(text='Создать Контакт', callback_data='add')
    menu_keyboard.add(key_add)

    key_delete = telebot.types.InlineKeyboardButton(text='Удалить Контакт', callback_data='delite')
    menu_keyboard.add(key_delete)

    key_change = telebot.types.InlineKeyboardButton(text='Изменить Контакт', callback_data='edit')
    menu_keyboard.add(key_change)
    
    bot.send_message(chat_id, text='Выберите действие:', reply_markup=menu_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def phone(call):
    if call.data == 'menu':

        key_view = telebot.types.InlineKeyboardButton(text='Весь Список', callback_data='viev')
        callback_data='view'
        keyboard.add(key_view)

        key_search = telebot.types.InlineKeyboardButton(text='Поиск Контакта', callback_data='search')
        callback_data='search'
        keyboard.add(key_search)

        key_add = telebot.types.InlineKeyboardButton(text='Создать Контакт', callback_data='add')
        callback_data='add'
        keyboard.add(key_add)

        key_delite = telebot.types.InlineKeyboardButton(text='Удалить Контакт', callback_data='delite')
        callback_data='delite'
        keyboard.add(key_delite)

        key_change = telebot.types.InlineKeyboardButton(text='Изменить Контакт', callback_data='edit')
        callback_data='edit'
        keyboard.add(key_change)
        
        bot.send_message(call.message.chat.id, text='Какое действие хотите совершить?', reply_markup=keyboard)

    elif call.data == 'viev':
        bot.send_message(call.message.chat.id, text='Список Ваших контактов: ')
        with open('phonebook.json', 'r', encoding='utf-8') as ph:
            data = json.load(ph)
            contact = '\n'.join([entry["ФИО"] for entry in data.values()])
        bot.send_message(call.message.chat.id, contact)


    elif call.data == 'search':

        bot.send_message(call.message.chat.id, text="Введите или номер телефона")
        bot.register_next_step_handler(call.message, search_contact)

    elif call.data == 'add':

        contact_name = bot.send_message(call.message.chat.id, text="Введите ФИО")
        bot.register_next_step_handler(call.message, add_contact)   

    elif call.data == 'delite':
        contact_name = bot.send_message(call.message.chat.id, text="Введите ФИО контакта который хотите удалить: ")
        bot.register_next_step_handler(call.message, del_contact)   

    elif call.data == 'edit':
        contact_name = bot.send_message(call.message.chat.id, text="Введите ФИО контакта который хотите изменить: ")
        bot.register_next_step_handler(call.message, edit)  

    else:
        bot.send_message(call.message.chat.id, text = 'к сожелению произошла критическая ошибка... попробуйте еще раз...')

bot.polling()
# bot.polling(none_stop=True)