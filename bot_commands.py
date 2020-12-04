import random
import logging
from main import guild, bot, config
from panda_tools import init_logging

logger = panda_tools.init_logging()

@bot.command(name="private_channel")
async def private_channel(ctx, user_id: int):
    """Nowy kanał dostępny jedynie dla roli Owner oraz wybranego użytkownika"""
    try:
        logger.debug(f"Looking for user id {user_id}")
        user = ctx.guild.get_member(user_id)
        logger.info(f"Found user with id {user_id}: {user}")
        await panda_tools.create_text_channel(user=user, name=user, category=channel_category)
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
