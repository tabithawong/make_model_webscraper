# importing packages
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

# constant, only looking at models from 2010 and onwards
start_year = 2010

# change path if file gets moved
df = pd.read_excel("/Users/tabithawong/Documents/make_model_webscraper/make_model(1).xlsx")

# creating the dictionary of all boat makes from the excel file, the end year is the key
# CHANGE HERE
df = df[df['Type'] == "Snowmobile"]
# creating the list of all boat makes from the excel file
boat_makes_dict = df.set_index('Make')['End Year'].to_dict()

# creating dictionary of URLs for each boat make
# data structure:
    # key: boat make as a string
    # value: list of url strings
url_dict = {}

for boat in boat_makes_dict:
    make_urls = []
    # cleaning up the data in the spreadsheet
    clean_boat = boat.replace("&", "and")
    final_boat = clean_boat.replace(" ", "-")
    end_year = boat_makes_dict[boat] + 1
    for year in range(start_year, end_year):
        # building the URL and adding it to the dictionary
        # CHANGE HERE
        url = "https://www.jdpower.com/motorcycles/" + str(year) + "/" + final_boat.lower()
        make_urls.append(url)
    # setting the dictionary value to be the list of URLs
    url_dict[boat] = make_urls

makes_list = []
models_list = []
# iterating through the makes in the dictionary
for make in url_dict:
    make_name = make
    # iterating through the URLs in each list 
    for url in url_dict[make]:
        #print(url)
        URL = url
        url_split = int(url.split("/")[4])
        # sleep to prevent DDOS
        time.sleep(0.5)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        # checking if page exists on JD Power
        if (len(soup.find_all('h1', string="Sorry, We Couldn't Find That Page")) > 0):
            # skip if the page doesn't exist
            continue
        else: 
            # setting up the soup (parsing through the html on the URL)
            results = soup.find_all('a', class_ = '', href = True)
            for r in results:
                if (r['href'].find("/motorcycles") != -1):
                    index_model = r.text.replace("\r\n                            ","")
                    # removing second \r\n
                    model = index_model.replace("    ","")
                    if (models_list.count(model.upper()) == 0):
                        #print("here")
                        makes_list.append(make_name.upper())
                        models_list.append(model.upper())
    # print statement to track progress through the different makes
    print("Done "+make_name)
# names of columns
names = ['Make','Model']
# making dataframe and writing to Excel
df = pd.DataFrame(list(zip(makes_list, models_list)), columns=names)
print(df)
# CHANGE HERE
df.to_excel("jetski_models.xlsx")
print("DONE!")
