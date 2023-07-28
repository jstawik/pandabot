import logging
import panda_tools
import panda_roles
from panda_init import *
import random

logger = init_logging(config, __name__) 

# @bot.command(name="private_channel")
# async def private_channel(ctx, user_id, channel_category):
#     """Nowy kanał dostępny jedynie dla roli Owner oraz wybranego użytkownika"""
#     try:
#         logger.debug(f"Looking for user id {user_id}")
#         user = ctx.guild.get_member(int(user_id))
#         logger.info(f"Found user with id {user_id}: {user}")
#         await panda_tools.create_text_channel(ctx.guild, user, user.name, channel_category )
#     except Exception as e:
#         logger.warning (e)
#         await ctx.send('Wystąpił błąd, prawdopodobnie nie znaleziono takiej osoby')
#         await panda_tools.channel_message(ctx.guild, e, "pandabot-log", "Techniczne")
#         return

@bot.command(name="priv")
async def private_channel(ctx):
    """Nowy kanał dostępny jedynie dla roli Owner oraz wybranego użytkownika"""
    try:
        logger.debug(f"Looking for user id {ctx.author.id}")
        user = ctx.guild.get_member(int(ctx.author.id))
        logger.info(f"Found user with id {ctx.author.id}: {user}")
        await panda_tools.create_text_channel(ctx.guild, user, f"{ctx.author.name}_priv", config["private_chat_category_name"] )
    except Exception as e:
        logger.warning (e)
        await ctx.send('Wystąpił błąd, prawdopodobnie nie znaleziono takiej osoby')
        await panda_tools.channel_message(ctx.guild, e, "pandabot-log", "Techniczne")
        return

@bot.command(name="roll")
async def roll(ctx, dice: str):
    """Rzut kością, format NkN (np. 2k6 -> 2x 6 ścian)"""
    try:
        rolls, limit = map(int, dice.split('k'))
    except Exception as e:
        await ctx.send('Format rzutu kością musi być NkN!')
        await panda_tools.channel_message(ctx.guild, e, "pandabot-log", "Techniczne")
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

# TODO: Enable again for owner only.
# @bot.command(name="question")
# async def question(ctx):
#     """Nie używać"""
#     try:
#         await panda_roles.generate_questions(ctx.guild, "michald", "Kandydat-devops-core")
#     except Exception as e:
#         await ctx.send(e)
