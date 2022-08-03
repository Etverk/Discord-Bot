#Imports
from os import startfile
from discord.ext import commands
import discord
import asyncio
import requests
import json
import re
import serverdata

#Message intents
intents = discord.Intents.default()
intents.members = True
#Client
client = discord.Client(intents=intents)

#Main inspiration function
def get_inspiration():
    apiResponse = requests.get("https://zenquotes.io/api/quotes/")
    jsonData = json.loads(apiResponse.text)
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
        name = "&callstaff \{anledning\}",
        value = "Skickar en rapport och pingar staff.",
        inline = True
    )
    return embed

#Client events
#Login confirmation message
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

#Checks all sent messages
@client.event
async def on_message(message):
    
    #Looks for "&inspiration" command and runs corresponding function
    if message.content.startswith("&inspiration"):
        inspiration = get_inspiration()
        await message.channel.send(inspiration)
        
    if message.content.startswith("&hjälpare"):
        await message.channel.send(content=None, embed=get_hjälpare_embed())
        
    #&callstaff {reason}
    if message.content.startswith("&callstaff"):
        channel = client.get_channel(1004381595836358676)
        await channel.send(content=None, embed=report_function(message))
        await channel.send("<@&1004383226862772274>")
 
    #Looks for "&hjälp" command and runs corresponding function
    if message.content == ("&hjälp"):
        await message.channel.send(content=None, embed=get_help())
        print(serverdata.MP["name"])
    
#Imports discord token from "token.0"
with open("token.0", "r", encoding="utf-8") as f:
    lines = f.readlines()
    botToken = lines[0]

#Runs bot 
client.run(botToken)