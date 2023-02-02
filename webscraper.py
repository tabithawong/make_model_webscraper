# importing packages
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

# change path if file gets moved
makes = pd.read_excel("/Users/tabithawong/Documents/make_model_webscraper/make_model(1).xlsx")

# creating the list of all boat makes from the excel file
boat_makes_list = []
for boat_make in makes[makes['Type'] == "Boat"]['Make']:
    boat_makes_list.append(boat_make)

# creating dictionary of URLs for each boat make
# data structure:
    # key: boat make as a string
    # value: list of url strings
url_dict = {}
make_urls = []
for boat in boat_makes_list:
    clean_boat = boat.replace("&", "and")
    final_boat = clean_boat.replace(" ", "-")
    for year in range(2010,2023):
        # check if year exists (check for not found error on page)
        # do a sleep
        url = "https://www.jdpower.com/boats/" + str(year) + "/" + final_boat.lower()
        make_urls.append(url)
    url_dict[boat] = make_urls

# iterating through the makes in the dictionary
for make in url_dict:
    # iterating through the  
    for url in url_dict[make]:
        URL = url
        print(URL)
        time.sleep(3)
        page = requests.get(URL)
        # setting up the soup (parsing through the html on the URL)
        soup = BeautifulSoup(page.content, "html.parser")
        # finding all elements that have the specified class in the soup
        results = soup.find_all('a', attrs={"class":"detail-row__link detail-row__link--fixed-width"})
        models_list = []
        # grabbing all the names
        for result in results:
            # cleaning up the results and removing \r\n
            raw_model = result.text
            # removing first \r\n
            index_model = raw_model.replace("\r\n                                        ","")
            # removing second \r\n
            split_index = (index_model.index("\r\n"))
            model = index_model[0:split_index]
            # adding model to the list
            models_list.append(model)
        print(models_list)