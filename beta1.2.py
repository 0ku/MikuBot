import discord
import json
from discord.ext import commands
import os
import random
import ast
client = commands.Bot(command_prefix = '!')

#scrimSheet.write("\n")

currentScrims = {
    'MONDAY':[],
    'TUESDAY':[],
    'WEDNESDAY':[],
    'THURSDAY':[],
    'FRIDAY':[],
    'SATURDAY':[],
    'SUNDAY':[]
    }

def deleteScrims():
        open("sixesScrims.txt",'w').close()

def refreshScrims():
    global currentScrims
    scrimSheet = open("sixesScrims.txt",'w')
    deleteScrims()
    textForm = json.dumps(currentScrims)
    scrimSheet.write(textForm)

def initScrims():
    global currentScrims
    scrimSheet = open("sixesScrims.txt",'r')
    contents = scrimSheet.read()
    if os.path.getsize("sixesScrims.txt") > 0:
        currentScrims = ast.literal_eval(contents)
    scrimSheet.close()

def checkOverlap(day,time):
    global currentScrims
    day = day.upper()
    for a in currentScrims[day]:
        currentTime = list(map(str,a.split(" ")))[2]
        print(currentTime)
        if currentTime == time:
            return True
    return False

initScrims()

@client.event
async def on_ready():
    print('Bot is ready')

@client.event
async def on_member_join(member):
    print(member+" has joined the server!")
async def on_member_remove(member):
    print(member+" has left the server")

@client.command()
async def ping(ctx):
    await ctx.send("Pong! Current Ping is "+str(round(client.latency*1000))+"ms")

@client.command(aliases = ['roll','rolldice'])
async def _rolldice(ctx):
    responses = [1,2,3,4,5,6]
    await ctx.send("You rolled a "+ str(random.choice(responses)))

@client.command()
async def addScrim(ctx,day,time,maps,contact,host):
    global currentScrims
    statement = day +" | "+time+" | "+maps+" | "+contact+" | "+host
    if checkOverlap(day,time) == False:
        currentScrims[day.upper()].append(statement)
        await ctx.send("The scrim: "+statement+" was added to the schedule")
        refreshScrims()
    else:
        await ctx.send("There is already a scrim at this time")

@client.command()
async def showSchedule(ctx):
    global currentScrims
    message = "Current scrims are:\n "
    for day in currentScrims.keys():
        message = message+ ("**"+day+"**\n")
        for scrim in currentScrims[day]:
            message = message+ scrim+"\n"
    await ctx.send(message)

@client.command()
async def showScrims(ctx,day):
    global currentScrims
    day = day.upper()
    message = "Scrims for "+day+" are:\n"
    for scrim in currentScrims[day]:
        message+=scrim
        message+="\n"
    await ctx.send(message)

@client.command()
async def removeScrim(ctx,day,time):
    global currentScrims
    day = day.upper()
    for scrim in currentScrims[day]:
        if time in scrim:
            await ctx.send("Removed "+scrim)
            currentScrims[day].remove(scrim)
            refreshScrims()
            return
    await ctx.send("No scrim was found at that time")
    

# @client.command()
# async def commands(ctx):
#     await ctx.send("File was cleared")

@client.command()
async def clearScrims(ctx, certainty):
    global currentScrims
    if certainty == "YESSIR":
        currentScrims = {
        'MONDAY':[],
        'TUESDAY':[],
        'WEDNESDAY':[],
        'THURSDAY':[],
        'FRIDAY':[],
        'SATURDAY':[],
        'SUNDAY':[]
        }
        open("sixesScrims.txt",'w').close()
        await ctx.send("File was cleared")
    else:
        await ctx.send("Confirmation denied")


client.run('NjkzODkzMjI3MzgzODgxODY5.XoDsbQ.H3GNJKAhle8Aqm2I4cbhIj-5Lkg')