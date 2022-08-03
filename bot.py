#Imports
import discord
import asyncio
import requests
import json

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
    

#Imports discord token from "token.0"
with open("vault.0", "r", encoding="utf-8") as f:
    lines = f.readlines()
    botToken = lines[0]

#Runs bot
client.run(botToken)