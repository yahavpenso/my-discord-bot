import discord
from discord.ext import commands
import os
import requests
from flask import Flask
from threading import Thread

# --- שרת פנימי לשמירה על הבוט ב-Render ---
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- הגדרות הבוט ---
intents = discord.Intents.default()
intents.message_content = True  # חשוב מאוד! תוודא שזה דלוק ב-Discord Developer Portal
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# הנתונים שלך
SOURCE_ID = 1482253320948023368
WEBHOOK_URL = "https://discord.com/api/webhooks/1483573732860624928/mtr60liIyyRv9Ju6KQ5nj_OODVUntCZZ62AyOmR--8GhHzdVQFAQU28EO9YTcoRmUojd"

@bot.event
async def on_ready():
    print(f'--- הבוט התחבר ומקשיב לערוץ {SOURCE_ID} ---')

@bot.event
async def on_message(message):
    # בודק אם ההודעה מהערוץ הנכון ואם זה לא הבוט עצמו
    if message.channel.id == SOURCE_ID and not message.author.bot:
        
        # הכנת הנתונים למשלוח דרך ה-Webhook
        data = {
            "content": message.content,
            "username": f"{message.author.display_name} (מערוץ מקור)",
            "avatar_url": str(message.author.display_avatar.url)
        }
        
        # שליחה ל-Webhook שלך
        response = requests.post(WEBHOOK_URL, json=data)
        
        if response.status_code == 204:
            print(f"הודעה מ-{message.author.display_name} הועברה בהצלחה.")
        else:
            print(f"שגיאה בהעברת הודעה: {response.status_code}")

# --- הפעלה ---
keep_alive()

# הבוט עדיין צריך את ה-TOKEN כדי "להקשיב" לערוץ המקור
token = os.environ.get('TOKEN')
if token:
    bot.run(token)
else:
    print("שגיאה: לא נמצא TOKEN ב-Environment Variables של Render!")
