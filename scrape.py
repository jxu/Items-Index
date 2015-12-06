# Scrapes Auction House and stores today's standing offers
# Current time resolution: 1 day (without automated script)

# Current data_list format:
# Item name, user, quantity, offer price, price/unit, offer date, image ID, date accessed
from bs4 import BeautifulSoup
import requests

FILE_PATH = "data/new.csv"

def get_num(text, s):
    text = "".join(text.split()) # Remove whitespace
    text = text.replace(',', '')
    s = "".join(s.split())
    r = text.partition(s)[2]
    if '.' in r:
        return float(r)
    else:
        return int(r)


def scrape():
    data_list = []
    print("Starting...")
    for i in range(1, 2):
        response = requests.get("http://www.funnyjunk.com/item/auction/date/desc/120/%s" % i)
        html = response.content

        # Manual parsing horror is gone!
        soup = BeautifulSoup(html)
        table = soup.find("ul", attrs={"class": "offerList"})
        for entry in table.findAll("div", attrs={"class": "offerInfo"}):
            print(entry.prettify())
            item_name = entry.find("span", attrs={"class": "pinkLight"}).text
            print(item_name)
            user = entry.find("a").text
            print(user)
            # regex the br/


            print()


            return

        if "No offer found." in f:
            print("Done scraping!")
            break
        else:
            print("Page %s\t" % i, end='')


    return data_list

def file_write(data_list):
    file_write = True

    if os.path.isfile(FILE_PATH):
        with open(FILE_PATH, 'r', newline='') as f:
            r = csv.reader(f) # Works in 'r' mode
            for row in r:
                if row[-1] == today:
                    print("Today has already been logged!")
                    file_write = False
                    break


    if file_write:
        with open(FILE_PATH, 'a', newline='') as f:
            print("Appending data...")
            wr = csv.writer(f)
            wr.writerows(data_list)


        print("Done appending!")




def main():
    scrape()



main()