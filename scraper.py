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
    author = str(message.author)
    content = str(message.content)
    userid = str(message.author.id) 
    messageid = str(message.id)
    time = str(message.created_at)
    link = str(message.jump_url)
    channel = str(message.channel)
    row = [userid,author,content,time,messageid,link,channel]
    try:
        f = open("history.txt", "a")
        f.write(f"{row}\n")
        f.close()
    except expression as identifier:
        print("Can't write")
    finally:
        pass
    await bot.process_commands(message)

bot.run(token)