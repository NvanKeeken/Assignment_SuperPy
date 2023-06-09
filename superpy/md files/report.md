## Report
This is my report on the Winc Back-End Assignment SuperPy. 

Extra functionalities I used:

* Rich Table to show the csv files as tables in the CLI
* Rich console to print the messages in certain colors
* Mathplotlib to make the line charts

Technical elements I like to highlight are:

- use of csv

  I imported csv to read and write to the csv files. I especially used csv.Dictreader(file) to read the rows in csv in a dictionary. This gave the advantage that i could access the values of different columns more easily and I found it more readable then csv.reader().  

- use of add_mutually_exclusive_group() with args.parse 
  
  I imported args_parse to build the CLI programm. To make sure certain arguments can not be used side by side 
  I added mutually_exclusive_group(). This makes sure that arguments like ``--yesterday``, `` --today ``, ``--now`` can't be parsed add the same time.
  
  for example 
      
      python main.py report inventory --today --yesterday 

  Gives error:

       usage: main.py report inventory [-h]
                                (--now [NOW] | --yesterday [YESTERDAY] | --date DATE | --today [TODAY] | --expired [EXPIRED])
      main.py report inventory: error: argument --yesterday: not allowed with argument --today
- use of datetime:
  
  I imported datetime to the programm dynamic in using dates in format of %Y-%m-%d, %y-%m or %Y. This made it possible for me to calculate the profit of a certain month of the year or a whole year instead of only a certain date. with strptime I could make a date object of a date passed down and with strftime I could format it. 
  
  With this function I would for example check the format that a certain date was in and return it if it was if it was in the allowed formats. If that was not the case a ValueError was raised.

       def get_date_Format(date):     
    try:
      if date == datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d"):
            return "%Y-%m-%d"
    except ValueError:
      try:
          if date == datetime.datetime.strptime(date, "%Y-%m").strftime("%Y-%m"):
            return "%Y-%m"
      except ValueError:
           try:
               if date == datetime.datetime.strptime(date, "%Y").strftime("%Y"):
                  return "%Y"
           except ValueError:
                raise ValueError("format must be 'YYYY-MM-DD', 'YYYY-MM' or 'YYYY'")

   That format gets used to filter a csv on products that are equal to that time period. Because the format for the sell_date and buy_date are always %Y-%m-%d, they need to be formatted to the date passed down
   for example in this function that filters the sold.csv for products sold on a certain date:

       def get_sold_products_per_date(date):
        with open("sold.csv", "r") as soldfile:
        reader = csv.DictReader(soldfile)
        sold_products_by_date = []
        date_format= get_date_Format(date)
        for row in reader:
            row_date = dt.datetime.strptime(row["sell_date"], "%Y-%m-%d").strftime(date_format)
            if row_date == date:
                 sold_products_by_date.append(row)
        return sold_products_by_date

- use of calandar 

  I imported calender to transform a date in format of %Y-%m to a written form for example from 2023-05 to May 2023

       def get_month(date):
        date_format = get_date_Format(date)
        if date_format == "%Y-%m":
        month = int(dt.datetime.strptime(date, "%Y-%m").strftime("%m").lstrip("0").replace(" 0", " "))
        year = dt.datetime.strptime(date, "%Y-%m").strftime("%Y")
        return calendar.month_name[month] +" " + year
        else:
          return date


 


