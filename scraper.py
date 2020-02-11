import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

description = 'A seed bot that does nothing'
bot = commands.Bot(command_prefix='?', description=description)

@bot.event
async def on_ready():
    print(bot.user.id)
    print(bot.user.name)
    print('---------------')
    print('This bot is ready for action!')

@bot.command(pass_context=True)
async def ping(ctx):
    '''Returns pong when called'''
    author = ctx.message.author.name
    guild = ctx.message.guild.name
    await bot.say('Pong for {} from {}!'.format(author, guild))

bot.run(token)