# importing packages
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = "https://www.jdpower.com/motorcycles/2010/aprilia"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
final = []
# checking if page exists on JD Power
results = soup.find_all('a', class_ = '', href = True)
for r in results:
    if (r['href'].find("/motorcycles") != -1):
        index_model = r.text.replace("\r\n                            ","")
                # removing second \r\n
        split_index = index_model.replace("    ","")
        final.append(split_index)

print(final)

