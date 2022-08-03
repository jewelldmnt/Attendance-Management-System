from datetime import *


def get_strmonth_today() -> str:
    return datetime.today().date().strftime("%B")

def get_strdate_today() -> str:
    return datetime.today().date().strftime("%m-%d-%Y")

def get_strtime_today() -> str:
    return datetime.today().time().strftime("%H:%M")

def get_stryear_today() -> str:
    return str(datetime.today().year)

def convert_to_strdate(_date) -> str:
    return _date.strftime("%m/%d/%Y")

def convert_to_strtime(_time) -> str:
    return _time.strftime("%H:%M")

def convert_to_datetime(strdate) -> datetime:
    return datetime.strptime(strdate, "%m/%d/%Y")

def get_date_today() -> date:
    return datetime.today().date()

def get_time_today() -> time:
    return datetime.today().time()

def convert_to_time(strtime) -> time:
    return datetime.strptime(strtime, "%H:%M").time()

def make_time(hours, mins) -> time:
    return time(hours, mins)
