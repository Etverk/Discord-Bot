#Imports
from os import startfile
from discord.ext import commands
import discord
import asyncio
import requests
import json
import re
import serverdata

#Config
moderatorRole = "<@&1004383226862772274>"
commandsChannel = 1004381595836358676

#Bot intiation
bot = commands.Bot(command_prefix="&", intents = discord.Intents.default())

#Main inspiration function
def get_inspiration():
    apiResponse = requests.get("https://zenquotes.io/api/quotes/")
    jsonData = json.loads(apiResponse.text)
    if jsonData[0]["q"].startswith("Too many requests."):
        return "För många förfrågningar. Vänligen vänta."
    else:
        return jsonData[0]["q"] + "  - **" + jsonData[0]["a"] + "**"
    
#Returns embed containing the server's helpers.
def get_hjälpare_embed():
    embed = discord.Embed(
        title = "Våra hjälpare",
        description = "\u200b",
        color = 0xFFFFFF
    )
    
    embed.add_field(
        name = "PROFESSORER",
        value = "Denna roll ges till medlemmar som ger högt kvalitativa och ingående svar som hjälp.",
        inline = False
    )
    
    for i in serverdata.professorList:
        embed.add_field(
            name = i["name"],
            value = "• " + i["skill1"] + "\n • " + i["skill2"],
            inline = True
        )
    
    embed.add_field(
        name = "\u200b",
        value = "\u200b",
        inline = False
    )
    
    embed.add_field(
        name = "LÄRARE",
        value = "Denna roll ges till medlemmar som är extra duktiga på att ge hjälp åt andra på servern.",
        inline = False
    )
    
    for i in serverdata.lärareLista:
        embed.add_field(
            name = i["name"],
            value = "• " + i["skill1"] + "\n • " + i["skill2"],
            inline = True
        )
    
    embed.add_field(
        name = "\u200b",
        value = "\u200b",
        inline = True
    )
    
    return embed

#Returns embed containing report.
def report_function(message):
    reportReason = message.content.split(" ", 1)
    
    embed = discord.Embed(
        title = "STAFF FÖRFRÅGAN",
        description = f"Det har skett en förfrågan om staff i #{message.channel} " + "\.",
        color = 0xFFFFFF
    )
    
    embed.add_field(
        name = message.author,
        value = "Anledning: " + str(reportReason[1]),
        inline = False
    )
    
    return embed

#Returns embed containing help.
def get_help():
    embed = discord.Embed(
        title = "Hjälp",
        description = f"Följande kommandos kan du använda med denna botten.",
        color = 0xFFFFFF
    )
    
    embed.add_field(
        name = "&hjälp",
        value = "Visar alla kommandos denna bot stöder.",
        inline = True
    )
    
    embed.add_field(
        name = "&hjälpare",
        value = "Visar alla hjälpare och deras inriktningar.",
        inline = True
    )
    
    embed.add_field(
        name = "&inspiration",
        value = "Ger dig lite inspiration!",
        inline = True
    )
    
    embed.add_field(
        name = "&callstaff \{anledning\}",
        value = "Skickar en rapport och pingar staff.",
        inline = True
    )
    return embed

#Login confirmation message
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        minutesLeft = int(error.retry_after / 60)
        msg = f"**Vänligen vänta**, försök igen om {minutesLeft} minuter!"
        await ctx.send(msg)
        
@bot.command()
async def inspiration(ctx):
    await ctx.send(get_inspiration())

@bot.command()
async def hjälpare(ctx):
    await ctx.send(content=None, embed=get_hjälpare_embed())

@bot.command()
@commands.cooldown(1,1800,commands.BucketType.user)
async def callstaff(ctx):
    channel = bot.get_channel(commandsChannel)
    await channel.send(content=None, embed=report_function(ctx.message))
    await channel.send(moderatorRole)
    await ctx.send("Din staff-förfrågan har skickats!")
    
@bot.command()
async def hjälp(ctx):
    await ctx.send(content=None, embed=get_help())

#Imports discord token from "token.0"
with open("token.0", "r", encoding="utf-8") as f:
    lines = f.readlines()
    botToken = lines[0]

#Runs bot 
#bot.run(botToken)
bot.run(botToken)