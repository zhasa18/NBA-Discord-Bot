# NBAtrix Discord Bot

## Overview
NBAtrix is a Discord bot designed for basketball enthusiasts. It provides up-to-date statistics and information about NBA players directly within your Discord server. With simple commands, users can query season averages and other relevant data for their favorite NBA players.

## Features
- **Player Statistics**: Retrieve the season averages for any NBA player by specifying the player's name and the season.
- **Easy Interaction**: Simple command structure for easy interaction within any Discord server.
- **Real-time Data**: Fetches the latest available data from the "balldontlie" API for accurate and current statistics.

## Setup and Installation
To set up NBAtrix in your own Discord server, follow these steps:

1. **Clone the Repository**

```
git clone https://github.com/redski18/NBAtrix.git
```

2. **Install Dependencies**
- Ensure you have Python 3.x installed.
- Install required Python packages:
  ```
  pip install requests
  ```
  ```
  pip install discord.py
  ```
  ```
  pip install python-dotenv
  ```

3. **Discord Bot Token**
- Create a Discord bot on the [Discord Developer Portal](https://discord.com/developers/applications).
- Copy the bot token and add it to a `.env` file in the root directory:
  ```
  API_KEY=your_discord_bot_token_here
  ```

4. **Run the Bot**


## Usage
Once NBAtrix is running in your Discord server, you can use the following commands:

- `!player [player_name] [season]`: Retrieves the season averages for the specified player and season. Example: `!player LeBron James 2020`.

## Contributing
Contributions to NBAtrix are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for more information on how you can contribute.

## License
NBAtrix is released under the [MIT License](LICENSE).
