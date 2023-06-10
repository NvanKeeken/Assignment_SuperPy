## User_Guide Superpy SuperPy

the core functionality of this commant line tool is to keep track of the inventory and produce report on different kind of data.

### With this CLI application you can:
- buy a product
- sell a product 
- get a report of the inventory 
- get a report of the sold products
- get a report of the bought products
- get a report of all the expired products
- calculate the profit 
- calculate the revenue
- show profit/revenue in linechard 
- advance date that is precieved to be today 
- set date that is precieved to be today

### How to buy a product?
To buy a product use:
    
     python main.py buy

The options of arguments you are required to use are:
- --name or -n              product name
- --price or -p             price of one bought product 
- --expiration_date or -e   expiration_date of bought product in format YYYY-MM-DD
- --amount or -a            amount of products bought with this expiration_date

The argument that is optional to use:
- --buy_date or -b          buy date of the bought product in format YYYY-MM-DD

If buy_date is not defined it will automatically set the buy_date to the date that is precieved to be today

Example:

    python main.py buy --name milk --price 0.99 --expiration_date 2023-06-14 --amount 10 --buy_date 2023-06-15

    python main.py buy -n milk -p 0.99 -e 2023-06-14 -a 10 -b 20230-06-15

    python main.py buy --name milk --price 0.99 --expiration_date 2023-06-14 --amount 10

    python main.py buy -n milk -p 0.99 -e 2023-06-14 -a 10

### How to Sell a product?
To sell a product use:

    python main.py sell

The options of arguments you are required to use are:
* --name or -n              product name
* --price or -p             price of one sold product 
* --amount or -a            amount of products bought with this expiration_date

The argument that is optional to use:
* --sell_date or -s         sell date of sold product in fromat YYYY-MM-DD

If sell_date is not defined it will set the sell_date to the date that is precieved to be today

When there are more then one of the sold product in the inventory, it will automatically sell the one that is closest to expiring. If that product is already expired it will sell the next closest to expiring, until the expired product is left. Then it will give an error message to make you aware. 

Example:

    python main.py sell --name milk --price 1.50 --amount 2 --sell_date 2023-06-14

    python main.py sell -n milk -p 1.50 -a 2 -s 20230-06-14

    python main.py sell --name milk --price 1.50 --amount 2 

    python main.py sell -n milk -p 1.50 -a 2 

### How to get a report of the inventory?
To show inventory:

    python main.py report inventory 

You are required to use only one of these options:
* --now  shows inventory actual date
* --yesterday shows inventory of yesterday based on the date that is precieved as today by the programm
* --today shows inventory of date that is precieved as today by the programm
* --date shows inventory of a spefic date or period of time, date passed need to be in format %Y-%m-%d, %Y-%d or %Y
* --expired shows expired products in inventory of today or products that are going to expire in a certain amount of days 

Examples:

    python main.py report inventory --now 

    python main.py report inventory --yesterday

    python main.py report inventory --today

    python main.py report inventory --date 2023-05-22
    python main.py report inventory --date 2023-05
    python main.py report inventory --date 2023

    python main.py report inventory --expired

### How to get a report on the expired products?
to show expired products use:

    python main.py report inventory --expired

to show the products that are going to expire in a certain amount of days use:

    python main.py report inventory --expired [amount of days]

Example:

     python main.py report inventory --expired 7
### How to get a report of the sold products?
To show sold products:

      python main.py report sold


### How to get a report of the bought products?
To show bought products:

    python main.py report bought

### How to get a report of revenue?
To calculate revenue:

    python main.py report revenue  

You are required to use only one of these options:
* --yesterday       calculates revenue of yesterday based on the date that is precieved as today by the programm
* --today           calculates revenue of date that is precieved as today by the programm
* --date            calculates revenue of a spefic date or period of time, date passed need to be in format %Y-%m-%d, %Y-%d or %Y

Examples:

    python main.py report revenue --yesterday

    python main.py report revenue --today

    python main.py report revenue --date 2023-05-22
    python main.py report revenue --date 2023-05
    python main.py report revenue --date 2023

### How to get a report of profit?
To calculate profit:

    python main.py report profit  

You are required to use only one of these options:
* --yesterday       calculates profit of yesterday based on the date that is precieved as today by the programm
* --today           calculates profit of date that is precieved as today by the programm
* --date            calculates profit of a spefic date or period of time, date passed need to be in format %Y-%m-%d, %Y-%d or %Y

Examples:

    python main.py report profit --yesterday

    python main.py report profit --today

    python main.py report profit --date 2023-05-22
    python main.py report profit --date 2023-05
    python main.py report profit --date 2023

### How to show a line chart?

to show a line chart:
    python main.py chart 

You need to choose at least one of these options:

* --revenue shows a line chart of revenue over a specified period of time
* --profit shows a line chart of the profit over a specified period of time 

To specify the period of time you need to choose one of these options:

* --last_week shows line chart over a period of a week 
* --last_month shows line chart over a period of a month
* --week you need to supply the amount of weeks you want your period of time to be

Examples:
    
    python main.py chart --revenue --last_week
    python main.py --revenue --last_month
    python main.py --revenue --week 2

    python main.py chart --profit --last_week
    python main.py chart --profit --last_month
    python main.py chart --profit --week 3
### How to advance the date that is precieved as today?

to advance the date:

    python main.py --advance_date  [number of days you want to andvance by]

Example:

     python main.py --advance_date 2

### How to set the date that is precieved as today?

to set the date that is precieved as today at a specific date:
    
    python main.py --set_date [YYYY-MM-DD]

Example:

    python main.py --set_date 2023-06-10