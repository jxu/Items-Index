# Currently finds lowest price of item (by name) at date
# Use picture ID for items with same name later
import csv

ITEM_NAME = "Bucket Of Coal"
DATE = "01/01/2015"

with open("data/data.csv", 'r') as f:
    reader = csv.reader(f)
    lowest_row = []
    for row in reader:
        if row[-1] == DATE and row[0] == ITEM_NAME:
            if lowest_row == []:
                lowest_row = row
            elif float(row[4]) < float(lowest_row[4]):
                lowest_row = row
                
    print(lowest_row)
                    
            
    
            

