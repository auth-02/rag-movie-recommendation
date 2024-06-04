# Connecting the ChatBot to discord -> rag-movie-recomm

import os
import discord
from discord.ext import commands
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# print(TOKEN)

intents = discord.Intents.default()
intents.messages = True 
intents.message_content = True

client = discord.Client(intents=intents)

# Connected to the server log
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
# Bot messaging - Respond (User to Bot, Bot to User)
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]
    
    # print(message.content)

    if message.content == 'rag-movie-recomm':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)

client.run(TOKEN)