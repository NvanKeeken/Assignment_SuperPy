from report import reset_inventory, add_to_csv, make_inventory, show_Inventory
import datetime
from advance import get_date_file
import csv

# This file contains all the functions for the option --expired 

# this function checks if a product is expired 
def expiration_check(row):
     current_date = datetime.datetime.strptime(get_date_file(), "%Y-%m-%d")
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
   if (current_date - row_date).days == days_before_expiring:
        is_expired += True
   else:
        is_expired += False
   return is_expired
   
""" this function filters the inventory for expired products if default of 0 days is passed
else for products that will expire in the amount of days passed 
if days is bigger then 0. These products will be shown in in the CLI """
def get_expired_products(days):
    expired_products = []
    with open("Invent.csv", "r") as inventoryfile:
        reader = csv.DictReader(inventoryfile)
        for row in reader:
          if days == "0" and expiration_check(row):
            expired_products.append(row)
          elif days > "0" and expiring_in_future(row,days):
              expired_products.append(row)
    show_Inventory(expired_products)

