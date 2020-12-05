
from panda_init import *
import healthcheck
import bot_commands
import bot_events

logger = init_logging(config, __name__) 

bot.loop.create_task(healthcheck.app.run_task('0.0.0.0', 5000))
bot.run(config["key"])
