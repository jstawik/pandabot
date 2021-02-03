import logging
import panda_tools
from panda_init import *
import json

logger = init_logging(config, __name__)

async def on_update(before, after):
    guild = after.guild
       
    for role_name in config["role_names"]:
        logger.debug(f"Searching for the configured roles in guild roles: {guild.roles}")
        role = [role for role in guild.roles if role.name == role_name][0]
        
        if role in after.roles and role not in before.roles:
            await panda_tools.add_role(after, "Panda")
            channel_name = f"{role.name}_{after}".lower().replace("#", "")
            logger.debug(f"Checking if channel {channel_name} exists")
            
            if not panda_tools.channel_exists(channel_name, after.guild):
                logger.debug(f"Channel {channel_name} doesn't exist. Trying to create channel")
                channel = await panda_tools.create_text_channel(guild=guild, user=after, name=channel_name, category=config["bot_category_name"])
                await welcome_user(channel, role)

async def welcome_user(channel, role):
    with open( f"{config_path}/role_message.json", 'r') as file:
        role_message = json.loads(file.read())
    
    if role_message[role.name]:
        logger.info(f"Sending a welcome message to a new {role.name}")
        await channel.send(role_message[role.name])
