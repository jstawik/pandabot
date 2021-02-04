import json
import discord
from discord.ext import commands
import logging
# import discord_logging #### TODO - discord logs handling

config_path = "/home/kstawik/.pandacfg"
config_file = "config.json"

with open( f"{config_path}/{config_file}", 'r') as file:
    config = json.loads(file.read())

logger = logging.getLogger(__name__)
logger.debug(f"Initalized logging for {__name__} module")

bot = commands.Bot(command_prefix=config["prefix"], intents=discord.Intents.all())

def init_logging(config, name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    #### TODO - discord logs handling
    # discord_handler = DiscordHandler(webhook, application, notify_users="nobody")
    # discord_handler = discord_logging.Discord_Handler(webhook)
    # discord_handler.setLevel(logging.DEBUG)
    # discord_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(config["log_path"])
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # logger.addHandler(discord_handler) #### TODO - discord logs handling
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    logger.debug("Logger created")
    return logger

logger = init_logging(config, __name__)
