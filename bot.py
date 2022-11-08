import vk_api
import config
import urllib
import json
import requests as req
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import string
import array


token = config.settings['TOKEN']    # присваиваем переменной значение токена из файла конфига
group_id=config.settings['group_id']             # id выбранной для работы бота группы

def get_apis(period):
     # объявляем лист для хранения апи погоды
    url = config.api[0] #берем первую ссылку на апи
    #print(url)
    json_data = urllib.request.urlopen(url).read()  # читаем данные из JSON полученного из нашей ссылки
    weather = []
    weather.append(json.loads(json_data)) #добавляем в конец листа наш JSON
    key = config.settings['yan_key']
    url = config.api[1]
    yandex_req = req.get(url, headers={'X-Yandex-API-Key': key}, verify=False)
    json_data = yandex_req.text
    weather.append(json.loads(json_data))
    if period >= 3:
        for i in range(period):
            url = config.api[i+2]
            json_data = urllib.request.urlopen(url).read()
            weather.append(json.loads(json_data))
   # print(weather)
    return weather

def get_numbers(weather):
    current_weather = weather[0]['data'][0]
    wind_spd = array.array('f') #массив для скорости ветра типа float
    temp = array.array('f') #массив для температуры типа float
    wind_spd.append(current_weather['wind_spd'])  # скорость ветра
    wind_spd.append(weather[1]['forecasts'][0]['parts']['morning']['wind_speed'])
    wind_spd1 = comparison(wind_spd)
    temp.append(current_weather['app_temp'])  # температура
    temp.append(weather[1]['forecasts'][0]['parts']['morning']['temp_avg'])
    temp1 = comparison(temp)
    # можно ли будет добавить направление ветра?
    date = weather[1]['date']
    wind_dir =weather[1]['parts']['morning']['wind_dir']
    weather = date + '\n' + 'Температура - ' + str(temp1) + 'C \n' + "Ветер - " + wind_change(wind_dir) + '\nСкорость ветра - ' + str(wind_spd1) + ' м/с'
    return weather

def comparison(num):

    average=sum(num)/len(num)

    return average

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

def wind_change(wind_dir):
    if wind_dir =="sw":
        dir="Юго-западный"
    if wind_dir =="se":
        dir="Юго-восточный"
    if wind_dir =="s":
        dir="Южный"
    if wind_dir =="n":
        dir="Северный"
    if wind_dir =="ne":
        dir="Северо-восточный"
    if wind_dir =="nw":
        dir="Северо-западный"
    if wind_dir =="w":
        dir="Западный"
    if wind_dir =="e":
        dir="Восточный"
    return dir

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
            weather = date + '\n' + desc + ' - ' + str(temp) + 'C \n' + "Ветер - " + wind + '\nСкорость ветра - ' + str(wind_spd) + ' м/с'
        elif period == 7:
            temp = current_weather['app_max_temp']
            weather = date + '\n' + desc + ' - ' + 'макс. температура - ' + str(temp) + 'C \n' + "Ветер - " + wind + '\nСкорость ветра - ' + str(wind_spd) + ' м/с'
    elif period == 6 or 3:
        current_weather = data[1]['forecasts'][i]
        date = current_weather['date']
        temp = current_weather['parts']['morning']['temp_avg']
        wind = current_weather['parts']['morning']['wind_speed']
        wind_dir = current_weather['parts']['morning']['wind_dir']
        weather = date + '\n' + 'Температура - ' + str(temp) + 'C \n' + "Ветер - " + wind_change(wind_dir) + '\nСкорость ветра - ' + str(wind) + ' м/с'
    # print(weather)
    return weather


def write_message(chat, message):                           # функция отправки сообщения в чат ,получает его номер и сообщение
    authorize.method('messages.send', {'chat_id': chat, 'message': message, 'random_id': get_random_id()})
    # используем функцию внутри апи по отправки сообщений,принимающую номер чата,сообщение и рандомный id

authorize = vk_api.VkApi(token = token)                        # авторизируем бота через токен
getting_api = authorize.get_api()
longpoll = VkBotLongPoll(authorize, group_id="216563568")      # отправляем запрос на сервер с помощью технологии long polling
print("Бот запущен!")

def menu(reseived_message):

    if reseived_message=="привет":    
        write_message(chat, "Вас приветствует бот прогноза погоды. Хотите узнать прогноз? \nда \nнет")

    elif reseived_message == "нет":
        write_message(chat, "До свидания!")

    elif reseived_message == "да":
        write_message(chat, "Выберите период \n6 часов \nзавтра \n3 дня \nнеделя \nтекущая")

    if reseived_message == "6часов":
        write_message(chat, "Ваш прогноз:")
        print("Погода на 6 часов отправлена в ", chat)
        write_message(chat, print_weather(6,0))

    elif reseived_message == "3дня":
        write_message(chat, "Ваш прогноз:")
        print("Погода на 3 дня отправлена в ", chat)
        for i in range(3):
            write_message(chat, print_weather(3, i))

    elif reseived_message == "неделя":
        print("Погода на неделю отправлена в ", chat)
        write_message(chat, "Ваш прогноз:")
        for i in range(7):
         write_message(chat, print_weather(7,i))

    elif reseived_message == "текущая":
        print("Текущая погода отправлена в ", chat)
        weather = get_apis(2)
        write_message(chat, get_numbers(weather))


for event in longpoll.listen():                               # ждем от сервера ответа о произошедшем событии
    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get('text'): 
        # если тип ивента это новое сообщение, оно из чата и сообщение в ивенте текстовое
       
        reseived_message = event.message.get('text')            # то сохраняем полученное сообщение
        reseived_message=reseived_message.translate({ord(c): None for c in string.whitespace})       # если было введено раздельно, убрали пробелы

        chat = event.chat_id                                    # сохраняем номер чата
        print('из чата', chat)
        from_id = event.message.get('from_id')
        menu(reseived_message.lower())
