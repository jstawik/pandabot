import logging
import panda_tools
import panda_roles
from panda_init import *
import json

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
            await panda_tools.channel_message(after.guild, e, "pandabot-log")
