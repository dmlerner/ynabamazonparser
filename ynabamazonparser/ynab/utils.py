import datetime
import ynabamazonparser as yap


def parse_money(price):
    assert isinstance(price, int)
    return price / 1000


def to_milliunits(p):
    return int(p * 1000)


date_format = '%Y-%m-%d'


def parse_date(d):
    return yap.utils.parse_date(d, date_format)


def format_date(d):
    return yap.utils.format_date(d, date_format)


def first_of_coming_month():
    now = yap.utils.now()
    next_month = now.month + 1
    if next_month == 13:
        next_month = 1
    return datetime.datetime(now.year + next_month == 1, next_month, 1)
