import discord
import json
from discord.ext import commands
import os
import random
import ast
import time

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print('MikuBot is ready')

@client.command()
async def ping(ctx):
    await ctx.send("Pong! Current Ping is "+str(round(client.latency*1000))+"ms")

@client.command()
async def load(ctx,extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx,extension):
    client.unload_extension(f'cogs.{extension}')

@client.command(aliases = ['flip','flipcoin'])
async def _flipcoin(ctx):
    responses = [1,2,3,4,5,6]
    if random.choice(responses) % 2 == 0:
        await ctx.send("You got heads")
    else:
        await ctx.send("You got tails")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('NjkzODkzMjI3MzgzODgxODY5.XoDsbQ.H3GNJKAhle8Aqm2I4cbhIj-5Lkg')