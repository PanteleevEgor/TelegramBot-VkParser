from time import sleep
import requests
import json
import telebot
import csv

bot = telebot.TeleBot('token')  # Получить в BotFather
group_id = ''
count = ''

def main():
    # Токен для запросов, получаем при создание Standalone приложение ВК.
    access_token = 'token'
    version = '5.92'  # Версия запросов в ВК
    offset = 0
    all_posts = []

    while offset < 300:
        myparams = {'domain': group_id, 'v': version, 'access_token': access_token, 'offset': offset, 'count': count}
        respons = requests.get('https://api.vk.com/method/wall.get', params=myparams)
        posts = respons.json()['response']['items']
        offset += 100
        all_posts.extend(posts)
        sleep(3)
    return all_posts


def to_csv(file):
    with open('data.csv', 'w', encoding='utf-8', newline='') as f:
        write = csv.writer(f, delimiter=';')
        write.writerow(['Текст', 'Изображение'])
        for post in file:
            try:
                if post['attachments'][0]['type']:
                    img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
                else:
                    img_url = 'none'
            except:
                pass
            write.writerow((post['text'], img_url))


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Напиши id группы для парсинга.")
        bot.register_next_step_handler(message, get_id)  # следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')

def get_id(message):  # получаем фамилию
    global group_id
    group_id = message.text
    bot.send_message(message.from_user.id, 'Сколько постов надо спрасить?')
    bot.register_next_step_handler(message, get_count)

def get_count(message):
    global count
    count = message.text
    all_posts = main()
    to_csv(all_posts)
    bot.send_message(message.from_user.id, 'Парсинг заверешен.')
    send_chats(all_posts)
    # bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    # bot.register_next_step_handler(message, get_age)


def send_chats(data):
    print(data)


bot.polling()

if __name__ == '__main__':
    start()