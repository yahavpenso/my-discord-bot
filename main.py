import discord
from discord.ext import commands
import os
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
intents.message_content = True  # חשוב: תדליק את זה ב-Discord Developer Portal!
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ה-IDs שנתת (כמספרים)
SOURCE_ID = 1482253320948023368  # הערוץ ממנו מגיעות ההודעות
TARGET_ID = 1483573061679845488  # הערוץ אליו הבוט שולח

@bot.event
async def on_ready():
    print(f'--- הבוט מחובר! ---')
    print(f'שם הבוט: {bot.user.name}')
    print(f'ID: {bot.user.id}')
    print(f'------------------')

@bot.event
async def on_message(message):
    # 1. בודק אם ההודעה מהערוץ הנכון
    # 2. מוודא שזה לא הבוט עצמו ששלח את ההודעה
    if message.channel.id == SOURCE_ID and message.author.id != bot.user.id:
        target_channel = bot.get_channel(TARGET_ID)
        
        if target_channel:
            # הכנת התוכן: שם השולח + ההודעה שלו
            msg_content = f"**{message.author.display_name}**: {message.content}"
            
            # שליחת ההודעה
            await target_channel.send(msg_content)
            
            # אם יש קבצים/תמונות, נשלח גם אותם
            if message.attachments:
                for attachment in message.attachments:
                    await target_channel.send(attachment.url)
        else:
            print("שגיאה: הבוט לא מצליח למצוא את ערוץ היעד. וודא שהוא נמצא בשרת שלך!")

# --- הפעלה ---
keep_alive()

# הבוט ימשוך את ה-TOKEN מה-Environment Variables ב-Render
token = os.environ.get('TOKEN')
if token:
    bot.run(token)
else:
    print("שגיאה: לא הוגדר TOKEN ב-Render Environment Variables!")
