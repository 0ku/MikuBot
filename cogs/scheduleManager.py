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
warnedScrims = []
weekDay = ""
class Scrims(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.teamname = "Zipf's Law"
    
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
        global warnedScrims
        global currentScrims
        global weekDay
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
                if scrim in warnedScrims:
                    warnedScrims.remove(scrim)
            elif scrimTime == warnTime1 and scrim not in warnedScrims:
                await desiredChannel.send(f"{role.mention} Scrim in 1 hour!\n{scrim}")
                currentScrims[weekDay].remove(scrim)
                warnedScrims.append(scrim)

    @commands.command(aliases = ['roll','rolldice'])
    async def _rolldice(self,ctx):
        responses = [1,2,3,4,5,6]
        await ctx.send("You rolled a "+ str(random.choice(responses)))

    @commands.command()
    async def todaysScrim(self,ctx):
        global currentScrims
        global weekDay
        print(weekDay)
        scrimList = currentScrims[weekDay]
        if len(scrimList) == 0:
            await ctx.send("There are no scrims today!")
        else:
            message = "**Scrims for today**"
            message+="```\n"
            for scrim in scrimList:
                message+=f"[{scrim}]\n"
            message+="```"
            await ctx.send(message)

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
        check = False
        embed = discord.Embed(
            title = self.teamname,
            description = "Scrims",
            colour = discord.Colour.dark_purple() 
        )
        for day in currentScrims.keys():
            if len(currentScrims[day]) > 0:
                check = True
                message = ""
                for scrim in currentScrims[day]:
                    message = message+ scrim+"\n"
                embed.add_field(name = day,value = message,inline = False)
        if check == False:
            await ctx.send("There are no scrims at the moment")
        else:
            await ctx.send(embed=embed)


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