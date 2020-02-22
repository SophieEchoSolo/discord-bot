import os
import discord
import datetime
import asyncio
from discord.ext import commands
from discord.ext.commands import bot
from dotenv import load_dotenv
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
							 user='root',
							 password='',
							 db='housing',
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)

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
    Inserts data into MySQL DB 
    '''
    await bot.process_commands(message)

    author = message.author.id 
    if author != 449752516469456906 & len(message.embeds)<1:
        return

    embed = message.embeds[0].to_dict()
    results = housing_parser(embed)
    try:
        with connection.cursor() as cursor:
            sql = """INSERT INTO houses (street, region, rooms, area, rent, story, applicants, points, built, renovated, last_app) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            val = (results["street"], results["region"], results["rooms"], results["area"], results["rent"], results["story"], results["applicants"], results["points"], results["built"], results["renovated"], results["last_app"])
            cursor.execute(sql, val)
            connection.commit()
            cursor.close()

    except Exception as e:
        print("Unable to write to database")
        print(e)
    finally:
        pass


if __name__ == '__main__':
    try:
        bot.run(token)
    except Exception as e:
        print('Could Not Start Bot')
        print(e)
    finally:
        print('Closing Session')
        connection.close()