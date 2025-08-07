import os
import discord
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials

import json
from dotenv import load_dotenv

load_dotenv() 

# Setup Discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Setup Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file(os.getenv('GOOGLE_CREDENTIALS'), scopes=scope)
client_gsheets = gspread.authorize(creds)
sheet = client_gsheets.open('BotLogs').sheet1

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if message.author == client.user:
        return

    if message.content.startswith('log '):
        entry = message.content[4:]  # Get the text after 'log '
        sheet.append_row([str(message.author), entry, timestamp])
        await message.channel.send('Logged to Google Sheet ✅')

client.run(os.getenv("DISCORD_BOT_TOKEN"))
