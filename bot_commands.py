import logging
import panda_tools
from panda_init import *
import random

logger = init_logging(config, __name__) 

@bot.command(name="private_channel")
async def private_channel(ctx, user_id: int, channel_category):
    """Nowy kanał dostępny jedynie dla roli Owner oraz wybranego użytkownika"""
    try:
        logger.debug(f"Looking for user id {user_id}")
        user = ctx.guild.get_member(user_id)
        logger.info(f"Found user with id {user_id}: {user}")
        await panda_tools.create_text_channel(user=user, name=user, category=channel_category, guild=ctx.guild)
    except Exception as e:
        logger.info (e)
        await ctx.send('Wystąpił błąd, prawdopodobnie nie znaleziono takiej osoby')
        return

@bot.command(name="roll")
async def roll(ctx, dice: str):
    """Rzut kością, format NkN (np. 2k6 -> 2x 6 ścian)"""
    try:
        rolls, limit = map(int, dice.split('k'))
    except Exception:
        await ctx.send('Format rzutu kością musi być NkN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)
