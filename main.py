import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# --- קוד לשמירה על הבוט דלוק (Keep Alive) ---
app = Flask('')
@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# -------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

SOURCE_ID = 1482253320948023368  # תחליף ב-ID של הערוץ שממנו מעתיקים
TARGET_ID = 1483573061679845488  # תחליף ב-ID של הערוץ שלך

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.channel.id == SOURCE_ID and not message.author.bot:
        target_channel = bot.get_channel(TARGET_ID)
        if target_channel:
            await target_channel.send(f"**{message.author.name}:** {message.content}")

keep_alive() # מפעיל את השרת ששומר על הבוט
bot.run(os.environ['TOKEN'])
