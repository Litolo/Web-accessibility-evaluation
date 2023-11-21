# please keep in mind that this program may take a while to run due to the nature of having to check
# the validity of websites. It takes a while to ping so many requests and have valid results

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
    counter = 0
    government_domains = ['.gov', '.gv', '.gob','.gc','.gouv','.go.','.govt', '.admin.ch','.government','.gub','.mil']
    # repeated code consider making a function
    with open('sample_urls/government_urls.csv', 'w', newline='') as csvwrite:
        writer = csv.writer(csvwrite)
        # see full list at https://en.wikipedia.org/wiki/.gov
        # gets 100 random valid governement domains and saves to csv
        checked =[]
        while counter < 100:
            # while it is impossible that the same url can be added twice it is extremely unlikely but will account for it anyway
            index = randint(0,1_000_000)
            if (index in checked):
                # stop early for efficiency
                continue
            else:
                checked.append(index)
            if any(x in spamreader[index][1] for x in government_domains) and get_url_status(spamreader[index][1]):
                writer.writerow(spamreader[index])
                counter +=1
                checked.append(index)
    csvwrite.close()
    # gets 100 random valid non governement domains
    counter = 0
    with open('sample_urls/non_government_urls.csv', 'w', newline='') as csvwrite:
        writer = csv.writer(csvwrite)
        checked = []
        while counter < 100:
            # while it is impossible that the same url can be added twice it is extremely unlikely but will account for it anyway
            index = randint(0,1_000_000)
            if (index in checked):
                # stop early for efficiency
                continue
            else:
                checked.append(index)
            # we have to first check if it is a governement domain (remember we cannot do 'not in') if so then skip and generate new index
            if any(x in spamreader[index][1] for x in government_domains):
                continue
            # only executes if not government domain
            if get_url_status(spamreader[index][1]):
                writer.writerow(spamreader[index])
                counter +=1
                checked.append(index)
    csvwrite.close()
    # gets 100 random valid low page rank urls and saves to csv
    counter = 0
    with open('sample_urls/low_open_page_rank_urls.csv', 'w', newline='') as csvwrite:
        writer = csv.writer(csvwrite)
        checked = []
        while counter < 100:
            # while it is impossible that the same url can be added twice it is extremely unlikely but will account for it anyway
            index = randint((len(spamreader)*3)//4,len(spamreader)-1)
            if (index in checked):
                # stop early for efficiency
                continue
            else:
                checked.append(index)
            if get_url_status(spamreader[index][1]):
                checked.append(index)
                writer.writerow(spamreader[index])
                counter += 1
    csvwrite.close()
    # gets 100 random valid high page rank urls and saves to csv
    counter = 0
    with open('sample_urls/high_open_page_rank_urls.csv', 'w', newline='') as csvwrite:
        writer = csv.writer(csvwrite)
        checked = []
        while counter < 100:
            # while it is impossible that the same url can be added twice it is extremely unlikely but will account for it anyway
            index = randint(1,1804)
            if (index in checked):
                # stop early for efficiency
                continue
            else:
                checked.append(index)
            if get_url_status(spamreader[index][1]):
                checked.append(index)
                writer.writerow(spamreader[index])
                counter += 1
    csvwrite.close()
csvfile.close()