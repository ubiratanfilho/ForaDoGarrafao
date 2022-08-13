from nba_api.stats.static import players
import pandas as pd

class Datasets():
    """ A class to represent and create datasets using different sources.
    """
    def __init__(self) -> None:
        pass
    
    def from_basketball_reference(url: str, output_path=None) -> pd.DataFrame:
        """ Create a dataset from basketball-reference.com.
        """
        from urllib.request import urlopen
        from bs4 import BeautifulSoup
        
        # URL to scrape
        url = url

        # collect HTML data
        html = urlopen(url)   
        # create beautiful soup object from HTML
        soup = BeautifulSoup(html, features="lxml")

        # use getText()to extract the headers into a list
        headers = [th.getText() 
                   for th in soup.findAll('tr', limit=2)[0].findAll('th')
                   ][1:]
        # get rows from table
        rows = soup.findAll('tr')[1:]
        rows_data = [[td.getText() for td in rows[i].findAll('td')]
                            for i in range(len(rows))]

        # create dataframe
        df = pd.DataFrame(rows_data, columns = headers)
        # save dataframe to csv
        if output_path != None:
            df.to_csv(output_path, index=False)
        return df
    
Datasets.from_basketball_reference('https://www.basketball-reference.com/leagues/NBA_2022_per_poss.html', 'data/importado/players_per100.csv')