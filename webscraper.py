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
for boat in boat_makes_list:
    make_urls = []
    clean_boat = boat.replace("&", "and")
    final_boat = clean_boat.replace(" ", "-")
    for year in range(2010,2023):
        # check if year exists (check for not found error on page)
        # do a sleep
        url = "https://www.jdpower.com/boats/" + str(year) + "/" + final_boat.lower()
        make_urls.append(url)
    # setting the dictionary value to be the list of URLs
    url_dict[boat] = make_urls

# iterating through the makes in the dictionary
makes_list = []
models_list = []
for make in url_dict:
    make_name = make
    # iterating through the URLs in each list 
    for url in url_dict[make]:
        URL = url
        time.sleep(0.5)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        # checking if page exists on JD Power     
        if (len(soup.find_all('h1', string="Sorry, We Couldn't Find That Page")) > 0):
            # skip if the page doesn't exist
            #print(URL)
            continue
        else: 
            # setting up the soup (parsing through the html on the URL)
            results = soup.find_all('a', attrs={"class":"detail-row__link detail-row__link--fixed-width"})
            # grabbing all the model names
            #for result in results:
            for result in results:
                # cleaning up the results and removing \r\n
                raw_model = result.text
                # removing first \r\n
                index_model = raw_model.replace("\r\n                                        ","")
                # removing second \r\n
                split_index = (index_model.index("\r\n"))
                model = index_model[0:split_index]
                # adding to a list of makes and models to make writing to Excel easier
                makes_list.append(make_name.upper())
                models_list.append(model.upper())
    print("Done "+make_name)
# names of columns
names = ['Make','Model']
# making dataframe and writing to Excel
df = pd.DataFrame(list(zip(makes_list, models_list)), columns=names)
df.to_excel("models.xlsx")
print("DONE!")
