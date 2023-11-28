import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv
from time import sleep
# to do a independent t test on errors we need to first compute the A3 aggregation score for each website.
# Please see the report on what each variable does if you are confused

# needs refactoring
def get_checkpoints() -> (str, str, str, str):
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://wave.webaim.org/api/docs?format=html")
    h2_elements = driver.find_elements(By.TAG_NAME, "h2")
    headers = []
    for h2_ele in h2_elements:
        header = h2_ele.text.split('-')[0]
        header = header[:len(header)-1]
        header = header.replace(' ', '_')
        headers.append(header)
    driver.close()
    alert_start_index = headers.index('Suspicious_alternative_text')
    features_start_index = headers.index('Alternative_text')
    strucuture_start_index = headers.index('Heading_level_1')
    aria_start_index = headers.index('ARIA')
    errors = headers[:alert_start_index]
    alerts = headers[alert_start_index:features_start_index]
    features = headers[features_start_index:strucuture_start_index]
    aria = headers[aria_start_index:]
    return (errors, alerts, features, aria)

# this is so bad. Needs refactoring if there is time
def compute_A3(data_url: [str, str], url: str, F_b: int, checkpoint_headers: ([str], [str], [str], [str]) = get_checkpoints()) -> int:
    error_headers, alert_headers, feature_headers, aria_headers = checkpoint_headers[0], checkpoint_headers[1], checkpoint_headers[2], checkpoint_headers[3]
    missing_alt_no = 0
    form_label_err_no = 0
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://"+url)
    # let the page load
    sleep(10)
    # get alt text information
    img_elements = driver.find_elements(By.TAG_NAME, "img")
    long_desc_imgs_amount = len([x for x in img_elements if x.get_attribute('longdesc')])
    map_elements = driver.find_elements(By.TAG_NAME, 'map')
    space_elements = driver.find_elements(By.TAG_NAME, 'spacer')
    area_elements = driver.find_elements(By.TAG_NAME, 'area') # used inside maps
    possible_alt_violations = len(img_elements + map_elements + space_elements + area_elements)
    # get form control label information
    possible_form_violations = len(driver.find_elements(By.TAG_NAME, "input"))
    # ignoring longdesc error since it is depricated
    total_headings_no = len(driver.find_elements(By.TAG_NAME, "h1") + driver.find_elements(By.TAG_NAME, "h2") +
                            driver.find_elements(By.TAG_NAME, "h3") + driver.find_elements(By.TAG_NAME, "h4")+ 
                            driver.find_elements(By.TAG_NAME, "h5") + driver.find_elements(By.TAG_NAME, "h6"))
    total_buttons_no = len(driver.find_elements(By.TAG_NAME, "button"))
    all_links = driver.find_elements(By.TAG_NAME, "a")
    total_links_no = len(all_links)
    #skip_links_no = len([x for x in all_links if "#" in x.get_attribute('href')]) -> need to handle empty href
    skip_links_no = 0
    for x in all_links:
        try:
            if '#' in x.get_attribute('href'):
                skip_links_no += 1
        except:
            continue
    table_headers_no = len(driver.find_elements(By.TAG_NAME, "th"))
    # we will use this to estimate how many possible contrast errors there are we will take any
    # element with text to be a possible contrast error
    total_text_elements = len(driver.find_elements(By.XPATH, "//*[text()]"))
    violations = []
    possible_violations = []
    for error_header in error_headers:
        if "missing_alternative" in error_header.lower():
            try:
                missing_alt_no += data_url[error_header]
            # if key error then violation was not found
            except KeyError:
                continue
        elif 'longdesc' in error_header.lower():
            if missing_alt_no != 0:
                violations.append(missing_alt_no)
                possible_violations.append(possible_alt_violations)
            try:
                violations.append(data_url[error_header])
                possible_violations.append(long_desc_imgs_amount)
            except KeyError:
                continue
        elif 'form_label' in error_header.lower():
            try:
                form_label_err_no += data_url[error_header]
            except KeyError:
                continue
        elif 'aria_reference' in error_header.lower():
            if form_label_err_no != 0:
                violations.append(form_label_err_no)
                possible_violations.append(possible_form_violations)
            try:
                violations.append(data_url[error_header])
                possible_violations.append(int(data_url['ARIA']))
            except KeyError:
                continue
        elif 'aria_menu' in error_header.lower():
            try:
                violations.append(data_url[error_header])
                # check
                possible_violations.append(int(data_url['ARIA_menu']))
            except KeyError:
                continue
        elif 'page_title' in error_header.lower():
            try:
                violations.append(data_url[error_header])
                # check
                possible_violations.append(1)
            except KeyError:
                continue
        elif 'language' in error_header.lower():
            try:
                violations.append(data_url[error_header])
                #  technically there can be more than one language per page
                possible_violations.append(data_url[error_header])
            except KeyError:
                continue
        elif 'empty_heading' in error_header.lower():
            try:
                violations.append(data_url[error_header])
                possible_violations.append(total_headings_no)
            except KeyError:
                continue
        elif 'empty_button' in error_header.lower():
            try:
                violations.append(data_url[error_header])
                possible_violations.append(total_buttons_no)
            except KeyError:
                continue
        elif 'empty_link' in error_header.lower():
            try:
                violations.append(data_url[error_header])
                possible_violations.append(total_links_no)
            except KeyError:
                continue
        elif 'skip_link' in error_header.lower():
            try:
                violations.append(data_url[error_header])
                possible_violations.append(skip_links_no)
            except KeyError:
                continue
        elif 'table_header' in error_header.lower():
            try:
                violations.append(data_url[error_header])
                possible_violations.append(table_headers_no)
            except KeyError:
                continue
        elif 'blinking_content' in error_header.lower():
            try:
                violations.append(data_url[error_header])
                possible_violations.append(data_url[error_header])
            except KeyError:
                continue
        elif 'marquee' in error_header.lower():
            try:
                violations.append(data_url[error_header])
                possible_violations.append(data_url[error_header])
            except KeyError:
                continue
        elif 'low_contrast' in error_header.lower():
            try:
                violations.append(data_url[error_header])
                if int(data_url[error_header]) > total_text_elements:
                    possible_violations.append(data_url[error_header])
                else:
                    possible_violations.append(total_text_elements)
            except KeyError:
                continue

    B_pb_vals = violations
    N_pb_vals = possible_violations
    product_val = 0
    B_p = sum(B_pb_vals)
    for i in range(len(B_pb_vals)):
        if product_val == 0:
            product_val = pow((1-F_b), ((B_pb_vals[i]/N_pb_vals[i]) + (B_pb_vals[i] / B_p)))
        else:
            product_val *= pow((1-F_b), ((B_pb_vals[i]/N_pb_vals[i]) + (B_pb_vals[i] / B_p)))
    return 1 - product_val

def get_A3_to_file(json_filepath: str, outpout_filepath: str) -> None:
    f = open(json_filepath)
    data = json.load(f)
    urls = []
    checkpoint_headers = get_checkpoints()
    for url in data:
        urls.append(url)
    with open(outpout_filepath, 'w', newline='') as csvwrite:
        writer = csv.writer(csvwrite)
        writer.writerow(["Wesbite URL", "A3 Value", "PageRank"])
        for url in urls:
            # get total number of potential points of failure. # errors + # features + # alerts // 2)
            # some alerts are not always a failure but some are so we will be generous and divide by 2
            # F_p = severity of the violation of barrier b we take assume each violation is as severe as each other
            # usually this value can change the severity of violations based on the disability group we are testing for 
            # (i.e. blind will care more about no alt text than deaf)
            F_b = 0.1
            # if a selenium error then just try again 10 times
            for i in range(5):
                try:
                    a3 = compute_A3(data[url][0], url, F_b, checkpoint_headers = checkpoint_headers)
                    writer.writerow([url, a3, data[url][1]])   
                    break
                except Exception as err:
                    print(err)
            else:
                print(url, "did not work, likely something is wrong with the website")
    csvwrite.close()
    return

get_A3_to_file('sample_data/high_pagerank_error_data.json', 'results/A3_high_pagerank_results.csv')
get_A3_to_file('sample_data/low_pagerank_error_data.json', 'results/A3_low_pagerank_results.csv')
get_A3_to_file('sample_data/government_error_data.json','results/A3_government_results.csv')
get_A3_to_file('sample_data/non_government_error_data.json','results/A3_non_government_results.csv')


