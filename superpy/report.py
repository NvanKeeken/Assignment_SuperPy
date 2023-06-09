import csv
from checks.expired import expiration_check, expiring_in_future
from advance import get_date_Format, get_date_file
from visible_components.tables import make_table_from_inventory
from sell import add_sold_product
from datetime import datetime
from rich.console import Console

console= Console()
# This file contains all the functions related to the report inventory CLI argument

# This function empties the inventory csv to just the headers 
def reset_inventory():
    with open("Invent.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Product Name", "Count", "Buy Price", "Expiration Date"])

# adds a item to a csv file
def add_to_csv(path, item):
       with open(path, "a", newline="") as file:
           writer = csv.writer(file)
           writer.writerow(item)

# Makes inventory table visible in the CLI
def show_Inventory(inventory):
     make_table_from_inventory(inventory)

""" This function checks when a product is sold if that specific product with the expiration date 
  is in stock. """      
def is_inStock(product_name,price, amount,sell_date=get_date_file()):
    with open("Invent.csv", "r") as file:
        reader = csv.DictReader(file)
        is_in_stock = False
        expiration_date = get_sold_expiration_date(product_name, sell_date, amount)
        from checks.expired import expiration_check
        for row in reader:
            if row["Product Name"] == product_name and row["Expiration Date"] == expiration_date:
                # checks if product is expired, if so it can not be sold
                if expiration_check(row,sell_date) != True:
                   # if sold amount is equal to the amount in stock, it deletes product  out of inventory 
                   if int(row["Count"]) == int(amount):
                       is_in_stock = True
                       delete_product(row)

                    # if stock amount is bigger than 0 and bigger than amount it updates stock count  
                   elif int(row["Count"]) > 0 and int(row["Count"]) >= int(amount):
                       update_count_inventory(product_name,"sold",expiration_date, amount)
                       is_in_stock = True
                else:
                    is_in_stock = False

        if is_in_stock:
            add_sold_product(product_name, price, amount, expiration_date, sell_date)
        else:
            # if sold product is in stock but expired it gives an error
            if expiration_check(row, sell_date):
               console.print("Error: Product(s) are expired", style="bold magenta")
            else: 
               console.print("Error: product is out of stock", style="red bold")

""" this function filters the inventory for expired products if default of 0 days is passed
# else for products that will expire in the amount of days passed 
# if days is bigger then 0. These products will be shown in in the CLI """
def get_expired_products(days):
    expired_products = []
    with open("Invent.csv", "r") as inventoryfile:
        reader = csv.DictReader(inventoryfile)
        for row in reader:
          if days == "0" and expiration_check(row):
            expired_products.append(row)
          elif days > "0":
            if expiring_in_future(row,days):
              expired_products.append(row)
    show_Inventory(expired_products)

""" This function filters the inventory to products of the same kind as the sold product, so by product name.
These products have are of the same kind but have a different expiration date. It return a list of 
the filtered inventory"""

def bought_products_of_kind(product_name):
    with open("Invent.csv", "r") as file:
        reader = csv.DictReader(file)
        products_of_kind=[]
        for row in reader:
            if row["Product Name"] == product_name:
              products_of_kind.append(row)
        return products_of_kind
    

"""This function calculates the expiration date of the sold product.It is possible that a supermarket has multiple 
batches of the same kind of product but with a different expiration date. If that is the case the product will be 
sold from the batch that is closest to expiring, unless the batch is already expired or the amount of products sold 
is bigger than the amount of products of that date in the inventory. In that case it will sell the of the batch next closest to expiring   """       

def get_sold_expiration_date(product_name,sell_date, amount):
    products = bought_products_of_kind(product_name)
    first_expired = ""
    # if there is only one badge or product of this kind it will return that expiration date
    if len(products) == 1:
            return products[0]["Expiration Date"]
    else:
         for product in products:
           product_expiration_date = datetime.strptime(product["Expiration Date"], "%Y-%m-%d")
           # checks if product is already expired 
           if expiration_check(product, sell_date) == False:
             # checks if the amount of products is not bigger than the stock of the product with that expiration date
             if int(product["Count"]) >= amount:
               if first_expired == "":
                   first_expired = product["Expiration Date"]  
               elif product_expiration_date < datetime.strptime(first_expired, "%Y-%m-%d"): # updates the product closest to expiring
                   first_expired = product["Expiration Date"]
             else:
                 continue
           else:
               continue   
    return first_expired

# This function deletes product out of inventory, by emtying the inventory and adding updated list
def delete_product(deleted_product): 
    newLines = []
    with open("Invent.csv", "r+") as inventory:
        lines = csv.DictReader(inventory)
        for line in lines:
            if line != deleted_product: 
                newLines.append(line)
        reset_inventory()
        for line in newLines:
             product = [line["Product Name"], line["Count"], line["Buy Price"], line["Expiration Date"]]
             add_to_csv("Invent.csv", product)

# this function updates the count in inventory if a product is bought or sold
def update_count_inventory(product_name, status, expiration_date, amount = 1): 
    newLines = []
    with open("Invent.csv", "r+") as inv:
        lines = csv.DictReader(inv)
        for line in lines:
            # when a product is sold count gets subtracted by sold amount else it gets added by bought amount
            count = int(line["Count"]) - int(amount) if status == "sold" else int(line["Count"]) + int(amount)
            if line["Product Name"] == product_name and line["Expiration Date"]==expiration_date:
                newLines.append(
                    {
                        "Product Name": line["Product Name"],
                        "Count": count,
                        "Buy Price": line["Buy Price"],
                        "Expiration Date": line["Expiration Date"]
                    }
                )
            else:
                newLines.append(line)

        reset_inventory()
        for line in newLines:
             product = [line["Product Name"],
                        line["Count"],
                        line["Buy Price"],
                        line["Expiration Date"]]
             add_to_csv("Invent.csv",product)

# This function gets all the sold or bought products before and on a certain date 
def get_products_before(date, csv_path, product_date ):
     products = []
     format = get_date_Format(date)
     with open(csv_path, "r") as file:
       reader = csv.DictReader(file)
       for row in reader:
         inventorydate = datetime.strptime(date, format)
         # formats the sell date or buy date to the same format as the date passed down
         formatted_row_date = datetime.strptime(row[product_date], "%Y-%m-%d").strftime(format)
         row_date = datetime.strptime(formatted_row_date, format)
         if row_date <= inventorydate:
            products.append(row)
       return products

""" this function makes the inventory by comparing the bought products and sold products in a certain time frame. 
if a bought product is also in the sold products list, the bought amount is substracted by the sold amount. 
If the diffirnece is not zero or if a bought product has not been sold it will be added to the inventory """

def make_inventory(date, action):
    bought_products = get_products_before(date, "bought.csv", "buy_date")
    new_inventory =[]
    for bought_product in bought_products:
             sold_products= find_sold_product(bought_product["id"],date)

             # Checks if bought product has been sold
             if sold_products != []:
                #calculates total of items sold from that product
                sold_amount = 0
                for product in sold_products:
                    sold_amount += int(product["amount"])
                amount_difference = int(bought_product["amount"]) - sold_amount
                # checks if product did not already go out of stock 
                if amount_difference != 0: 
                    new_inventory.append(
                    {
                        "Product Name": bought_product["product_name"],
                        "Count": amount_difference,
                        "Buy Price": bought_product["buy_price"],
                        "Expiration Date": bought_product["expiration_date"]
                    })     
             # if bought product has not been sold it will be added to inventory as it is 
             else:
                      new_inventory.append({
                        "Product Name": bought_product["product_name"],
                        "Count": bought_product["amount"],
                        "Buy Price": bought_product["buy_price"],
                        "Expiration Date": bought_product["expiration_date"]
                    })
    # if inventory needs to be updated action is "add"               
    if action == "add": 
       reset_inventory()
       for line in new_inventory:
           product = [
                line["Product Name"],
                line["Count"],
                line["Buy Price"],
                line["Expiration Date"] ]  
           add_to_csv("Invent.csv",product)

    # if inventory needs to be shown action is "show"
    elif action == "show":
        show_Inventory(new_inventory)

def find_bought_product(id,path,characteristic):
    with open(path, "r") as boughtproduct:
        reader= csv.DictReader(boughtproduct)
        for row in reader:
            if id == row["bought_id"]:
                   return row[characteristic]

# this function searches if a product in bought.csv has already been sold in a the same time frame 
#  it returns these sells             
def find_sold_product(id, date):
        sold_products_before = get_products_before(date, "sold.csv", "sell_date")
        sold_products =[]
        for product in sold_products_before:
            if id == product["bought_id"]:
                sold_products.append(product) 
        return sold_products      





           

