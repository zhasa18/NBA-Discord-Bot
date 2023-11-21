import requests
import sqlite3

def create_database():
    connection = sqlite3.connect('nbatrix.db')
    cursor = connection.cursor()

    # Create a table
    cursor.execute('''CREATE TABLE IF NOT EXISTS players
                      (id INTEGER PRIMARY KEY,
                       name TEXT,
                       season INTEGER,
                       points REAL,
                       rebounds REAL,
                       assists REAL,
                       steals REAL,
                       blocks REAL)''')

    connection.commit()
    connection.close()

create_database()

def find_player_id(player_name):
    """
    Find the player ID based on the player's name.
    """
    url = "https://www.balldontlie.io/api/v1/players"
    params = {"search": player_name}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        players = response.json()['data']
        for player in players:
            if player_name.lower() in (player['first_name'].lower() + " " + player['last_name'].lower()):
                return player['id']
    return None



def get_season_averages(player_name, season):
    connection = sqlite3.connect('nbatrix.db')
    cursor = connection.cursor()

    # Check if data is already in the database
    cursor.execute("SELECT * FROM players WHERE name=? AND season=?", (player_name, season))
    data = cursor.fetchone()

    if data:
        stats_output = f"Season Averages for {player_name} ({season} Season):\n"
        stats_output += f"- Points: {data[3]}\n"
        stats_output += f"- Rebounds: {data[4]}\n"
        stats_output += f"- Assists: {data[5]}\n"
        stats_output += f"- Steals: {data[6]}\n"
        stats_output += f"- Blocks: {data[7]}"
        connection.close()
        return stats_output

    # If data not found in database, fetch from API
    player_id = find_player_id(player_name)
    if player_id is None:
        connection.close()
        return f"No player found with the name {player_name}"

    url = "https://www.balldontlie.io/api/v1/season_averages"
    params = {"season": season, "player_ids[]": [player_id]}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        stats = response.json().get('data', [])
        if stats:
            stats = stats[0]
            stats_output = f"Season Averages for {player_name} ({season} Season):\n"
            stats_output += f"- Points: {round(stats.get('pts', 0), 1)}\n"
            stats_output += f"- Rebounds: {round(stats.get('reb', 0), 1)}\n"
            stats_output += f"- Assists: {round(stats.get('ast', 0), 1)}\n"
            stats_output += f"- Steals: {round(stats.get('stl', 0), 1)}\n"
            stats_output += f"- Blocks: {round(stats.get('blk', 0), 1)}"

            # Save data to database
            cursor.execute("INSERT INTO players (name, season, points, rebounds, assists, steals, blocks) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (player_name, season, round(stats.get('pts', 0), 1), round(stats.get('reb', 0), 1), round(stats.get('ast', 0), 1), round(stats.get('stl', 0), 1), round(stats.get('blk', 0), 1)))
            connection.commit()
            connection.close()
            return stats_output
        else:
            connection.close()
            return "No data available for this player and season."
    else:
        connection.close()
        return "Failed to retrieve data from API."

# # Example usage
# player_name = "LeBron James"  # Replace with the player's name
# season = 2018  # Replace with the desired season
# print(get_season_averages(player_name, season))
