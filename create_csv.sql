.mode csv
.headers on
.output data/test.csv
-- Eventually will be one csv file per item
SELECT item_name,min(ppu),scrape_datetime FROM listing GROUP BY item_name,scrape_datetime;
.output stdout