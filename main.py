
from panda_init import *
import healthcheck
import panda_tools
import bot_commands

import json

guild = discord.Guild

@bot.event
async def on_ready():
    logger.info(f'We have logged in as {bot.user}')
    global guild
    guild = [guild for guild in bot.guilds if guild.id == config["server_id"]][0]

@bot.event
async def on_member_update(before, after):
    logger.debug(f"Member update from {before} to {after} ")
    
    with open( f"{config_path}/role_message.json", 'r') as file:
        role_message = json.loads(file.read())
    
    for role_name in config["role_names"]:
        logger.debug(f"Searching for the configured roles in guild roles: {guild.roles}")
        role = [role for role in guild.roles if role.name == role_name][0]
        
        if role in after.roles and role not in before.roles:
            logger.debug(f"Searching for the panda role in guild roles: {guild.roles}")
            panda_role = [role for role in guild.roles if role.name == "Panda"][0]
            await after.add_roles(panda_role)
            channel_name = f"{role.name}_{after}".lower().replace("#", "")
            logger.debug(f"Checking if channel {channel_name} exists")
            
            if not channel_exists(channel_name):
                logger.debug(f"Channel {channel_name} doesn't exist. Trying to create channel")
                channel_category = [category for category in guild.categories if category.name == config["bot_category_name"]][0]
                channel = await panda_tools.create_text_channel(guild=guild, user=after, name=channel_name, category=channel_category)
                if role_message[role.name]:
                    logger.info(f"Sending a welcome message to a new {role.name}")
                    await channel.send(role_message[role.name])

def channel_exists(name):
    channel_exists = False
    for channel in guild.channels:
        if channel.name == name:
            channel_exists = True 
    return channel_exists


# async def create_text_channel(user, name, category):
#     tmp_channel = await guild.create_text_channel(name=name, category=category)
#     await tmp_channel.set_permissions(user, read_messages=True, send_messages=True)

#     logger.info(f"Channel {tmp_channel.name}"
#           f" created in {tmp_channel.category}"
#           f" with ID {tmp_channel.id}"
#           f" on behalf of {user}")
#     return tmp_channel


logger = init_logging(config, __name__) 

bot.loop.create_task(healthcheck.app.run_task('0.0.0.0', 5000))
bot.run(config["key"])
