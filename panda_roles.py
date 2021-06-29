import logging
import panda_tools
from panda_init import *
import json
import numpy
import os

logger = init_logging(config, __name__)


async def on_role_update(before, after):
    guild = after.guild
       
    for role_name in config["role_names"]:
        logger.debug(f"Searching for the configured roles in guild roles: {guild.roles}")
        role = [role for role in guild.roles if role.name == role_name][0]
        
        if role in after.roles and role not in before.roles:
            await panda_tools.add_role(after, "Panda")
            channel_name = after.name.lower().replace("#", "")
            logger.debug(f"Checking if channel {channel_name} exists")
            
            if not panda_tools.channel_exists(channel_name, guild, role.name):
                logger.debug(f"Channel {channel_name} doesn't exist. Trying to create channel")
                channel = await panda_tools.create_text_channel(guild=guild, user=after, name=channel_name, category=role.name)
                await welcome_user(guild, channel, role)


async def welcome_user(guild, channel, role):
    with open( f"{config_path}/role_message.json", 'r') as file:
        role_message = json.loads(file.read())
    
    if role_message[role.name]:
        logger.info(f"Sending a welcome message to a new {role.name}")
        await channel.send(role_message[role.name])
    
    if role.name == "Kandydat-devops-core":
        logger.info(f"Generating random question set for Kandydat-devops-core channel.")
        await generate_questions(guild, "Kandydat-devops-core")

async def generate_questions(guild, channel):
        questions_path = f"{config_path}/questions/{channel}.json"
        
        questions = load_questions(questions_path) 
        if not questions:
            questions = prepare_questions()
        logger.debug(f"Questions: {questions}")

        save_questions(questions, questions_path)
        await print_questions(guild, questions, channel)

def prepare_questions():
    logger.debug(f"Preparing random question set")
    with open( f"{config_path}/questions.json", 'r') as file:
        questions = json.loads(file.read())
    
    generated_questions = {}
    for category in questions:
        generated_questions[category] = numpy.random.choice(questions[category], size=3, replace=False).tolist()

    return generated_questions

async def print_questions(guild, questions, channel):
    logger.debug(f"Printing questions: {questions}")
    for category in questions:
        embed=discord.Embed(title="Pytania:", color=0x70ae36)
        embed.set_author(name=f"Kategoria: {category}", icon_url=guild.icon_url)
        embed.set_footer(text="Prosimy o nie udostępnianie pytań innym osobom i przypominamy, że pytania mają na celu jedynie określić poziom kursanta. W Twoim najlepszym interesie jest odpowiadać samodzielnie!")
        for iteration, question in enumerate(questions[category]):
            logger.debug(f"Printing {iteration}, {question}")
            embed.add_field(name=f"{iteration + 1}. {question}", value='\u200b', inline=False)
        logger.debug(f"Printing {embed}")
        await panda_tools.channel_message(guild, embed, channel, embed=True)

def save_questions(questions, questions_path):
    logger.debug(f"Saving questions")
    with open(questions_path, 'w', encoding='utf8') as file:
        json.dump(questions, file, ensure_ascii=False)
    logger.debug(f"New question file created")

def load_questions(questions_path):
    logger.debug(f"Trying to load questions")
    if os.path.exists(questions_path):
        with open( f"{questions_path}", 'r', encoding='utf8') as file:
            questions = json.loads(file.read())
            logger.debug(f"Loading questions")
        return questions
    else:
        logger.debug(f"Questions file doesn't exist")
        return False
   
        