import vk
import time
import datetime

from WeatherReporter import WeatherReporter

print('VKBot')

# Авторизуем ссесию с помощью access токена
session = vk.Session('key')

# Создаем объект API
api = vk.API(session)

weatherReporter = WeatherReporter("key")

def DoesStringRepresentInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

while True:
    # Получим 20 последних входящих сообщений
    messages = api.messages.get()


    # Найдем среди них непрочитанные сообщения с поддерживаемыми командами
    # такими образом получим список в формате [(id_пользователя, id_сообщения, команда), ...]
    messages = [(m['uid'], m['mid'], m['body'])
                for m in messages[1:] if m['read_state'] == 0]

    # Отвечаем на полученные команды
    for m in messages:
        user_id = m[0]
        message_id = m[1]
        comand = m[2]

        # Сформируем строку с датой и временем сервера
        data_time_string = datetime.datetime.now().strftime('[%Y=%m-%d %H:%M:^s]')

        if comand == 'help':
            api.messages.send(user_id=user_id,
                              message=data_time_string + '\n>VKBot v0.1\n>Разработал: LittleDani')
        if comand == 'привет':
            api.messages.send(user_id=user_id,
                              message=data_time_string + '\n>Занята, напишите позже\n>VKBot')
        else:
            report = ""
            report = ' '.join(report)
            if DoesStringRepresentInt(comand):
                status, report = weatherReporter.GetWeatherReportByID(int(comand))
            else:
                status, report = weatherReporter.GetWeatherReportByPlaceName(comand)
            api.messages.send(user_id=user_id, message=data_time_string + '\n' + report)
                                                                    

    # Формируем список id всех сообщений с командами через запятую
    ids = ', '.join([str(m[1]) for m in messages])

    # Помечаем полученные сообщения как прочитанные
    if ids:
        api.messages.markAsRead(message_ids=ids)

    # Проверяем сообщения каждые 3 секунды
    time.sleep(3)
