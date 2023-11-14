from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv
from random import randint


service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://wave.webaim.org/")
driver.maximize_window()
web_url = driver.find_element(By.ID, "input_url")
web_url.send_keys("https://google.com")
submit = driver.find_element(By.ID, "button_wave")
submit.click()

with open('top10milliondomains.csv', newline='') as csvfile:
    spamreader = list(csv.reader(csvfile, delimiter=',', quotechar='"'))
    # get 100 websites in csv where page rank between 10 and 6 and 100 of the bottom 20% percentile
    url_list = []
    randomUpper = []
    randomLower = []
    # repeated code but who cares
    while len(url_list) != 100:
        tempLow = randint((len(spamreader)*3)//4,len(spamreader)-1)
        if tempLow not in randomLower:
            randomLower.append(tempLow)
            url_list.append(spamreader[tempLow])

    while len(url_list) != 200:
        tempHigh = randint(1,1804)
        if tempHigh not in randomUpper:
            randomUpper.append(tempHigh)
            url_list.append(spamreader[tempHigh])


for url in url_list:
    try:
        web_url = driver.find_element(By.ID, "input_url")
        web_url.clear()
        web_url.send_keys(url[1])
        submit = driver.find_element(By.ID, "button_wave")
        submit.click()

        details_button = driver.find_element(By.ID, "tab-details")
        details_button.click()
        time.sleep(5)
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
        print(errors)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("It is likely that the website no longer exists or you do not have access to it")
        continue
driver.quit
