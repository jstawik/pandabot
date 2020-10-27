import discord
from discord.ext import commands
import json
import os
import random

with open( f"{os.path.dirname(__file__)}/config.json", 'r') as file:
    config = json.loads(file.read())

pfx = config["prefix"]
bot = commands.Bot(command_prefix=pfx, intents=discord.Intents.all())

guild = discord.Guild
channel_category = discord.CategoryChannel
role = discord.Role

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    global guild
    guild = [guild for guild in bot.guilds if guild.id == config["server_id"]][0]
    global channel_category
    channel_category = [category for category in guild.categories if category.name == config["bot_category_name"]][0]
    global role
    role = [role for role in guild.roles if role.name == config["role_name"]][0]

@bot.event
async def on_member_update(before, after):
    if role in after.roles and role not in before.roles:
        await create_text_channel(name=after, category=channel_category)

@bot.command(name="kursant_channel")
async def kursant_channel(ctx, kursant: str):
    """Nowy kanał dla potencjalnego kursanta"""
    try:
        await create_text_channel(name=guild.get_member_named(kursant), category=channel_category)
    except Exception as e:
        print (e)
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

async def create_text_channel(name, category):
    tmp_channel = await guild.create_text_channel(name=f"{name}", category=category)
    await tmp_channel.set_permissions(name, read_messages=True, send_messages=True)
    print(f"Channel {tmp_channel.name}"
          f" created in {tmp_channel.category}"
          f" with ID {tmp_channel.id}"
          f" on behalf of {name}")

bot.run(config["key"])
