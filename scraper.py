import os
import discord
import datetime
import asyncio
from discord.ext import commands
from discord.ext.commands import bot
from dotenv import load_dotenv
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Houses

engine = create_engine('sqlite:///houses-bot.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

description = 'A seed bot that does nothing'
bot = commands.Bot(command_prefix='?', description=description)

# If table doesn't exist, Create the database
if not engine.dialect.has_table(engine, 'places'):
    Base.metadata.create_all(engine)

def housing_parser(embed):
    '''
    This method will create a new dictionary with relevant key:value pairs 
    '''
    scrubbed = {}
    try:
        area_end = embed["fields"][1]["value"].find("m")
        rent_end = embed["fields"][2]["value"].find("kr")
        region_start = embed["author"]["name"].find("(")
        region_end = embed["author"]["name"].find(")")

        scrubbed["street"] = embed["author"]["name"][0:region_start-1]
        scrubbed["region"] = embed["author"]["name"][region_start+1:region_end]
        scrubbed["rooms"] = int(embed["fields"][0]["value"][0])
        scrubbed["area"] = int(embed["fields"][1]["value"][0:area_end])
        scrubbed["rent"] = int(embed["fields"][2]["value"][0:rent_end])
        scrubbed["story"] = int(embed["fields"][3]["value"])
        scrubbed["applicants"] = int(embed["fields"][4]["value"])
        scrubbed["points"] = int(embed["fields"][5]["value"][12:-2])
        scrubbed["built"] = int(embed["fields"][6]["value"])
        scrubbed["renovated"] = int(embed["fields"][7]["value"])
        scrubbed["last_app"] = embed["fields"][8]["value"]
        scrubbed["date_added"] = embed["timestamp"]
        return scrubbed      

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
    '''
    Appends message context to a text file
    '''
    embed = message.embeds[0].to_dict()
    time = str(message.created_at)
    results = housing_parser(embed)
    try:
        f = open("history.txt", "a")
        f.write(f"{embed} {time}\n")
        f.close()

        placeholders = ', '.join(['%s'] * len(results))
        columns = ', '.join(results.keys())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" %('houses', columns, placeholders)
        engine.execute(sql, results.values())

    except:
        print("Can't write")
    finally:
        pass
    await bot.process_commands(message)

if __name__ == '__main__':
    try:
        bot.run(token)
    except Exception as e:
        print('Could Not Start Bot')
        print(e)
    finally:
        print('Closing Session')
        session.close()