import vk_api
import config
import urllib
import json
import requests as req
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import string
import array

token = config.settings['TOKEN']  # присваиваем переменной значение токена из файла конфига
group_id = config.settings['group_id']  # id выбранной для работы бота группы
url=[]

for i in range(3):
    url.append(config.api[i])

сoord=config.api[0][39:68]

latitude=сoord[4:14] #'56.3264816'
longtitude=сoord[19:29]#'44.0051395'
print(сoord,' ',latitude,' ',longtitude)

newlat='66.66666'
newlong='69.6969'
def setnewcoord(newlat,newlong):
    new = []
    for i in range(3):
        new.append(url[i])
        new[i]=url[i].replace(longtitude, newlong)
        new[i] = new[i].replace(latitude, newlat)
        print(new[i])
        url[i]=new[i]

def get_apis(period,url):
    # объявляем лист для хранения апи погоды
    weather = []
    if period==7:

        json_data = urllib.request.urlopen(url[0]).read()  # читаем данные из JSON полученного из нашей ссылки
        weather.append(json.loads(json_data))  # добавляем в конец листа наш JSON

        json_data = urllib.request.urlopen(url[2]).read()
        weather.append(json.loads(json_data))

    key = config.settings['yan_key']

    yandex_req = req.get(url[1], headers={'X-Yandex-API-Key': key}, verify=False)
    json_data = yandex_req.text
    weather.append(json.loads(json_data))

    # print(weather)
    return weather


def get_numbers(weather):
    current_weather = weather[0]['data'][0]
    wind_spd = array.array('f')  # массив для скорости ветра типа float
    temp = array.array('f')  # массив для температуры типа float

    wind_spd.append(current_weather['wind_spd'])  # скорость ветра 1 апи
    wind_spd.append(weather[2]['forecasts'][0]['parts']['morning']['wind_speed'])  # 2 апи
    wind_spd.append(weather[1]['days'][0]['windspeed'])
    wind_spd1 = comparison(wind_spd)
    wind_spd1 = toFixed(wind_spd1, 2)

    temp.append(current_weather['app_temp'])  # температура 1 апи
    temp.append(weather[2]['forecasts'][0]['parts']['morning']['temp_avg'])  # 2 апи
    temp.append(weather[1]['days'][0]['temp'])  # 3 апи

    temp1 = comparison(temp)
    temp1 = toFixed(temp1, 2)
    # можно ли будет добавить направление ветра?
    date = weather[2]['forecasts'][0]['date']
    wind_dir = weather[2]['forecasts'][0]['parts']['morning']['wind_dir']
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
        cond = "Ясно \U00002600"
    if condition == "partly-cloudy":
        cond = "Малооблачно \U000026C5"
    if condition == "cloudy":
        cond = "Облачно с прояснениями \U0001F324"
    if condition == "overcast":
        cond = "Пасмурно \U00002601"
    if condition == "drizzle":
        cond = "Морось \U0001F327"
    if condition == "light-rain":
        cond = "Небольшой дождь \U0001F326"
    if condition == "rain":
        cond = "Дождь \U0001F327"
    if condition == "moderate-rain":
        cond = "Умеренно сильный дождь \U0001F327"
    if condition == "heavy-rain":
        cond = "Сильный дождь \U0001F327"
    if condition == "continuous-heavy-rain":
        cond = "Длительный сильный дождьм \U0001F327"
    if condition == "showers":
        cond = "Ливень \U0001F327"
    if condition == "wet-snow":
        cond = "Дождь со снегом \U0001F328"
    if condition == "light-snow":
        cond = "Небольшой снег \U0001F328"
    if condition == "snow":
        cond = "Снег \U00002744"
    if condition == "snow-showers":
        cond = "Снегопад \U0001F328"
    if condition == "hail":
        cond = "Град \U0001F327"
    if condition == "thunderstorm":
        cond = "Гроза \U0001F329"
    if condition == "thunderstorm-with-rain":
        cond = "Дождь с грозой \U000026C8"
    if condition == "thunderstorm-with-hail":
        cond = "Гроза с градом \U000026C8"
    return cond

def print_weather(period, i):  # функция получения текущего города
    # print(data)
    data = get_apis(2,url)
    if period == 7:
        current_weather = data[0]['data'][i]  # выбираем нужную нам часть с данными
        date = current_weather['datetime']
        desc = current_weather['weather']['description']
        wind = current_weather['wind_cdir_full']
        wind_spd = current_weather['wind_spd']
        wind_spd = toFixed(wind_spd, 2)
        temp = current_weather['app_max_temp']
        weather = date + '\n' + desc + ' - ' + '\nмакс. температура - ' + str(temp) + '°C \n' + "Ветер - " + wind + '\nСкорость ветра - ' + str(wind_spd) + ' м/с'

    elif period == 1 or 3 or 2:
        current_weather = data[0]['forecasts'][i]
        #date = current_weather['date'] # дата погоды
        condition = current_weather['parts']['day_short']['condition'] # погодное описание
        #icon = current_weather['parts']['day_short']['icon'] # иконка погоды
        temp_min = current_weather['parts']['day_short']['temp_min'] # мин температура
        feels_like = current_weather['parts']['day_short']['feels_like'] # ощущается как
        humidity = current_weather['parts']['day_short']['humidity'] # влажность воздуха
        temp_max = current_weather['parts']['day_short']['temp'] # макс температура
        wind = current_weather['parts']['day_short']['wind_speed'] # скорость ветра
        wind_dir = current_weather['parts']['morning']['wind_dir'] # направление ветра
        weather = cond_change(condition) + '\n' + 'Температура от ' + str(temp_min) + '°C до ' + str(temp_max) + "°C\n\t  По ощущениям как "+ str(feels_like) + "°C\n\t   Влажность воздуха " + str(humidity) + "%\nВетер " + wind_change(wind_dir) + ', ' + str(wind) + ' м/с'
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
        write_message(chat, print_weather(1, 0))

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
        weather = get_apis(7)
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
