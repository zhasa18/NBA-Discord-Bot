import requests
import sqlite3

# Define the API endpoint URLs
players_url = 'https://www.balldontlie.io/api/v1/players'
season_averages_url = 'https://www.balldontlie.io/api/v1/season_averages'

# Create or connect to the database
conn = sqlite3.connect('nba_stats.db')
cursor = conn.cursor()

# Create a Players table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Players (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

# Create a SeasonAverages table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS SeasonAverages (
        id INTEGER PRIMARY KEY,
        player_id INTEGER,
        season TEXT,
        avg_points REAL,
        avg_rebounds REAL,
        avg_assists REAL,
        total_games INTEGER
    )
''')

# Commit changes
conn.commit()

# Function to get the player's ID by name
def get_player_id(player_name):
    # Check if the player is in the database
    cursor.execute('SELECT id FROM Players WHERE name = ?', (player_name,))
    player_id = cursor.fetchone()

    if player_id:
        return player_id[0]

    # If not found in the database, fetch from the API
    params = {"search": player_name}
    response = requests.get(players_url, params=params)

    if response.status_code == 200:
        player_data = response.json()
        if player_data["data"]:
            # Insert the player name into the database
            cursor.execute('INSERT INTO Players (name) VALUES (?)', (player_name,))
            conn.commit()
            return player_data["data"][0]["id"]

    return None

# Function to get the season averages for a specific player and season
def get_season_averages(player_name, season):
    player_id = get_player_id(player_name)

    # Check the database for season averages
    cursor.execute('''
        SELECT avg_points, avg_rebounds, avg_assists, total_games
        FROM SeasonAverages
        WHERE player_id = ? AND season = ?
    ''', (player_id, season))
    
    season_averages = cursor.fetchone()
    
    if season_averages:
        return {
            "average_points": season_averages[0],
            "average_rebounds": season_averages[1],
            "average_assists": season_averages[2],
            "total_games": season_averages[3]
        }
    else:
        # If not found in the database, fetch from the API
        params = {
            "player_ids[]": player_id,
            "season": season
        }

        response = requests.get(season_averages_url, params=params)

        if response.status_code == 200:
            season_data = response.json()
            if season_data["data"]:
                # Insert season averages data into the database
                avg_points = season_data["data"][0]["pts"]
                avg_rebounds = season_data["data"][0]["reb"]
                avg_assists = season_data["data"][0]["ast"]
                total_games = season_data["data"][0]["games_played"]

                cursor.execute('''
                    INSERT INTO SeasonAverages (player_id, season, avg_points, avg_rebounds, avg_assists, total_games)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (player_id, season, avg_points, avg_rebounds, avg_assists, total_games))

                conn.commit()

                return {
                    "average_points": avg_points,
                    "average_rebounds": avg_rebounds,
                    "average_assists": avg_assists,
                    "total_games": total_games
                }

    return None

# Example usage
player_name = input("Enter the name of the player: ")
season = input("Enter the season you want for the player's statistics (e.g., '2022-2023'): ")

season_averages = get_season_averages(player_name, season)

if season_averages:
    print(f"Player Name: {player_name}")
    print(f"Season: {season}")
    print(f"Average Points: {season_averages['average_points']:.1f}")
    print(f"Average Rebounds: {season_averages['average_rebounds']:.1f}")
    print(f"Average Assists: {season_averages['average_assists']:.1f}")
    print(f"Total Games: {season_averages['total_games']}")
else:
    print(f"No data found for {player_name} in the {season} season.")

# Close the database connection
conn.close()



