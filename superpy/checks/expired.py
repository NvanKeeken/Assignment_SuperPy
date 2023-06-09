# from report import reset_inventory, add_to_csv, make_inventory, show_Inventory
import datetime
from advance import get_date_file

# This file contains all the functions for the option --expired 

# this function checks if a product is expired 
def expiration_check(row, date= get_date_file()):
     current_date = datetime.datetime.strptime(date, "%Y-%m-%d")
     row_date = datetime.datetime.strptime(row["Expiration Date"], "%Y-%m-%d")
     is_expired= False
     if row_date.date() < current_date.date():
        is_expired += True
     else:
        is_expired += False
     return is_expired

# this function checks if a product is expired in the amount of days passed
def expiring_in_future(row,days_before_expiring):
   current_date = datetime.datetime.strptime(get_date_file(), "%Y-%m-%d")
   row_date = datetime.datetime.strptime(row["Expiration Date"], "%Y-%m-%d")
   is_expired= False
   if (current_date - row_date).days == int(days_before_expiring):
        is_expired += True
   else:
        is_expired += False
   return is_expired
