# may take a few minutes so please be patient.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time
import json
import csv

def gather_urls(filenames: [str]) -> [str]:
    url_list = []
    for filename in filenames:
        with open(filename, 'r') as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                url_list.append(row)
        csvfile.close()
    return url_list

# I know this function is quite bad but webscraping is a colossal pain
def create_json_data(urls_list_filepaths: [str], json_name: str) -> None:
    # start selenium and get to the page ready for automation
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://wave.webaim.org/")
    driver.maximize_window()
    web_url = driver.find_element(By.ID, "input_url")
    web_url.send_keys("https://google.com")
    submit = driver.find_element(By.ID, "button_wave")
    submit.click()
    # initial value for json
    website_data = {}
    # get the urls from the file paths
    url_list = gather_urls(urls_list_filepaths)
    # run the tool on each url and if we have any errors, retry for a max of 10 times
    for url in url_list:
        for atsplit_tool_textt in range(10):
            # we may find some errors in the tool:
            # (the page may not exist or the tool will see we are automating its use and kick us off)
            try:
                # input url and send
                web_url = driver.find_element(By.ID, "input_url")
                web_url.clear()
                web_url.send_keys(url[1])
                submit = driver.find_element(By.ID, "button_wave")
                submit.click()
                # go to details tab
                details_button = driver.find_element(By.ID, "tab-details")
                details_button.click()
                # let the tool load for a bit
                time.sleep(10)
                # get the list elements (errors, alerts, features, etc.)
                flagged_list = driver.find_elements(By.CLASS_NAME, 'icon_group')
                # we will layout each value as follows:
                # { 
                #   'Errors': 12,
                #   'Contrast_Errors': 2,
                #   ... and so on
                # }
                # In this case 'Errors' we will call a header and the value '12' is a value
                errors = {}
                # for each header in ['errors', 'alerts', ...]
                # remember that html is of form
                # <li class='icon_group'> ... 
                #   <label for='{error_type}'> {number_of_checkpoint_violation} X {checkpoint_violation_name} </label>
                # </li> 
                # to read about the different error types see https://wave.webaim.org/api/docs?format=html
                for list_element in flagged_list[:len(flagged_list)+1]:
                    # get the text for each header and make it one big list (which will be processed)
                    split_tool_text = list_element.text.split()
                    i = 0
                    # initialise as the first character SHOULD always be a number sometimes 
                    # may be index out of range if error in tool (page does not exist)
                    lastNum = split_tool_text[0]
                    # final header for our dictionary
                    # i.e. the key part
                    header = ""
                    # loop through string list
                    for i in range(1, len(split_tool_text)):
                        # try to convert to a number if so break (we have the value now we need to find the key) not 
                        # them check if the header is empty the the header is updated 
                        # (there is no header currently set for the last number, remember that numbers are always followed a header value)
                        # if there is already a value in header then the following word belongs to the same header and are seperated by a space
                        # e.g. 'Contrast Errors' -> ['Contrast','Errors'] -> 'Contrast_Errors'
                        try:
                            int(split_tool_text[i])
                            break
                        except:
                            if len(header) == 0:
                                header = split_tool_text[i]
                            else:
                                header += "_" + split_tool_text[i]
                    # we got to the end of the tool's displayed information for that error type ("Errors" or 'Alerts' or etc...)
                    errors[header] = lastNum
                    header = ""
                    # now we need to go from where we left off and repeat what we did before. update the last number as we go along and
                    # save the header (key), once we encounter another number then we know we are at a different error type so add it to the dictionary
                    for item in split_tool_text[i:]:
                        try:
                            num = int(item)
                            if len(header) != 0:
                                errors[header] = lastNum
                                header = ""
                            lastNum = num
                        except:
                            # ignore X's they are useless
                            if item == "X":
                                continue
                            elif len(header) == 0:
                                header = item
                            else:
                                header += "_"+item
                    errors[header] = lastNum
                # save the final dictionary as
                # {
                #     ['url' : {
                #         'error_type':num_of_error_type,
                #         ...
                #     },
                #     page_rank
                #     ],
                #     ...
                # }
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
                # something went wrong, typically this is an error with the WAVE tool and the website no longer exists or blocks the WAVE tool
                # urls have been sanitised to avoid this happening but may still happen
                # if it does then retry. NOTE When testing there are no urls which fail for all 10 attempts
                print(f"Unexpected {err=}, {type(err)=}")
                print("It is likely that the website no longer exists or you do not have access to it")
                print("Trying again...")
            break
        else:
            # something went seriously wrong (it failed running 10 times)
            print(f"--- {url[1]} does not work at all --- ")

    # write json (avoid recomputing everything)
    with open(json_name, "w") as file:
        json.dump(website_data, file)

    print("Data stored successfully!")
    driver.quit
    return

create_json_data(['sample_data/high_open_page_rank_urls.csv', 'sample_data/low_open_page_rank_urls.csv'], 'sample_data/pagerank_error_data.json')
create_json_data(['sample_data/government_urls.csv', 'sample_data/non_government_urls.csv'], 'sample_data/government_error_data.json')