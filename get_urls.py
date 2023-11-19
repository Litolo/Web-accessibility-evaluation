import requests
import csv
from random import randint

def get_url_status(url):  # checks status for each url in list urls
    url = "https://"+url
    try:
        r = requests.get(url, timeout=10)
        return True if r.status_code < 400 else False
    except Exception:
        return False


with open('top10milliondomains.csv', newline='') as csvfile:
    spamreader = list(csv.reader(csvfile, delimiter=',', quotechar='"'))
    # get 100 websites in csv where page rank between 10 and 6 and 100 of the bottom 20% percentile
    randomUpper = []
    randomLower = []
    counter = 0
    # repeated code consider making a function
    with open('sample_urls/low_open_page_rank_urls.csv', 'w', newline='') as csvwrite:
        writer = csv.writer(csvwrite)
        while counter != 100:
            tempLow = randint((len(spamreader)*3)//4,len(spamreader)-1)
            if tempLow not in randomLower and get_url_status(spamreader[tempLow][1]):
                randomLower.append(tempLow)
                writer.writerow(spamreader[tempLow])
                counter += 1
    csvwrite.close()
    counter = 0
    with open('sample_urls/high_open_page_rank_urls.csv', 'w', newline='') as csvwrite:
        writer = csv.writer(csvwrite)
        while counter != 100:
            tempHigh = randint(1,1804)
            if tempHigh not in randomUpper and get_url_status(spamreader[tempHigh][1]):
                randomUpper.append(tempHigh)
                writer.writerow(spamreader[tempHigh])
                counter += 1
    csvwrite.close()
csvfile.close()