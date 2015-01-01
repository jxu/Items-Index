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
    raw_text = urllib.request.urlopen("http://www.funnyjunk.com/item/auction/")
    f = raw_text.read().decode('utf-8')
    
    # Laxy mix of parsing
    f = f.split("<div id='offer_items'>")[1]
    f = f.split('<div class="comPaginatorPages">')[:-1]
    f = "".join(f)
    
    soup = BeautifulSoup(f)

    full_text = soup.get_text()
    full_list = full_text.split('Buy')[:-1]
    
    data_list = []
    
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
        
        data_list.append([name, user, quantity, points, ppu, od, today])
        
    links = []
    for link in soup.find_all('img'):
        links.append(link.get('src')[36:40])
    for i in range(len(links)):
        data_list[i].append(links[i])
        
    print(data_list)
        
        
        
    
    
main()