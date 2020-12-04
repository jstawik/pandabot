import logging
import panda_tools
from panda_init import *
import json

logger = init_logging(config, __name__) 

@bot.event
async def on_ready():
    logger.info(f'We have logged in as {bot.user}')

@bot.event
async def on_member_update(before, after):
    guild = before.guild

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
            
            if not panda_tools.channel_exists(channel_name, guild):
                logger.debug(f"Channel {channel_name} doesn't exist. Trying to create channel")
                channel_category = [category for category in guild.categories if category.name == config["bot_category_name"]][0]
                channel = await panda_tools.create_text_channel(guild=guild, user=after, name=channel_name, category=channel_category)
                if role_message[role.name]:
                    logger.info(f"Sending a welcome message to a new {role.name}")
                    await channel.send(role_message[role.name])

