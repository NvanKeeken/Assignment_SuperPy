import csv
from sell import get_file_id
from advance import get_date_file
from report import make_inventory
from rich.console import Console
console= Console()

# this file contains all functionality for subparser buy

"""this functions adds passed bought product to the bought.csv and calls add_to_inventory 
function to add it to inventory.csv """
def buy_product(product_name, buy_price, expiration_date, amount, buy_date = get_date_file()):
    if check_product_already_bought(product_name, expiration_date):
       console.print("Error: Product with this expiration date has already been bought", style="red")
    else:
       with open("bought.csv", 'a', newline="") as file:
         writer = csv.writer(file, lineterminator='\n')
         bought_id = get_file_id("bought.csv")
         formatted_buy_price = format(buy_price,".2f")
         product_name = product_name.lower()
         product =[bought_id,product_name,buy_date,formatted_buy_price,expiration_date,amount]
         writer.writerow(product)
         file.close()
       make_inventory(get_date_file(), "add")

# This function checks if the same product with the same expiration date has already been bought 
def check_product_already_bought(product_name, expiration_date):
   with open("bought.csv", "r") as file:
      reader = csv.DictReader(file)
      is_already_bought = False
      for row in reader:
         if row["product_name"] == product_name:
            if row["expiration_date"] == expiration_date:
             is_already_bought = True
      return is_already_bought

   
 
