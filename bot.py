#mattBot by matt#1054

import json
import logging
import random
import sys
import datetime
import asyncio

import discord
from discord.ext import commands

logging.basicConfig(level=logging.WARNING)

def load_db():
    with open('db.json') as f:
        return json.load(f)

db = load_db()

prefix = db['prefix']

bot = commands.Bot(command_prefix=prefix, no_pm=True, pm_help=True)

bot.remove_command('help')

current_datetime = datetime.datetime.now().strftime("%d %b %Y %H:%M")

i_extend = [
    'cogs.basic',
    'cogs.admin',
    'cogs.mod'
]

@bot.event
async def on_ready():
    print("mattBot Alpha v0.4")
    print("-----")
    print("Current Login Info")
    print("Bot Username: " + str(bot.user.name))
    print("Bot User ID: " + str(bot.user.id))
    print("-----")
    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.utcnow()
    while True:
        await bot.change_presence(activity=discord.Game("mattBot Alpha v0.5"))
        await asyncio.sleep(15)
        await bot.change_presence(activity=discord.Game("ya boi"))
        await asyncio.sleep(15)
    #await bot.change_presence(game=discord.Game(name="TESTING MODE"), status=discord.Status.offline)

@bot.event
async def on_resumed():
    print("Resumed...")

@bot.event
async def on_server_join(server):
    print("Joined Server")
    await bot.say(":anger: what up im mattBot woo :anger:")

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(ctx.message.author, 'Sorry, this command can\'t be used in private messages!')
        print("[{}] *ERROR* {} command called by {} in {} - {} with error NoPrivateMessage".format(datetime.datetime.today(), ctx.message.content, ctx.message.author, ctx.message.server.name if ctx.message.channel.is_private == False else "PM", ctx.message.channel.name if ctx.message.channel.is_private == False else "PM"))
    elif isinstance(error, commands.DisabledCommand):
        await bot.send_message(ctx.message.author, 'Sorry, this command is disabled and can\'t be used!')
        print("[{}] *ERROR* {} command called by {} in {} - {} with error DisabledCommand".format(datetime.datetime.today(), ctx.message.content, ctx.message.author, ctx.message.server.name if ctx.message.channel.is_private == False else "PM", ctx.message.channel.name if ctx.message.channel.is_private == False else "PM"))
    elif isinstance(error, commands.CommandInvokeError):
        await bot.send_message(ctx.message.author, str(error))
        print("[{}] *ERROR* {} command called by {} in {} - {} with error {}".format(datetime.datetime.today(), ctx.message.content, ctx.message.author, ctx.message.server.name if ctx.message.channel.is_private == False else "PM", ctx.message.channel.name if ctx.message.channel.is_private == False else "PM", str(error)))
        pass
    elif isinstance(error, commands.CheckFailure):
        await bot.send_message(ctx.message.channel, 'Sorry, you do not have the proper permissions for this command!')
        print("[{}] *ERROR* {} command called by {} in {} - {} with error CheckFailure".format(datetime.datetime.today(), ctx.message.content, ctx.message.author, ctx.message.server.name if ctx.message.channel.is_private == False else "PM", ctx.message.channel.name if ctx.message.channel.is_private == False else "PM"))
    elif isinstance(error, commands.CommandNotFound):
        await bot.send_message(ctx.message.channel, 'Sorry, the command you entered doesn\'t exist!')
        print("[{}] *ERROR* {} command called by {} in {} - {} with error CommandNotFound".format(datetime.datetime.today(), ctx.message.content, ctx.message.author, ctx.message.server.name if ctx.message.channel.is_private == False else "PM", ctx.message.channel.name if ctx.message.channel.is_private == False else "PM"))

if __name__ == '__main__':
    if any('debug' in arg.lower() for arg in sys.argv):
        bot.command_prefix = "^"

    #bot.client_id = db['client_id']
    #bot.bots_key = db['bots_key']

    for extension in i_extend:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}'.format(extension, type(e).__name__))

bot.run(db['token'])