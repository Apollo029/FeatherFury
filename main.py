# main.py
import discord
from core.bot import FeatherFuryBot
import json
import traceback

try:
    # Load the bot token from config.json
    with open("config.json", "r") as f:
        config = json.load(f)
    bot_token = config.get("token")
    if not bot_token:
        raise ValueError("Bot token not found in config.json")

    # Initialize and run the bot
    bot = FeatherFuryBot()
    bot.run(bot_token)
except FileNotFoundError:
    print("Error: config.json file not found. Please create config.json with your bot token.")
except json.JSONDecodeError:
    print("Error: config.json is not a valid JSON file.")
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print("Error during bot startup:")
    print(traceback.format_exc())
