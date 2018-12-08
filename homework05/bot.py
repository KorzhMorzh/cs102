import telebot
import requests
import config
from bs4 import BeautifulSoup
import datetime
from time import sleep
from typing import Union, Tuple


# Создание бота с указанным токеном доступа
bot: telebot = telebot.TeleBot(config.access_token)
cache: dict = {}


def get_page(group: str, week: str = '') -> list:
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group.upper())
    if url in cache:
        response = cache[url]
    else:
        response = requests.get(url)
    web_page = response.text
    sleep(0.1)
    return web_page


def parse_schedule(web_page: list, day: str) -> Union[Tuple, int]:
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": day})
    try:
        times_list = schedule_table.find_all("td",
                                             attrs={"class": "time"})
    except AttributeError:
        return -1
    else:
        # Время проведения занятий
        times_list = [time.span.text for time in times_list]

        # Место проведения занятий
        locations_list = schedule_table.find_all("td",
                                                 attrs={"class": "room"})
        locations_list = [room.span.text for room in locations_list]

        # Название дисциплин и имена преподавателей
        lessons_list = schedule_table.find_all("td",
                                               attrs={"class": "lesson"})
        lessons_list = [lesson.text.replace('\n', '').replace('\t', '')
                        for lesson in lessons_list]
        # Аудитория
        rooms_list = schedule_table.find_all("td",
                                             attrs={"class": "room"})
        rooms_list = [room.dd.text for room in rooms_list]
    return times_list, locations_list, rooms_list, lessons_list


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday',
                               'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message: telebot.types.Message) -> telebot.types.Message:
    """ Получить расписание на указанный день """
    try:
        command, week, group = message.text.split()
    except ValueError:
        week = '0'
        try:
            command, group = message.text.split()
        except ValueError:
            return bot.send_message(message.chat.id,
                                    "Неверный запрос",
                                    parse_mode='HTML')
    if len(group) != 5:
        return bot.send_message(message.chat.id,
                                'Неверно указана группа',
                                parse_mode='HTML')
    days = {'/monday': '1day', '/tuesday': '2day',
            '/wednesday': '3day', '/thursday': '4day', '/friday': '5day',
            '/saturday': '6day', '/sunday': '7day'}
    web_page = get_page(group, week)
    day = days[command]
    if parse_schedule(web_page, day) == -1:
        return bot.send_message(message.chat.id, 'В этот день пар нет',
                                parse_mode='HTML')
    else:
        times_lst, locations_lst, rooms_lst, lessons_lst = \
            parse_schedule(web_page, day)
        resp = ''
        for time, location, room, lesson in \
                zip(times_lst, locations_lst, rooms_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}, {}\n'.\
                format(time, location, room, lesson)
        return bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message: telebot.types.Message) -> telebot.types.Message:
    """ Получить расписание на всю неделю для указанной группы """
    if len(message.text.split()) != 1 and len(message.text.split()) <= 3:
        try:
            _, week, group = message.text.split()
        except ValueError:
            week = ''
            _, group = message.text.split()
        if len(group) != 5:
            return bot.send_message(message.chat.id,
                                    'Неверно указана группа',
                                    parse_mode='HTML')
        week_list = ['1day', '2day', '3day', '4day', '5day', '6day']
        days = ['Понедельник', 'Вторник', 'Среда', 'Четверг',
                'Пятница', 'Суббота']
        web_page = get_page(group, week)
        resp = ''
        for i in range(6):
            resp += '<b>' + days[i] + '</b> ' + ':\n'
            if parse_schedule(web_page, week_list[i]) == -1:
                resp += 'В этот день пар нет\n'
            else:
                try:
                    times_lst, locations_lst, room_lst, \
                     lessons_lst = parse_schedule(web_page, week_list[i])
                    for time, location, room, lesson in \
                            zip(times_lst, locations_lst,
                                room_lst, lessons_lst):
                        resp += '<b>{}</b>, {}, {}, {}\n'.\
                            format(time, location, room, lesson)
                except TypeError:
                    pass
            resp += '\n'
        return bot.send_message(message.chat.id, resp, parse_mode='HTML')
    else:
        return bot.send_message(message.chat.id,
                                'Неверный запрос', parse_mode='HTML')


def get_date(group: str, tomorrow: bool = False, today_: str = '') \
        -> tuple:
    web_page = get_page(group)
    soup = BeautifulSoup(web_page, "html5lib")
    date_ = soup.find("h2", class_="schedule-week")
    week = date_.find("strong").text
    if week == 'Нечетная':
        week = str(2)
    else:
        week = str(1)
    today = datetime.datetime.today().strftime('%Y-%m-%d').split('-')
    day = datetime.date(int(today[0]), int(today[1]), int(today[2])).weekday()
    if tomorrow:
        if today_ == '':
            day_str = str(day + 2) + "day"
        else:
            today_, _ = today_.split('d')
            day_str = str(int(today_) + 2) + "day"
        if day_str == "7day" or day_str == "1day":
            day_str = "1day"
            if week == '2':
                week = str(1)
            else:
                week = str(2)
    else:
        if today_ == '':
            day_str = str(day + 1) + "day"
        else:
            today_, _ = today_.split('d')
            day_str = str(int(today_) + 1) + "day"
    return week, day_str


@bot.message_handler(commands=['tomorrow'])
def get_tomorrow(message: telebot.types.Message) -> telebot.types.Message:
    if len(message.text.split()) == 1 or len(message.text.split()) > 2:
        return bot.send_message(message.chat.id,
                                "Неверный запрос", parse_mode='HTML')
    _, group = message.text.split()
    if len(group) != 5:
        return bot.send_message(message.chat.id,
                                'Неверно указана группа', parse_mode='HTML')
    week, day = get_date(group, tomorrow=True)
    web_page = get_page(group, week)
    if parse_schedule(web_page, day) == -1:
        return bot.send_message(message.chat.id,
                                'В следующий учебный день пар нет',
                                parse_mode='HTML')
    else:
        times_lst, locations_lst, rooms_lst, \
         lessons_lst = parse_schedule(web_page, day)
        resp = ''
        for time, location, room, lession in \
                zip(times_lst, locations_lst, rooms_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}, {}\n'.\
                format(time, location, room, lession)
        return bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message: telebot.types.Message) -> telebot.types.Message:
    """ Получить ближайшее занятие """
    if len(message.text.split()) == 1 or len(message.text.split()) > 2:
        return bot.send_message(message.chat.id,
                                "Неверный запрос", parse_mode='HTML')
    _, group = message.text.split()
    if len(group) != 5:
        return bot.send_message(message.chat.id,
                                'Неверно указана группа', parse_mode='HTML')
    week, day = get_date(group)
    web_page = get_page(group, week)
    now = int(str(datetime.datetime.now().hour)) * 60 + \
        int(str(datetime.datetime.now().minute))
    i = 0
    days = {'1day': 'Понедельник', '2day': 'Вторник',
            '3day': 'Среда', '4day': 'Четверг',
            '5day': 'Пятница', '6day': 'Суббота'}
    while parse_schedule(web_page, day) == -1:
        week, day = get_date(group, tomorrow=True, today_=day)
        web_page = get_page(group, week)
        now = 0
        i += 1
        if i == 6:
            return bot.send_message(message.chat.id,
                                    'Расписание не найдено',
                                    parse_mode='HTML')
    times_list, locations_list, lessons_list, \
        rooms_list = parse_schedule(web_page, day)
    resp = ''
    while True:
        for counter, j in enumerate(times_list):
            if j == 'День':
                continue
            time, _ = j.split('-')
            t1, t2 = time.split(':')
            time = int(t1) * 60 + int(t2)
            if now < time:
                resp += '<b>' + days[day] + '</b> ' + ':\n'
                resp += '<b>{}</b>, {}, {}, {}\n' \
                    .format(times_list[counter], locations_list[counter],
                            lessons_list[counter], rooms_list[counter])
                return bot.send_message(message.chat.id, resp,
                                        parse_mode='HTML')
        week, day = get_date(group, tomorrow=True)
        i = 0
        while parse_schedule(web_page, day) == -1:
            week, day = get_date(group, tomorrow=True, today_=day)
            web_page = get_page(group, week)
            i += 1
            if i == 6:
                return bot.send_message(message.chat.id,
                                        'Расписание не найдено',
                                        parse_mode='HTML')
        web_page = get_page(group, week)
        try:
            times_list, locations_list, lessons_list, \
                rooms_list = parse_schedule(web_page, day)
        except TypeError:
            pass
        now = 0


if __name__ == '__main__':
    bot.polling(none_stop=True)
