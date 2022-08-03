from datetime import datetime
from . import DateManip


# getting previous date
def is_new_day() -> bool:
    date_today = DateManip.get_date_today()
    # getting the date and time in the file
    with open("Database/PreviousDate.txt", "r") as file:
        date_in_file = datetime.strptime(' '.join(file.readline().split('-')), "%Y %m %d").date()
        
    # changes the date in the file into date today
    if date_today > date_in_file:
        with open("Database/PreviousDate.txt", "w") as file:
            file.write(str(date_today))
        return True
    
    # date today is the dame as the date in the file
    return False


# checks if there is daily login and make the employee's daily login to false
def have_daily_login(id) -> bool:
    ret = False
    lines = get_allinfo_from_txt("Database/DailyLogin.txt")
    with open("Database/DailyLogin.txt", "w") as file:
        for line in lines:
            _id, daily_login = line.rstrip("\n").split(",")
            if _id == id and daily_login == "True":
                ret = True
                daily_login = "False"
                file.write(f"{_id},{daily_login}\n")
            else:
                file.write(line)   

    # employee have logged in already for that day           
    return ret


# check if employee have timeout
def have_timeout(id) -> bool:
    with open("Database/TimeOut.txt", "r") as file:
        for line in file:
            _id, timeout = line.rstrip("\n").split(",")
            if _id == id and timeout == "True":
                return True
    # does not have time out
    return False


# get the name of the one who logged in
def get_name(id) -> str:
    with open("Database/Attendance.txt", "r") as file:
        for line in file:
            _id, info = line.split(",")
            if id == _id:
                name, _ = info.split("|")
                return name


# get the recorder time out of the user
def get_timeout(id, strdate=DateManip.get_strdate_today()) -> str|None:
    with open("Database/Attendance.txt", "r") as file:
        info_list = []
        for line in file:
            _id, info = line.split(",")
            if id == _id:
                info_list = info.split("|")[1].split("/")
                break
        
        for x in info_list:
            if x.startswith(strdate):
                return x.split(";")[2].rstrip("\n")


# get the logged time in by user
def get_timein(id, strdate=DateManip.get_strdate_today()) -> str:
    with open("Database/Attendance.txt", "r") as file:
        info_list = []
        for line in file:
            _id, info = line.split(",")
            if id == _id:
                info_list = info.split("|")[1].split("/")
                break
    
        for x in info_list:
            if x.startswith(strdate):
                return x.split(";")[1].rstrip("\n")


# add time out to the employee info
def add_timeout(id) -> str:
    # writing the added info about employee
    lines = get_allinfo_from_txt("Database/Attendance.txt")
    with open("Database/Attendance.txt", "w") as file:
        for line in lines:
            _id, info = line.rstrip("\n").split(",")
            # if id is not equal to the passed id
            if id != _id:
                file.write(line)
                continue

            current_date = DateManip.get_strdate_today()
            current_time = DateManip.get_strtime_today()
            name, datetime_info = info.split("|")
            temp = f"{_id},{name}|"
            for x in datetime_info.split("/"):
                if x.startswith(current_date):
                    temp += x + ";" + current_time + "/"
                else:
                    temp += x + "/"

            file.write(temp.rstrip("/") + "\n")
    # return time out of employee
    return current_time


# adding time in to the employee info
def add_timein(id) -> list:
    lines = get_allinfo_from_txt("Database/Attendance.txt")
    with open("Database/Attendance.txt", "w") as file:
        for line in lines:
            _id, datetime_info = line.rstrip("\n").split(",")
            if _id != id:
                file.write(line)
                continue

            _, datetime_list = datetime_info.split("|")
            current_date = DateManip.get_strdate_today()
            current_time = DateManip.get_strtime_today()
            temp = line.rstrip("\n")
            if datetime_list != "":
                temp += f"/{current_date};{current_time}"
            else:
                temp += f"{current_date};{current_time}"
            file.write(temp + "\n")
    
    return [current_date, current_time]


# make the employee's daily timeout to false
def change_timeout(id) -> None:
    lines = get_allinfo_from_txt("Database/TimeOut.txt")
    with open("Database/TimeOut.txt", "w") as file:
        for line in lines:
            _id, timeout = line.rstrip("\n").split(",")
            if _id == id and timeout == "True":
                timeout = "False"
                file.write(f"{_id},{timeout}\n")
            else:
                file.write(line)


# reset time out of every employee
def reset_timeout() -> None:
    lines = get_allinfo_from_txt("Database/TimeOut.txt")
    with open("Database/TimeOut.txt", "w") as file:
        for line in lines:
            _id, timeout = line.split(",")
            timeout = "True\n"
            file.write(f"{_id},{timeout}")


# reset daily logins of every employee
def reset_daily_login() -> None:
    lines = get_allinfo_from_txt("Database/DailyLogin.txt")
    with open("Database/DailyLogin.txt", "w") as file:
        for line in lines:
            _id, daily_login = line.split(",")
            daily_login = "True\n"
            file.write(f"{_id},{daily_login}")


# get all info in attendance.txt
def get_allinfo_from_txt(filename):
    with open(filename, "r") as file:
        return file.readlines()