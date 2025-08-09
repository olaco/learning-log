import os
import discord
from discord.ext import commands
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv() 

# Setup Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Setup Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file(os.getenv('GOOGLE_CREDENTIALS'), scopes=scope)
client_gsheets = gspread.authorize(creds)
sheet = client_gsheets.open('BotLogs').sheet1

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if message.author.bot:
        return

    if message.content:
        entry = message.content  # Get the text 
        sheet.append_row([str(message.author), entry, timestamp])
        await bot.process_commands(message)
        await message.channel.send('Logged to Google Sheet ✅')

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
