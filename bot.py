import discord
import os
from dotenv import load_dotenv
# Import the functions from player_data.py
from nbaComparer import find_player_id, get_season_averages

# Function to process and send messages
async def send_message(channel, user_message):
    try:
        # Check if the message is a command for player data
        if user_message.startswith('!player'):
            parts = user_message.split()
            if len(parts) < 3:
                response = "Usage: !player [player_name] [season]"
            else:
                player_name = " ".join(parts[1:-1])
                season = parts[-1]
                response = get_season_averages(player_name, season)
        else:
            response = "Invalid command."

        await channel.send(response)
    except Exception as e:
        print(e)

# Discord bot setup and event handlers
def run_discord_bot():
    load_dotenv()
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        # Process messages that start with '!'
        if message.content.startswith('!'):
            await send_message(message.channel, message.content)

    client.run(os.getenv('API_KEY'))

# Uncomment the line below to run the bot (if running this script directly)
run_discord_bot()