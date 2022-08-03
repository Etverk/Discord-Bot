import discord
import asyncio


messages = joined = 0
intents = discord.Intents.default()
intents.members = True



client = discord.Client(intents=intents)


with open("token.0", "r", encoding="utf-8") as f:
    lines = f.readlines()
    botToken = lines[0]

client.run(botToken)