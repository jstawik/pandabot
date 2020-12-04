# from main import logger, guild, bot
# import tools
# import discord
# from discord.ext import commands
# from discord_handler import DiscordHandler
# import discord_logging
# import json
# import os
# import random

# logger = init_logging(config, __name__) 

# @bot.event
# async def on_ready():
#     logger.info(f'We have logged in as {bot.user}')
#     global guild
#     guild = [guild for guild in bot.guilds if guild.id == config["server_id"]][0]

# # @client.event
# # async def on_member_join(member):
# #     await member.send("Welcome!")

# @bot.event
# async def on_member_update(before, after):
#     panda_role = [role for role in guild.roles if role.name == "Panda"][0]
#     with open( f"{config_path}/role_message.json", 'r') as file:
#         role_message = json.loads(file.read())
    
#     for role_name in config["role_names"]:
#         role = [role for role in guild.roles if role.name == role_name][0]
        
#         if role in after.roles and role not in before.roles:
#             await after.add_roles(panda_role) 
#             channel_name = f"{role.name}_{after}".lower().replace("#", "")
            
#             if not panda_tools.channel_exists(channel_name):
#                 channel_category = [category for category in guild.categories if category.name == config["bot_category_name"]][0]
#                 channel = await panda_tools.create_text_channel(user=after, name=channel_name, category=channel_category)
#                 if role_message[role.name]:
#                     logger.info(f"Sending a welcome message to a new {role.name}")
#                     await channel.send(role_message[role.name])