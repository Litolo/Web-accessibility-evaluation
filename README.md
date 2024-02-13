# An Evaluation on Accessibility of Websites Based on Popularity - Source Code

## Project Description
This project aims to develop evaluate accesibility of websites. It compares seperate samples of 100 websites with varying PageRank. A comparison of government/non-government domains is also done, both by sampling 100 urls and comparing them.

## Technologies Used
- [WAVE](https://wave.webaim.org/) acessibility tool is used to find website violations. The web version of WAVE is used in this project. If you wish to extend this project you may choose to substitute for the paid API instead.
- [Selenium](https://selenium-python.readthedocs.io/) is used for automating web form submissions.

## Project structure & How to Run
[get_urls.py](get_urls.py) will first gather the 4 samples of 100 urls for high/low PageRank and government/non-government which are stored as .csv files in the [sample_data](sample_data/) folder. Note that the full url list is note included in the repo as it is very large, click [here](https://www.domcop.com/files/top/top10milliondomains.csv.zip) to download it. \
[gather_data.py](gather_data.py) will automate the running of the WAVE tool on the websites and scrape the accessibility report and save the results to .json files in the [sample_data](sample_data/) folder. \
[save_A3.py](save_A3.py) calculates the A3 accessibility score for every website and saves the results to a .csv file in the [results](results/) folder. \
Graphing and analysis is done in [generate_information.ipynb](generate_information.ipynb).
