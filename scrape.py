# Scrapes item/auction and stores today's standing offers
# Current time resolution: 1 day (without automated script)
import urllib.request
from bs4 import BeautifulSoup

def get_num(text, s):
    text = "".join(text.split()) # Remove whitespace
    text = text.replace(',', '')
    s = "".join(s.split())
    r = text.partition(s)[2]
    if '.' in r:
        return float(r)
    else:
        return int(r)


def main():
    data_list = []
    print("Starting...")
    for i in range(1, 30):
        raw_text = urllib.request.urlopen("http://www.funnyjunk.com/item/auction/date/desc/120/%s" % i)
        f = raw_text.read().decode('utf-8')
        
        if "No offer found." in f:
            print("Done scraping!")
            break
        else:
            print("Page %s\t" % i, end='')
        
        # Laxy mix of parsing
        f = f.split("<div id='offer_items'>")[1]
        f = f.split('<div class="comPaginatorPages">')[:-1]
        f = "".join(f)
        
        soup = BeautifulSoup(f)
    
        full_text = soup.get_text()
        full_list = full_text.split('Buy')[:-1]
        
        j = 0
        all_img = soup.find_all('img')
        
        for block in full_list:
            block = block.rstrip()
            
            nu, quantity, points, ppu, od = block.split('\n')
            name, user = nu.split(' - ')
            name = name.strip()
            user = user.strip()
            
            quantity = get_num(quantity, "Quantity:")
            points = get_num(points, "Points:")
            ppu = get_num(ppu, "Price per unit::")
            
            od = od.strip().partition("Offered date: ")[2]
            from time import gmtime, strftime
            today = strftime("%m/%d/%Y", gmtime())
            if "ago" in od:
                od = today
            
            img_id = all_img[j].get('src')[36:40]
            # Current data_list format
            # Item name, user, quantity, offer price, price/unit, offer date, image ID, date accessed
            data_list.append([name, user, quantity, points, ppu, od, img_id, today])
            j+=1
            
            
        print('...')
            
    #print(data_list)
    
    print("Appending data...")
    
    import csv
    f = open("data/data.csv", 'a', newline='')
    wr = csv.writer(f)
    wr.writerows(data_list)
        
        
    print("Done appending!")
    
    
        
main()