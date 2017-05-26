'''
Created on Apr 23, 2017

scp -r * pi@raspberrypi.local:/home/pi/Desktop/Discord/selfbot

@author: zhu.exe
'''

import logging

import discord
from discord.ext import commands

discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')
log.addHandler(handler)

bot = commands.Bot(command_prefix=".")

initial_extensions = [
    'cogs.scheduler'
]


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    if not hasattr(message, "server"): return
    if not message.server.id == "211219033658228739": return #only listen to Discord & Dragons
    await bot.process_commands(message)

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))
    with open('token.txt', mode='r') as f:
        token = f.read()
    bot.run(token) #ragnarok token