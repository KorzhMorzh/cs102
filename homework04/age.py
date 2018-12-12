from datetime import date
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    friends = get_friends(user_id, 'bdate')['items']
    friendslist = []
    for j in range(len(friends)):
        friendslist.append(User(**friends[j]))
    ageslist = []
    bdateslist: list = []
    for j in range(len(friendslist)):
        bdateslist.append([])
        try:
            bdateslist[j] = friendslist[j].bdate
        except Exception:
            pass
    for i in range(len(bdateslist)):
        try:
            dates = bdateslist[i].split('.')
            day = int(dates[0])
            month = int(dates[1])
            year = int(dates[2])
            today = date.today()
            if (month > int(today.month)) | \
                    (month == int(today.month)) & (day > int(today.day)):
                ageslist.append(int(today.year) - year - 1)
            else:
                ageslist.append((int(today.year - year)))
        except Exception:
            pass
    if len(ageslist) != 0:
        return median(ageslist)
    else:
        return None
