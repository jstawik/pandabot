import discord
from discord.ext import commands
from discord_handler import DiscordHandler
import discord_logging
import json
import logging
import os
import random
from quart import Quart
app = Quart(__name__)

with open( f"{os.path.dirname(__file__)}/config.json", 'r') as file:
    config = json.loads(file.read())

pfx = config["prefix"]

bot = commands.Bot(command_prefix=pfx, intents=discord.Intents.all())

@bot.event
async def on_ready():
    logger.info(f'We have logged in as {bot.user}')
    global guild
    guild = [guild for guild in bot.guilds if guild.id == config["server_id"]][0]
    
@bot.event
async def on_member_update(before, after):
    with open( f"{os.path.dirname(__file__)}/role_message.json", 'r') as file:
        role_message = json.loads(file.read())
    
    for role_name in config["role_names"]:
        role = [role for role in guild.roles if role.name == role_name][0]
        
        if role in after.roles and role not in before.roles: 
            channel_name = f"{role.name}_{after}".lower().replace("#", "")
            
            if not channel_exists(channel_name):
                channel_category = [category for category in guild.categories if category.name == config["bot_category_name"]][0]
                channel = await create_text_channel(user=after, name=channel_name, category=channel_category)
                if role_message[role.name]:
                    logger.info(f"Sending a welcome message to a new {role.name}")
                    await channel.send(role_message[role.name])

@bot.command(name="private_channel")
async def private_channel(ctx, user: str):
    """Nowy kanał dostępny jedynie dla roli Owner oraz wybranego użytkownika"""
    try:
        user= guild.get_member_named(user)
        await create_text_channel(user=user, name=user, category=channel_category)
    except Exception as e:
        logger.info (e)
        await ctx.send('Wystąpił błąd, prawdopodobnie nie znaleziono takiej osoby')
        return

@bot.command(name="roll")
async def roll(ctx, dice: str):
    """Rzut kością, format NkN (np. 2k6 -> 2x 6 ścian)"""
    try:
        rolls, limit = map(int, dice.split('k'))
    except Exception:
        await ctx.send('Format rzutu kością musi być NkN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

async def create_text_channel(user, name, category):
    tmp_channel = await guild.create_text_channel(name=name, category=category)
    await tmp_channel.set_permissions(user, read_messages=True, send_messages=True)

    logger.info(f"Channel {tmp_channel.name}"
          f" created in {tmp_channel.category}"
          f" with ID {tmp_channel.id}"
          f" on behalf of {user}")
    return tmp_channel

@app.route('/health')
async def hello():
    return 'Alive'

def init_logging():
    logging_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename='/home/kstawik/pandabot/discord.log' 
        , format=logging_format
        , level=logging.INFO
    )

    discord_handler = DiscordHandler(config["logger_webhook"])
    discord_handler.setLevel(logging.INFO)
    discord_handler.setFormatter(logging.Formatter(logging_format))

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(logging_format))
    
    logger.addHandler(discord_handler)
    logger.addHandler(stream_handler)

    logger.debug("Logger created")

def channel_exists(name):
    channel_exists = False
    for channel in guild.channels:
        if channel.name == name:
            channel_exists = True 
    return channel_exists


guild = discord.Guild
logger = logging.getLogger('discord')

init_logging()

bot.loop.create_task(app.run_task('0.0.0.0', 5000))
bot.run(config["key"])
