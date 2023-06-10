
from matplotlib import pyplot as plt
from revenue import get_total_revenue
from datetime import timedelta
import datetime
from advance import get_date_file
from profit import calculate_total_profit

def make_line_chard(days, data):
    dates_in_period=[]
    revenue_per_day = {}
    profit_per_day ={}
    today = datetime.datetime.strptime(get_date_file(), "%Y-%m-%d").date()
    for i in range(0,days):
       day = today - timedelta(days=i)
       dates_in_period.append(day.strftime("%Y-%m-%d"))
    for day in dates_in_period:
        day_revenue = get_total_revenue(day)
        day_profit = calculate_total_profit(day)
        revenue_per_day[day] = day_revenue
        profit_per_day[day] = day_profit
    if data == "revenue":
        plt.plot(list(revenue_per_day.keys()), list(revenue_per_day.values()))
        plt.title("Superpy Revenue")
    elif data == "profit":
        plt.plot(list(profit_per_day.keys()), list(profit_per_day.values()), color="#FFD700")
        plt.title("Superpy Profit")
   
    plt.xlabel("Day")
    plt.xticks(rotation = 45)
    plt.ylabel("euros (€)")
    plt.show()


