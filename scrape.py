# Scrapes item/auction and stores today's standing offers
import urllib.request

def main():
    raw_text = urllib.request.urlopen("http://www.funnyjunk.com/item/auction/")
    f = raw_text.read().decode('utf-8')
    
    # Manual parsing HORROR
    # DO NOT EVER ATTEMPT
    f = f.split("<div id='offer_items'>")[1]
    f = f.split("<script id='tmp-offer-buying-form' type='text/x-jquery-tmpl'>")[0]
    raw_list = f.split("<div class='offerInfo'>")[1:-1]
    for block in raw_list:
        block = block.split('style')[0]
        nu, quantity, points, ppu, oi = block.split("<br />")
        
        name, user = nu.split(" - ")
        name = name.replace("</span><span>", '').replace(" <span class='pinkLight'>", '')
        user = user.partition('">')[2].replace("</a></span> ", '')
        
        def get_int(text, s):
            text = "".join(text.split()) # Remove whitespace
            text = text.replace(',', '')
            s = "".join(s.split())
            r = text.partition(s)[2]
            if '.' in r:
                return float(r)
            else:
                return int(r)
            
        
        quantity = get_int(quantity, "Quantity:")
        points = get_int(points, "Points:")
        ppu = get_int(ppu, "Price per unit::")
        print(ppu)
        
        
        
    
    
main()