import os
import discord
import datetime
from datetime import datetime
import asyncio
from discord.ext import commands
from discord.ext.commands import bot
from dotenv import load_dotenv
import json

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

description = 'A seed bot that does nothing'
bot = commands.Bot(command_prefix='?', description=description)

def housing_parser(embed):
    '''
    This method will create a new dictionary with relevant key:value pairs 
    '''
    scrubbed = {}
    try:
        areanum = embed["fields"][1]["value"].find("m")
        rentnum = embed["fields"][2]["value"].find("kr")

        scrubbed["street"] = embed["author"]["name"]
        scrubbed["rooms"] = int(embed["fields"][0]["value"][0])
        scrubbed["area"] = int(embed["fields"][1]["value"][0:areanum])
        scrubbed["rent"] = int(embed["fields"][2]["value"][0:rentnum])
        scrubbed["story"] = int(embed["fields"][3]["value"])
        scrubbed["applicants"] = int(embed["fields"][4]["value"])
        scrubbed["points"] = int(embed["fields"][5]["value"][12:-2])
        scrubbed["built"] = int(embed["fields"][6]["value"])
        scrubbed["renovated"] = int(embed["fields"][7]["value"])
        scrubbed["last_app"] = embed["fields"][8]["value"]
        scrubbed["date_added"] = embed["timestamp"]

        print(scrubbed)
        
    except KeyError:
        print("Key not found")


@bot.event
async def on_ready():
    print(bot.user.name)
    print('---------------')
    print('This bot is ready for action!')

@bot.command(pass_context=True)
async def ping(ctx):
    '''Returns pong when called'''
    author = ctx.message.author.name
    guild = ctx.message.guild.name
    await ctx.channel.send('Pong for {} from {}!'.format(author, guild))

@bot.event
async def on_message(message):
    embed = message.embeds[0].to_dict()
    time = str(message.created_at)
    housing_parser(embed)
    try:
        f = open("history.txt", "a")
        f.write(f"{embed} {time}\n")
        f.close()
    except:
        print("Can't write")
    finally:
        pass
    await bot.process_commands(message)

bot.run(token)