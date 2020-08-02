import discord
import json
from time import time, localtime, strftime
from discord.ext import commands, tasks
from datetime import datetime, date
import os
import random
import ast

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

class Scrims(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    def deleteScrims():
            open("sixesScrims.txt",'w').close()

    def refreshScrims():
        global currentScrims
        scrimSheet = open("sixesScrims.txt",'w')
        Scrims.deleteScrims()
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
    @commands.Cog.listener()
    async def on_ready(self):
        self.remindScrims.start()

        print("Reminder was started")

    @tasks.loop(seconds = 10)
    #@commands.command()
    async def remindScrims(self):
        global currentScrims
        x=localtime(time())
        desiredChannel = self.client.get_channel(725821726424039444)
        role = desiredChannel.guild.get_role(733822850846425190)
        weekDay = strftime("%A",x).upper()
        t = localtime()
        currentTime = strftime("%H %M",t)
        hour, minute = map(str,currentTime.split(" "))
        newHour = int(hour)- 12
        newHourWarning1 = newHour +1
        formatTime = str(newHour)+":"+minute
        warnTime1 = str(newHourWarning1)+":"+minute
        for scrim in currentScrims[weekDay]:
            scrimTime = list(map(str,scrim.split(" - ")))[1]
            print(formatTime, scrimTime, warnTime1)
            if formatTime == scrimTime:
                await desiredChannel.send(f"{role.mention} Scrim right now!\n{scrim}")
                currentScrims[weekDay].remove(scrim)
            elif scrimTime == warnTime1:
                await desiredChannel.send(f"{role.mention} Scrim in 1 hour!\n{scrim}")
                currentScrims[weekDay].remove(scrim)

    @commands.command(aliases = ['roll','rolldice'])
    async def _rolldice(self,ctx):
        responses = [1,2,3,4,5,6]
        await ctx.send("You rolled a "+ str(random.choice(responses)))

    @commands.command(aliases = ['add','makeScrim'])
    async def addScrim(self,ctx,day,time,maps,contact,host):
        global currentScrims
        statement = day +" - "+time+" - "+maps+" - "+contact+" - "+host
        if Scrims.checkOverlap(day,time) == False:
            currentScrims[day.upper()].append(statement)
            await ctx.send("The scrim: "+statement+" was added to the schedule")
            Scrims.refreshScrims()
        else:
            await ctx.send("There is already a scrim at this time")

    @commands.command(aliases = ['showAllScrims','showAll'])
    async def showSchedule(self,ctx):
        global currentScrims
        message = "Current scrims are:\n "
        for day in currentScrims.keys():
            message = message+ ("**"+day+"**\n")
            for scrim in currentScrims[day]:
                message = message+ scrim+"\n"
        await ctx.send(message)

    @commands.command(aliases = ['scrims'])
    async def showScrims(self,ctx,day):
        global currentScrims
        day = day.upper()
        message = "Scrims for "+day+" are:\n"
        for scrim in currentScrims[day]:
            message+=scrim
            message+="\n"
        await ctx.send(message)

    @commands.command(aliases = ['remove','delete'])
    async def removeScrim(self,ctx,day,time):
        global currentScrims
        day = day.upper()
        for scrim in currentScrims[day]:
            if time in scrim:
                await ctx.send("Removed "+scrim)
                currentScrims[day].remove(scrim)
                Scrims.refreshScrims()
                return
        await ctx.send("No scrim was found at that time")
        

    # @client.command()
    # async def commands(ctx):
    #     await ctx.send("File was cleared")

    @commands.command()
    async def clearScrims(self,ctx, certainty):
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

def setup(client):
    client.add_cog(Scrims(client))