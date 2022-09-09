# import urrlib 
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
    
    def get_json_from_name(name: str, is_player=True) -> int:
        """ Get the json of a player or team from his name
        """
        from nba_api.stats.static import players, teams
        if is_player:
            nba_players = players.get_players()
            return [player for player in nba_players 
                    if player['full_name'] == name][0]
        else:
            nba_teams = teams.get_teams()
            return [team for team in nba_teams 
                    if team['full_name'] == name][0]
    
    def get_player_career(player_id: int) -> list:
        """ Get the career of a player from his id
        """
        from nba_api.stats.endpoints import playercareerstats
        career = playercareerstats.PlayerCareerStats(player_id=player_id)
        return career.get_data_frames()[0]
    
    def get_shot_data(id, team_ids, seasons) -> list:
        """ Get the shot data of a player from his id and seasons
        """
        from nba_api.stats.endpoints import shotchartdetail
        df = pd.DataFrame()
        for season in seasons:
            for team in team_ids:
                shot_data = shotchartdetail.ShotChartDetail(
                    team_id=team,
                    player_id=id,
                    context_measure_simple='FGA',
                    season_nullable=season
                )
                df = pd.concat([df, shot_data.get_data_frames()[0]])
        
        return df
    
    def get_all_ids(only_active=True) -> list:
        """ Get all the ids of the players
        """
        from nba_api.stats.static import players
        nba_players = players.get_players()
        if only_active:
            return [player['id'] for player in nba_players 
                    if player['is_active']]
        return [player['id'] for player in nba_players]
    
    def get_player_headshot(id) -> None:
            """ Get the headshot of a player from his id
            """
            from nba_api.stats.static import players
            import requests
            import shutil
            url = f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{id}.png'
            output_path = f'../../data/importado/headshots/{id}.png'
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(output_path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    
    def get_all_nba_headshots(only_active=False) -> None:
        """ Get the headshots of all the players
        """
        from nba_api.stats.static import players
        import requests
        import shutil
        ids = Datasets.get_all_ids(only_active=only_active)
        for id in ids:
            Datasets.get_player_headshot(id)
                    
        
                            
        

if __name__ == '__main__':
    # Datasets.from_basketball_reference('https://www.basketball-reference.com/leagues/NBA_2022_per_poss.html', 'data/importado/players_per100.csv')
    
    Datasets.get_all_nba_headshots(True)
