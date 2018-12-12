import datetime
from datetime import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from typing import List, Tuple

from api import messages_get_history
from api_models import Message
import config

Dates = List[datetime.date]
Frequencies = List[int]

plotly.tools.set_credentials_file(
    username=config.PLOTLY_CONFIG['username'],
    api_key=config.PLOTLY_CONFIG['api_key']
)


def fromtimestamp(ts: int) -> datetime.date:
    return datetime.datetime.fromtimestamp(ts).date()


def count_dates_from_messages(messages: List[Message]) \
        -> Tuple[Dates, Frequencies]:
    """ Получить список дат и их частот
    :param messages: список сообщений
    """
    dateslist: list = []
    datescount = []
    for i in range(len(messages)):
        message = messages[i]
        date = datetime.fromtimestamp(message.date).strftime("%Y-%m-%d")
        if date not in dateslist:
            dateslist.append(date)
            datescount.append(1)
        else:
            j = dateslist.index(date)
            datescount[j] += 1
    return dateslist, datescount


def plotly_messages_freq(dates: Dates, freq: Frequencies) -> None:
    """ Построение графика с помощью Plot.ly
    :param dates: список дат

    :param freq: число сообщений в соответствующую дату
    """
    data = [go.Scatter(x=dates, y=freq)]
    try:
        py.iplot(data)
    except KeyError:
        pass


def get_list_of_messages(user_id: int, offset: int = 0,
                         count: int = 20) -> List[Message]:
    messages = messages_get_history(user_id, offset, count)
    messages_list = []
    for j in range(len(messages)):
        messages_list.append(Message(**messages[j]))
    return messages_list


plotly_messages_freq(count_dates_from_messages
                     (get_list_of_messages(79828756, 0, 201))[0],
                     count_dates_from_messages
                     (get_list_of_messages(79828756, 0, 201))[1])
