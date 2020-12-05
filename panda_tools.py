import logging
from panda_init import *

logger = init_logging(config, __name__) 

async def create_text_channel(guild, user, name, category):
    category = [cat for cat in guild.categories if cat.name == category][0]
    logger.debug(f"Creating channel named {name} inside category {category}")
    tmp_channel = await guild.create_text_channel(name=name, category=category)
    logger.debug(f"Setting permissions for user {user}")
    await tmp_channel.set_permissions(user, read_messages=True, send_messages=True)

    logger.info(f"Channel {tmp_channel.name}"
          f" created in {tmp_channel.category}"
          f" with ID {tmp_channel.id}"
          f" on behalf of {user}")
    return tmp_channel
    
async def add_role(user, role_name):
    guild = user.guild
    logger.debug(f"Searching for the {role_name} role in guild roles: {guild.roles}")
    role = [role for role in guild.roles if role.name == role_name][0]
    await user.add_roles(role)

def channel_exists(name, guild):
    channel_exists = False
    for channel in guild.channels:
        if channel.name == name:
            channel_exists = True 
    return channel_exists

async def channel_message(guild, message, channel_name, embed=False):
    channel = [channel for channel in guild.channels if channel.name == channel_name][0]
    logger.debug(f"Printing message: {type(message)}")
    if embed:
        logger.debug(f"Printing embed message")
        await channel.send(embed=message)
    else:
        logger.debug(f"Printing message: {message}")
        await channel.send(message)
    
        
