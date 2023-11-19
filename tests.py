import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# do a independent t test on errors.

# First we need to compute the A3 aggregation score for each website. B_p = total points of failure

f = open('website_error_data.json')
data = json.load(f)

urls = []
page_ranks = []

def get_total_potential_failures(data_url: [str, str]) -> int:
    B_p = 0
    total_headers = ['Errors', 'Contrast_Errors','Alerts','Features']
    for header in total_headers:
        for failure_point in data_url:
            if failure_point == header:
                B_p += int(data_url[header]) if header != 'Alerts' else int(data_url[header])//2
    return B_p

def get_checkpoints() -> (str, str, str, str):
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://wave.webaim.org/api/docs?format=html")
    driver.maximize_window()
    h2_elements = driver.find_elements(By.TAG_NAME, "h2")
    headers = []
    for h2_ele in h2_elements:
        header = h2_ele.text.split('-')[0]
        header = header[:len(header)-1]
        header = header.replace(' ', '_')
        headers.append(header)
    alert_start_index = headers.index('Suspicious_alternative_text')
    features_start_index = headers.index('Alternative_text')
    strucuture_start_index = headers.index('Heading_level_1')
    aria_start_index = headers.index('ARIA')
    errors = headers[:alert_start_index]
    alerts = headers[alert_start_index:features_start_index]
    features = headers[features_start_index:strucuture_start_index]
    aria = headers[aria_start_index:]
    return errors, alerts, features, aria

def get_checkpoint_failures(data_url: [str, str]) -> (str, str):
    #error_headers, alert_headers, feature_headers, aria_headers = get_checkpoints()
    print(get_checkpoints())
    return None, None

for url in data:
    urls.append(url)
for url in urls:
    page_ranks.append(data[url][1])
    # get total number of potential points of failure. # errors + # features + # alerts // 2)
    # some alerts are not always a failure but some are so we will be generous and divide by 2
    B_p = get_total_potential_failures(data[url][0])
    # F_p = severity of the violation of barrier b we take assume each violation is as severe as each other, can be changed
    F_b = 0.05
    B_pb, N_pb = get_checkpoint_failures(data[url][0])
    ['Errors', 'Contrast_Errors','Alerts','Features']