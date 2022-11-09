import vk_api
import config
import urllib
import json
import requests as req
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import string
import array

token = config.settings['TOKEN']  # присваиваем переменной значение токена из файла конфига
group_id = config.settings['group_id']  # id выбранной для работы бота группы


def get_apis(period):
    # объявляем лист для хранения апи погоды
    url = config.api[0]  # берем первую ссылку на апи
    # print(url)
    json_data = urllib.request.urlopen(url).read()  # читаем данные из JSON полученного из нашей ссылки
    weather = []
    weather.append(json.loads(json_data))  # добавляем в конец листа наш JSON
    key = config.settings['yan_key']
    url = config.api[1]
    yandex_req = req.get(url, headers={'X-Yandex-API-Key': key}, verify=False)
    json_data = yandex_req.text
    print(json.loads(json_data))
    weather.append(json.loads(json_data))
    if period >= 3:
        for i in range(period):
            url = config.api[i + 2]
            json_data = urllib.request.urlopen(url).read()
            weather.append(json.loads(json_data))
    # print(weather)
    return weather


def get_numbers(weather):
    current_weather = weather[0]['data'][0]
    wind_spd = array.array('f')  # массив для скорости ветра типа float
    temp = array.array('f')  # массив для температуры типа float
    wind_spd.append(current_weather['wind_spd'])  # скорость ветра
    wind_spd.append(weather[1]['forecasts'][0]['parts']['morning']['wind_speed'])
    wind_spd1 = comparison(wind_spd)
    temp.append(current_weather['app_temp'])  # температура
    temp.append(weather[1]['forecasts'][0]['parts']['morning']['temp_avg'])
    temp1 = comparison(temp)
    # можно ли будет добавить направление ветра?
    date = weather[1]['forecasts'][0]['date']
    wind_dir = weather[1]['forecasts'][0]['parts']['morning']['wind_dir']
    weather = date + '\n' + 'Температура - ' + str(temp1) + 'C \n' + "Ветер - " + wind_change(
        wind_dir) + '\nСкорость ветра - ' + str(wind_spd1) + ' м/с'
    return weather


def comparison(num):
    average = sum(num) / len(num)
    return average


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


def wind_change(wind_dir):
    if wind_dir == "sw":
        dir = "юго-западный"
    if wind_dir == "se":
        dir = "юго-восточный"
    if wind_dir == "s":
        dir = "южный"
    if wind_dir == "n":
        dir = "северный"
    if wind_dir == "ne":
        dir = "северо-восточный"
    if wind_dir == "nw":
        dir = "северо-западный"
    if wind_dir == "w":
        dir = "западный"
    if wind_dir == "e":
        dir = "восточный"
    return dir

def cond_change(condition): # переводим состояние погоды
    if condition == "clear":
        cond = "\U00002600 Ясно"
    if condition == "partly-cloudy":
        cond = "\U000026C5 Малооблачно"
    if condition == "cloudy":
        cond = "\U0001F324 Облачно с прояснениями"
    if condition == "overcast":
        cond = "\U00002601 Пасмурно"
    if condition == "drizzle":
        cond = "\U0001F327 Морось"
    if condition == "light-rain":
        cond = "\U0001F326 Небольшой дождь"
    if condition == "rain":
        cond = "\U0001F327 Дождь"
    if condition == "moderate-rain":
        cond = "\U0001F327 Умеренно сильный дождь"
    if condition == "heavy-rain":
        cond = "\U0001F327 Сильный дождь"
    if condition == "continuous-heavy-rain":
        cond = "\U0001F327 Длительный сильный дождьм"
    if condition == "showers":
        cond = "\U0001F327 Ливень"
    if condition == "wet-snow":
        cond = "\U0001F328 Дождь со снегом"
    if condition == "light-snow":
        cond = "\U0001F328 Небольшой снег"
    if condition == "snow":
        cond = "\U00002744 Снег"
    if condition == "snow-showers":
        cond = "\U0001F328 Снегопад"
    if condition == "hail":
        cond = "\U0001F327 Град"
    if condition == "thunderstorm":
        cond = "\U0001F329 Гроза"
    if condition == "thunderstorm-with-rain":
        cond = "\U000026C8 Дождь с грозой"
    if condition == "thunderstorm-with-hail":
        cond = "\U000026C8 Гроза с градом"
    return cond

def print_weather(period, i):  # функция получения текущего города
    # print(data)
    data = get_apis(2)
    if period == 1 | 7:
        current_weather = data[0]['data'][i]  # выбираем нужную нам часть с данными
        date = current_weather['datetime']
        desc = current_weather['weather']['description']
        wind = current_weather['wind_cdir_full']
        wind_spd = current_weather['wind_spd']
        wind_spd = toFixed(wind_spd, 2)
        if period == 1:
            city = current_weather['city_name']
            temp = current_weather['app_temp']
            weather = date + '\n' + desc + '\n \U0001F321  Температура  ' + str(temp) + '°C \n' + "\U0001F32C Ветер - " + wind + '\nСкорость ветра - ' + str(wind_spd) + ' м/с'
        elif period == 7:
            temp = current_weather['app_max_temp']
            weather = date + '\n' + desc + ' - ' + '\n \U0001F321 макс. температура - ' + str(temp) + '°C \n' + "\U0001F32C Ветер - " + wind + '\nСкорость ветра - ' + str(wind_spd) + ' м/с'

    elif period == 6 or 3 or 2:
        current_weather = data[1]['forecasts'][i]
        #date = current_weather['date'] # дата погоды
        condition = current_weather['parts']['day_short']['condition'] # погодное описание
        #icon = current_weather['parts']['day_short']['icon'] # иконка погоды
        temp_min = current_weather['parts']['day_short']['temp_min'] # мин температура
        feels_like = current_weather['parts']['day_short']['feels_like'] # ощущается как
        humidity = current_weather['parts']['day_short']['humidity'] # влажность воздуха
        temp_max = current_weather['parts']['day_short']['temp'] # макс температура
        wind = current_weather['parts']['day_short']['wind_speed'] # скорость ветра
        wind_dir = current_weather['parts']['morning']['wind_dir'] # направление ветра
        weather =  cond_change(condition) + '\n' + '\U0001F321  Температура от ' + str(temp_min) + '°C до ' + str(temp_max) + "°C\n\t  По ощущениям как "+ str(feels_like) + "°C\n\t   Влажность воздуха " + str(humidity) + "%\n\U0001F32C  Ветер " + wind_change(wind_dir) + ', ' + str(wind) + ' м/с'
    return weather





def write_message(chat, message, keyboard = None):  # функция отправки сообщения в чат ,получает его номер и сообщение
    post = {
        "chat_id": chat,
        "message": message,
        "random_id": 0
    }

    if keyboard != None:
        post["keyboard"] = keyboard.get_keyboard()
    else:
        post = post

    authorize.method("messages.send", post)


authorize = vk_api.VkApi(token=token)  # авторизируем бота через токен
getting_api = authorize.get_api()
longpoll = VkBotLongPoll(authorize, group_id="216563568")  # отправляем запрос на сервер с помощью технологии long polling
print("Бот запущен!")


def menu(reseived_message):
    keyboard = VkKeyboard()  # добавить клавиатуру


    if reseived_message == "начать":
        keyboard.add_button("Текущая") # добавить кнопку
        keyboard.add_line() # добавить линию
        keyboard.add_button("Сегодня")
        keyboard.add_button("Завтра")
        keyboard.add_button("3 дня")
        keyboard.add_button("Неделя")
        #keyboard.add_location_button()  # добавить кнопку "геолокации" белого цвета
        write_message(chat, "Вас приветствует бот прогноза погоды!", keyboard)

    if reseived_message.endswith('сегодня'): # если в конце сообщения будет "сегодня"
        print("Погода на сегодня отправлена в ", chat)
        write_message(chat, print_weather(6, 0))

    elif reseived_message.endswith('3дня'):
        print("Погода на 3 дня отправлена в ", chat)
        for i in range(3):
            write_message(chat, print_weather(3, i))

    elif reseived_message.endswith('неделя'):
        print("Погода на неделю отправлена в ", chat)
        for i in range(7):
            write_message(chat, print_weather(7, i))

    elif reseived_message.endswith('текущая'):
        print("Текущая погода отправлена в ", chat)
        weather = get_apis(2)
        write_message(chat, get_numbers(weather))

    elif reseived_message.endswith('завтра'):
        print("Погода на завтра отправлена в ", chat)
        write_message(chat, print_weather(2, 1))

for event in longpoll.listen():  # ждем от сервера ответа о произошедшем событии
    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get('text'):
        # если тип ивента это новое сообщение, оно из чата и сообщение в ивенте текстовое

        reseived_message = event.message.get('text')  # то сохраняем полученное сообщение
        reseived_message = reseived_message.translate({ord(c): None for c in string.whitespace})  # если было введено раздельно, убрали пробелы

        chat = event.chat_id  # сохраняем номер чата
        print('из чата', chat)
        menu(reseived_message.lower())
