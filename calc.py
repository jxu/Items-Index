# Currently finds lowest price of item (by name) at date
# Use picture ID for items with same name later
import csv
from datetime import date, timedelta, datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


ITEM_NAME = "Demonic Ore"

def lowest(item_name, start_date, end_date):
    assert(end_date > start_date)
    
    
    
    with open("data/data.csv", 'r') as f:
        reader = csv.reader(f)
        data_rows = []
        
        for row in reader:
            row_date = datetime.strptime(row[-1], "%m/%d/%Y").date()
      
            if start_date <= row_date <= end_date and row[0] == ITEM_NAME:
                data_rows.append([row_date, float(row[4])] ) 
                
        
    lowest_rows = []
    current_date = start_date
    
    while current_date != end_date:
        x = []
        for rows in data_rows:
            if rows[0] == current_date:
                x.append(rows)
        
        lowest_rows.append(sorted(x, key=lambda x: x[1])[0])
        current_date += timedelta(days = 1)
        

    return lowest_rows

def plot(pairs):
    dates = [x[0] for x in pairs]
    ppu = [x[1] for x in pairs]
    

    fig, ax = plt.subplots(1)
    ax.plot(dates, ppu, '-')
    plt.title("Lowest Prices for " + ITEM_NAME)
    plt.grid(True)
    plt.axis([dates[0], dates[-1], 0, 1.1*max(ppu)])
    fig.autofmt_xdate()

    plt.show()
    

                                    

pairs = lowest(ITEM_NAME, date(2015, 1, 1), date.today())
plot(pairs)            

