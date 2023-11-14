from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://wave.webaim.org/")
driver.maximize_window()
web_url = driver.find_element(By.ID, "input_url")
web_url.send_keys("https://github.com")
submit = driver.find_element(By.ID, "button_wave")
submit.click()

for i in range(100):
    details_button = driver.find_element(By.ID, "tab-details")
    details_button.click()
    time.sleep(5)
    flagged_list = driver.find_elements(By.CLASS_NAME, 'icon_group')
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

    break
driver.quit
    # a = driver.find_element(By.CLASS_NAME, "login-link")
    # driver.implicitly_wait(10)
    # a.click()
    # driver.implicitly_wait(10)
    # username = driver.find_element(By.ID, "username")
    # username.send_keys("albertovitri@outlook.com")
    # password = driver.find_element(By.ID, "password")
    # password.send_keys("bkzBhnvSW0")
    # sign_in = driver.find_element(By.ID, "sign_in_btn")
    # sign_in.click()
    # high_impact = driver.find_element(By.XPATH, '//*[@id="filter-stats-types"]/ul/li[1]/span[3]')
    # print(high_impact.text)
    # driver.quit()