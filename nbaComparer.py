import requests

# Define the API endpoint URLs
players_url = 'https://www.balldontlie.io/api/v1/players'
season_averages_url = 'https://www.balldontlie.io/api/v1/season_averages'

# Function to get the player's ID by name
def get_player_id(player_name):
    params = {"search": player_name}
    response = requests.get(players_url, params=params)
    
    if response.status_code == 200:
        player_data = response.json()
        if player_data["data"]:
            return player_data["data"][0]["id"]
    
    return None

# Function to get the season averages for a specific player and season
def get_season_averages(player_id, season):
    params = {
        "player_ids[]": player_id,
        "season": season
    }

    response = requests.get(season_averages_url, params=params)

    if response.status_code == 200:
        season_data = response.json()
        if season_data["data"]:
            return season_data["data"][0]
    
    return None

# Example usage
player_name = input("Enter the name of the first player: ")
season = input("Enter the season you want for the first player's statistics (e.g., '2022-2023'): ")

player_id = get_player_id(player_name)

if player_id:
    season_averages = get_season_averages(player_id, season)

    if season_averages:
        print(f"Player Name: {player_name}")
        #print(f"Player ID: {player_id}")
        print(f"Season: {season}")
        print(f"Average Points: {season_averages['pts']:.1f}")
        print(f"Average Rebounds: {season_averages['reb']:.1f}")
        print(f"Average Assists: {season_averages['ast']:.1f}")
        print(f"Total Games: {season_averages['games_played']}")
    else:
        print("No season averages found.")
else:
    print(f"Player '{player_name}' not found.")


# Input values for player names and seasons
#player1Name = 
#player2Name = input("Enter the name of the second player: ")

#season1 = 
#season2 = input("Enter the season you want for the second player's statistics (e.g., '2022-2023'): ")


        
