import datetime as dt
import calendar


# this file contains all the functions related to the advance subparser and date in general

# this function advances the date in the currentDate file by the number of days pased in CLI 
def advance_time(day=0):
    date_today = dt.datetime.strptime(get_date_file(), "%Y-%m-%d")
    advanced_date = date_today + dt.timedelta(days = day)
    with open("currentDate.txt", "w") as file:
            file.write(advanced_date.strftime("%Y-%m-%d"))

# this function sets the date in currentDate file to the date of today
def set_date_today():
      with open("currentDate.txt", "w") as file:
            date_today= dt.date.today()
            file.write(date_today.strftime("%Y-%m-%d"))

# this function fetches date of today
def get_date_now():
     return dt.date.today().strftime("%Y-%m-%d")

# this function fetches the date of yesterday based on the date in currentDate file
def get_date_yesterday():
      current_date = get_date_file()
      yesterday_date = dt.datetime.strptime(current_date, "%Y-%m-%d") - dt.timedelta(days = 1)
      return yesterday_date.strftime("%Y-%m-%d")

# this function fetches the date in currentDate file
def get_date_file():
      with open("currentDate.txt", "r") as f:
            for line in f.readlines():
                return line

""" this function returns the format the passed date is in, if the passed date is 
not formatted in the allowed formats %Y-%m-%d, %Y-%m or %Y a ValueError is raised """
def get_date_Format(date):     
    try:
      if date == dt.datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d"):
            return "%Y-%m-%d"
    except ValueError:
      try:
          if date == dt.datetime.strptime(date, "%Y-%m").strftime("%Y-%m"):
            return "%Y-%m"
      except ValueError:
           try:
               if date == dt.datetime.strptime(date, "%Y").strftime("%Y"):
                  return "%Y"
           except ValueError:
                raise ValueError("Format must be 'YYYY-MM-DD', 'YYYY-MM' or 'YYYY'")
           
# This function sets date currentDate file to a specific date with the --set_date option
def set_date_file(date):
      if get_date_Format(date) == "%Y-%m-%d":
          with open("currentDate.txt", "w") as file:
               date_today= dt.datetime.strptime(date, "%Y-%m-%d")
               file.write(date_today.strftime("%Y-%m-%d"))
      else:
           raise ValueError("Format must be 'YYYY-MM-DD'")
      
# this function converts month number into the written form and return for example the string "May 2023"
def get_month(date):
     date_format = get_date_Format(date)
     if date_format == "%Y-%m":
        month = int(dt.datetime.strptime(date, "%Y-%m").strftime("%m").lstrip("0").replace(" 0", " "))
        year = dt.datetime.strptime(date, "%Y-%m").strftime("%Y")
        return calendar.month_name[month] +" " + year
     else:
          return date
                  
        
