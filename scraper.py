import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_message(message):
    guild = message.guild
    if guild:
        path = "chatlogs/{}.txt".format(guild.id)  
        with open(path, 'a+') as f:
            print("{0.timestamp} : {0.author.name} : {0.content}".format(message), file=f)
    await bot.process_commands(message)

bot.run(token)