# Imports
import argparse
from sys import stdout
from advance import advance_time,set_date_today,get_date_file, get_date_yesterday, get_month, get_date_now
from buy import buy_product
from report import  is_inStock, make_inventory
from checks.date import validation_check_date
from expired import get_expired_products
from revenue import get_total_revenue
from profit import calculate_total_profit
from visible_components.tables import make_table_from_bought_csv, make_table_from_sold_csv
from visible_components.chart import make_line_chard
from rich.console import Console
import os.path
# Do not change these lines
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
console = Console()
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest="command")
# parser = argparse.ArgumentParser()
# subparser = parser.add_subparsers(dest='command')

#all the subparsers 
sell = subparser.add_parser('sell')
buy = subparser.add_parser('buy')
report = subparser.add_parser("report")
chart = subparser.add_parser("chart")


# arguments subparser buy
buy.add_argument('--name', "-n", type=str, required=True, help="Supply the bought product name")
buy.add_argument('--price', "-p", type=float, required=True, help="Supply the bought product price")
buy.add_argument('--expiration_date',"-e", required=True, help="Supply the expiration date of the bought product")
buy.add_argument('--amount',"-a", required=True, help="Supply the amount of products bought")


# arguments subparser sell
sell.add_argument("--name","-n",type=str,help="Supply the name of the product sold",required=True )
sell.add_argument("--price", "-p", type=float, help="Supply the price of product sold", required=True)
sell.add_argument("--amount", "-a", type=int, help="Supply the amount of products sold", required=True)
sell.add_argument("--expiration_date","-e",help="Supply the expiration date of the sold product",required=True)

# add argument chart
chart_group = chart.add_mutually_exclusive_group(required=True)
chart_group.add_argument("--last_week",
                   const= 7,
                   nargs="?",
                   help="shows linechart profit/revenue over the last week", 
                   required=False)
chart_group.add_argument("--last_month",
                   const= 28,
                   nargs="?",
                   help="shows linechart profit/revenue over the last month", 
                   required=False)
chart_group.add_argument("--week",
                   type=int,
                   help="Supply amount of weeks you want linechart profit/revenue from ", 
                   required=False)
chart_data_group = chart.add_mutually_exclusive_group(required = True)
chart_data_group.add_argument("--profit",
                               const = "profit",
                               nargs="?",
                               help="shows linechart profit", 
                               required=False)
chart_data_group.add_argument("--revenue",
                               const = "revenue",
                               nargs="?",
                               help="shows linechart revenue", 
                               required=False)
# add subparsers to report 
sub_report = report.add_subparsers(dest = "report_comment")
sold = sub_report.add_parser("sold")
bought = sub_report.add_parser("bought")
inventory = sub_report.add_parser("inventory")
revenue = sub_report.add_parser("revenue")
profit = sub_report.add_parser("profit")


# add arguments to subparser inventory from parser report 
inventory_group = inventory.add_mutually_exclusive_group(required = True) 
inventory_group.add_argument("--now",
                       nargs="?",
                       const= get_date_now(),
                       required=False,
                       help="Shows inventory of actual date")

inventory_group.add_argument("--yesterday",
                       nargs="?",
                       const= get_date_yesterday(),
                       required=False, 
                       help="Shows inventory of yesterday based on the date the precieved as today")

inventory_group.add_argument("--date",
                       required=False,
                       help="Supply date you want the revenue form in format YYYY-mm-dd, YYYY-mm or YYYY")

inventory_group.add_argument("--today",
                       nargs="?",
                       const=get_date_file(),
                       required=False,
                       help="shows inventory of the date that is precieved to be today")

inventory_group.add_argument("--expired",
                       nargs="?",
                       const="0",
                       required=False,
                       help="Supply the amount of days before the products expires,by default it returns the already expired products " )

# adds arguments to subparser revenue from parser report 
revenue_group = revenue.add_mutually_exclusive_group(required=True)
revenue_group.add_argument("--today",
                     nargs="?",
                     const=get_date_file(),
                     required=False, 
                     help="Gives revenue of the date that is precieved to be today")

revenue_group.add_argument("--yesterday",
                     nargs="?",
                     const= get_date_yesterday(),
                     required=False, 
                     help="Gives revenue of yesterday based on date that is precieved to be today")

revenue_group.add_argument("--date", 
                     required=False, 
                     help="Supply date you want the revenue form in format YYYY-mm-dd , YYYY-mm or YYYY")

# adds arguments to subparser profit from parser report
profit_group = profit.add_mutually_exclusive_group(required=True)
profit_group.add_argument("--today",
                    nargs="?",
                    const=get_date_file(),
                    required=False,
                    help="Gives profit of the date that is precieved to be today")

profit_group.add_argument("--yesterday",
                    nargs="?",
                    const= get_date_yesterday(),
                    required=False,
                    help="Gives profit of yesterday based on what is precieved to be today")

profit_group.add_argument("--date",
                    required=False,
                    help="Supply date you want the profit form in format YYYY-mm-dd, YYYY-mm or YYYY")

# add argument advance
parser.add_argument("--advance_date", type=int,help="Supply the number of days you want to advance by")

args = parser.parse_args()

# Checks wich subparser and argument is used and wich functionality needs to be executed 
if args.command == 'buy':
   if validation_check_date("%Y-%m-%d",args.expiration_date):
       buy_product(args.name, args.price, args.expiration_date, args.amount)
       console.print("Ok", style="bold green")
  
if args.command == "sell":
   if validation_check_date("%Y-%m-%d",args.expiration_date):
      is_inStock(args.name,args.price, args.amount, args.expiration_date)
      console.print("Ok", style="bold green")

if args.command == 'chart':
   data_displayed = args.profit if args.profit else args.revenue
   if data_displayed:
       if args.last_week:
          make_line_chard(args.last_week,data_displayed)
       if args.last_month:
          make_line_chard(args.last_month,data_displayed)
       if args.week:
          make_line_chard(args.week * 7,data_displayed)

elif args.command == 'report':
  if args.report_comment == "sold":
    make_table_from_sold_csv()

  if args.report_comment == "bought":
    make_table_from_bought_csv()

  if args.report_comment == "inventory":
     if args.yesterday:
        make_inventory(args.yesterday, "show")
     if args.now:
        make_inventory(args.now, "show")
     if args.date:
        make_inventory(args.date, "show")
     if args.today:
        make_inventory(args.today,"show")
     if args.expired:
        get_expired_products(args.expired)

  if args.report_comment == "revenue":
     if args.today:
         console.print(f"Today's revenue: {get_total_revenue(args.today)} euro", style="bold cyan")
     elif args.yesterday:
         console.print(f"Yesterday's revenue: {get_total_revenue(args.yesterday)} euro", style="bold cyan")
     elif args.date:
        console.print(f"Revenue in {get_month(args.date)}: {get_total_revenue(args.date)} euro", style="bold cyan")

  if args.report_comment == "profit":
     no_profit_message = "No profit was made, only loss"
     if args.today:
        if int(calculate_total_profit(args.today)) >= 0:
            console.print(f"Today's profit:{calculate_total_profit(args.today)} euro", style="bold green")
        else:
           console.print(no_profit_message, style="bold red")

     elif args.yesterday:
         if int(calculate_total_profit(args.yesterday)) >= 0: 
            console.print(f"Yesterday's profit: {calculate_total_profit(args.yesterday)} euro", style="bold green")
         else:
             console.print(no_profit_message, style="bold red")

     elif args.date:
         if int(calculate_total_profit(args.date)) >= 0:
             console.print(f"Profit in {get_month(args.date)}: {calculate_total_profit(args.date)} euro", style="bold green")
         else:
            console.print(no_profit_message, style="bold red")

if args.advance_date:
    advance_time(args.advance_date)

def main():
   import csv
   if os.path.isfile("Invent.csv") == False:
      with open("Invent.csv", "w") as inventoryfile:
         writer = csv.writer(inventoryfile)
         writer.writerow(["Product Name", "Count", "Buy Price", "Expiration Date"])

   if os.path.isfile("sold.csv") == False:
      with open("sold.csv", "w") as soldfile:
         writer = csv.writer(soldfile)
         writer.writerow(["id","bought_id","product_name","amount","sell_date","sell_price"])

   if os.path.isfile("bought.csv") == False:
      with open("bought.csv", "w") as boughtfile:
         writer = csv.writer(boughtfile)
         writer.writerow(["id","product_name","buy_date","buy_price","expiration_date","amount"])
   if os.path.isfile("currentDate.txt") == False:
      set_date_today()

if __name__ == "__main__":
    main()
