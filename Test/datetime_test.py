from datetime import datetime

# getting the date and time today
date_today = datetime.today()
x = bool("True")
print(x)
x = "True"
print(x)

# getting the date and time in the file
with open("Database/PreviousDate.txt", "r") as file:
    date_in_file = datetime.strptime(' '.join(file.readline().split('-')), "%Y %m %d")
    
# checking the date today and the date in the file
if date_today.date() == date_in_file.date():
    print(f"The date today is: {date_today}")
elif date_today.date() > date_in_file.date():
    days_between = date_today - date_in_file
    print(f"The date is a new day and it is: {date_today}")
    print(f"The number of days passed is: {days_between.days} days")

    # changes the date in the file into date today
    # with open("Database/PreviousDate.txt", "w") as file:
    #     file.write(str(date_today.date()))