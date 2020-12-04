import logging
from panda_init import *

logger = init_logging(config, __name__) 

async def create_text_channel(guild, user, name, category):
    tmp_channel = await guild.create_text_channel(name=name, category=category)
    await tmp_channel.set_permissions(user, read_messages=True, send_messages=True)

    logger.info(f"Channel {tmp_channel.name}"
          f" created in {tmp_channel.category}"
          f" with ID {tmp_channel.id}"
          f" on behalf of {user}")
    return tmp_channel
    
# def channel_exists(name):
#     channel_exists = False
#     for channel in guild.channels:
#         if channel.name == name:
#             channel_exists = True 
#     return channel_exists



