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
    embed = str(message.embeds[0].to_dict())
    row = [embed]
    try:
        f = open("history.txt", "a")
        f.write(f"{row}\n")
        f.close()
    except:
        print("Can't write")
    finally:
        pass
    await bot.process_commands(message)

bot.run(token)