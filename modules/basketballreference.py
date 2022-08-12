from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
# URL to scrape
url = "https://www.basketball-reference.com/leagues/NBA_2022_per_poss.html"

# collect HTML data
html = urlopen(url)   
# create beautiful soup object from HTML
soup = BeautifulSoup(html, features="lxml")

# use getText()to extract the headers into a list
headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th') 
           if th.getText() != '']
# get rows from table
rows = soup.findAll('tr')[1:]
rows_data = [[td.getText() for td in rows[i].findAll('td')]
                    for i in range(len(rows))]

# create dataframe
per100 = pd.DataFrame(rows_data, columns = headers)
print(per100.head())
print(len(headers))
# save dataframe to csv
#per100.to_csv('../data/importado/players_per100.csv', index=False)