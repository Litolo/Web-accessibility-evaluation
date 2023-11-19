from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time
import json
import csv

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://wave.webaim.org/")
driver.maximize_window()
web_url = driver.find_element(By.ID, "input_url")
web_url.send_keys("https://google.com")
submit = driver.find_element(By.ID, "button_wave")
submit.click()

def gather_urls(filenames: [str]) -> [str]:
    url_list = []
    for filename in filenames:
        with open(filename, 'r') as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                url_list.append(row)
        csvfile.close()
    return url_list

website_data = {}
sample_data = ['sample_urls\high_open_page_rank_urls.csv', 'sample_urls\low_open_page_rank_urls.csv']
url_list = gather_urls(sample_data)
for url in url_list:
    for attempt in range(10):
        try:
            web_url = driver.find_element(By.ID, "input_url")
            web_url.clear()
            web_url.send_keys(url[1])
            submit = driver.find_element(By.ID, "button_wave")
            submit.click()

            details_button = driver.find_element(By.ID, "tab-details")
            details_button.click()
            time.sleep(10)
            flagged_list = driver.find_elements(By.CLASS_NAME, 'icon_group')

            # repeating code here
            errors = {}
            for list_element in flagged_list[:len(flagged_list)-1]:
                temp = list_element.text.split()
                i = 0
                lastNum = temp[0]
                header = ""
                for i in range(1, len(temp)):
                    try:
                        int(temp[i])
                        break
                    except:
                        if len(header) == 0:
                            header = temp[i]
                        else:
                            header += "_" + temp[i]
                errors[header] = lastNum
                header = ""
                for item in temp[i:]:
                    try:
                        num = int(item)
                        if len(header) != 0:
                            errors[header] = lastNum
                            header = ""
                        lastNum = num
                    except:
                        if item == "X":
                            continue
                        elif len(header) == 0:
                            header = item
                        else:
                            header += "_"+item
                errors[header] = lastNum
            website_data[url[1]] = [errors, url[2]]
        except NoSuchElementException:
            # we've been blocked by WAVE so reopen the driver and try the rest of the urls
            driver.quit
            service = Service()
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(service=service, options=options)
            driver.get("https://wave.webaim.org/")
            driver.maximize_window()
            web_url = driver.find_element(By.ID, "input_url")
            web_url.send_keys("https://google.com")
            submit = driver.find_element(By.ID, "button_wave")
            submit.click()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            print("It is likely that the website no longer exists or you do not have access to it")
            print("Trying again...")
        break
    else:
        print(f"--- {url[1]} does not work at all --- ")

with open("website_error_data.json", "w") as file:
    json.dump(website_data, file)

print("Data stored successfully!")
driver.quit
