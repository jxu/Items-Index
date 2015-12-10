# Scrapes Auction House and stores today's standing offers
# Current time resolution: 1 day (without automated script)

# Current data_list format:
# Item name, user, quantity, offer price, price/unit, offer date, image ID, date accessed
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime, timedelta, timezone
import sqlite3
import calendar

def process_int(s):
    return int(s.replace(',', ''))

def process_float(s):
    return float(s.replace(',', ''))

def process_datetime(text):
    # Only return dates
    if '/' in text:
        return datetime.strptime(text, "%m/%d/%Y").date()
    else:
        now = datetime.utcnow()
        quantity, time_unit = re.search("(\d*) ([a-z]*) ago", text).group(1, 2)
        quantity = int(quantity)
        if "second" in time_unit:
            tdelta = timedelta(seconds=quantity)
        elif "minute" in time_unit:
            tdelta = timedelta(minutes=quantity)
        elif "hour" in time_unit:
            tdelta = timedelta(hours=quantity)

        return (now-tdelta).date()


def scrape():
    data_list = []
    print("Starting...")
    for i in range(1, 30):
        response = requests.get("http://www.funnyjunk.com/item/auction/date/desc/120/%s" % i)
        html = response.content
        soup = BeautifulSoup(html)

        # Manual parsing horror is gone!
        if soup.find("li", attrs={"class": "offerNotFound"}):
            print("Done scraping!")
            break

        table = soup.find("ul", attrs={"class": "offerList"})
        for entry in table.findAll("li"):  # div offerInfo and img src
            #print(entry.prettify())
            item_name = entry.find("span", attrs={"class": "pinkLight"}).text
            if not item_name:
                print("Cancelled")
                continue

            user = entry.find("a").text
            entry_text = str(entry)
            #print(entry_text)
            quantity = process_int(re.search("Quantity: (.*)<br", entry_text).group(1))
            price = process_int(re.search("Points: (.*)<br", entry_text).group(1))
            ppu = process_float(re.search("Price per unit:: (.*)<br", entry_text).group(1))

            offer_datetime_text = re.search("Offered date: (.*)</div>", entry_text).group(1)
            offer_date = process_datetime(offer_datetime_text)

            img_src = entry.find("img")["src"]
            try:
                img_code = re.search("(.{8})\.(gif|png|jpg)", img_src).group(1)
            except:
                print("Image code error:", img_src)
                break

            # For datetime
            now_ts = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
            # For date
            offer_date_ts = calendar.timegm(offer_date.timetuple())

            print("...", item_name, user, quantity, price, ppu, img_code, offer_date_ts, now_ts)
            data_list.append((item_name, user, quantity, price, ppu, img_code, offer_date_ts, now_ts))

        print("Done page %s\t" % i)

    return data_list


def file_write_csv(data_list):
    # Deprecated
    import os, csv
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


def write_sqlite(data):
    conn = sqlite3.connect("data/ah.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS listing (item_name text, user text, quantity integer, price integer,
                 ppu real, img_code text, offer_date integer, scrape_datetime integer)""")

    c.executemany("INSERT INTO listing VALUES (?,?,?,?,?,?,?,?)", data)

    conn.commit()
    conn.close()


def main():
    data_list = scrape()
    write_sqlite(data_list)


if __name__ == "__main__":
    main()