import logging
import panda_tools
import panda_roles
from panda_init import *
import json
from datetime import datetime

logger = init_logging(config, __name__)

@bot.event
async def on_ready():
    logger.info(f'We have logged in as {bot.user}')

@bot.event
async def on_member_update(before, after):
    logger.debug(f"Member update from {before} to {after}")

    if len(before.roles) < len(after.roles):
        try:
            await panda_roles.on_role_update(before, after)
        except Exception as e:
            logger.warning(e)
            await panda_tools.channel_message(after.guild, e, "pandabot-log", "Techniczne")

@bot.event
async def on_member_join(member):
    try:
        logger.debug(f"Przyszedł użytkownik {member.name}")
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        embed=discord.Embed(title=member.name, description=" ", color=0x808000)
        embed.add_field(name="NOWA PANDA !", value=f"Data: {now} ", inline=False)
        logger.debug(f"Printing {embed}")
        await panda_tools.channel_message(member.guild, embed, config["user_info_category_name"], "Zarząd", embed=True)
    except Exception as e:
        logger.warning(e)
        await panda_tools.channel_message(member.guild, e, "pandabot-log", "Techniczne")

@bot.event
async def on_member_remove(member):
    try:
        logger.debug(f"Odszedł użytkownik {member.name}")
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        embed=discord.Embed(title=member.name, description=" ", color=0x8d8d8d)
        embed.add_field(name="SAD PANDA ! Odszedł nam użytkownik", value=f"Data: {now} ", inline=False)
        logger.debug(f"Printing {embed}")
        await panda_tools.channel_message(member.guild, embed, config["user_info_category_name"], "Zarząd", embed=True)
    except Exception as e:
        logger.warning(e)
        await panda_tools.channel_message(member.guild, e, "pandabot-log", "Techniczne")
