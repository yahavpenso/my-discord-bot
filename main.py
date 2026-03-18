import discord
from discord.ext import commands
import os
import urllib.request
import json
from flask import Flask
from threading import Thread

# שרת פנימי ל-Render
app = Flask('')
@app.route('/')
def home(): return "I'm alive!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# הגדרות הבוט
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix="!", intents=intents)

SOURCE_ID = 1482253320948023368
WEBHOOK_URL = "https://discord.com/api/webhooks/1483573732860624928/mtr60liIyyRv9Ju6KQ5nj_OODVUntCZZ62AyOmR--8GhHzdVQFAQU28EO9YTcoRmUojd"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.channel.id == SOURCE_ID and not message.author.bot:
        # שליחה ל-Webhook ללא ספריות חיצוניות
        data = {
            "content": message.content,
            "username": message.author.display_name,
            "avatar_url": str(message.author.display_avatar.url)
        }
        
        req = urllib.request.Request(WEBHOOK_URL, data=json.dumps(data).encode('utf-8'))
        req.add_header('Content-Type', 'application/json')
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        try:
            urllib.request.urlopen(req)
            print("Message forwarded!")
        except Exception as e:
            print(f"Error: {e}")

keep_alive()
bot.run(os.environ.get('TOKEN'))
