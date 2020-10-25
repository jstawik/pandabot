import discord
import json

with open("config.json", 'r') as file:
    config = json.loads(file.read())

client = discord.Client(intents=discord.Intents.all())
pfx = config["prefix"]

guild = discord.Guild
channel_category = discord.CategoryChannel
role = discord.Role
reaction_channel = discord.TextChannel
reaction_message = discord.Message


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    global guild
    guild = [guild for guild in client.guilds if guild.id == config["server_id"]][0]
    global channel_category
    channel_category = [category for category in guild.categories if category.name == config["bot_category_name"]][0]
    global role
    role = [role for role in guild.roles if role.name == config["role_name"]][0]
    global reaction_channel
    reaction_channel = [channel for channel in guild.channels if channel.id == config["reaction_channel_id"]][0]
    global reaction_message
    reaction_message = reaction_channel.fetch_message(config["reaction_message_id"])


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(f'{pfx}new'):
        tmp_channel = await guild.create_text_channel(name=f"{message.author}", category=channel_category)
        await tmp_channel.set_permissions(message.author, read_messages=True, send_messages=True)
        print(f"Channel {tmp_channel.name}"
              f" created in {tmp_channel.category}"
              f" with ID {tmp_channel.id}"
              f" on behalf of {message.author}")


@client.event
async def on_member_update(before, after):
    if role in after.roles and role not in before.roles:
        tmp_channel = await guild.create_text_channel(name=f"{after}", category=channel_category)
        await tmp_channel.set_permissions(after, read_messages=True, send_messages=True)
        print(f"Channel {tmp_channel.name}"
              f" created in {tmp_channel.category}"
              f" with ID {tmp_channel.id}"
              f" on behalf of {after}")

client.run(config["key"])
