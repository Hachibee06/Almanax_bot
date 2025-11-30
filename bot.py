import json
import requests
import discord
from discord.ext import commands
from datetime import datetime
import schedule
import asyncio
import os

TOKEN_BOT = os.getenv("TOKEN_BOT")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# 3. Langue de l'Almanax ("fr" pour français)
lang = "fr"

# Configuration des intents pour le bot Discord
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True  # pour accéder aux salons
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready ! Connecté en tant que {bot.user}")

    # 4. Heure d'envoi du message chaque jour
    #    Format 24h, "HH:MM" (par ex "08:00" pour 8h du matin)
    schedule.every().day.at("13:33").do(send_daily_message)

    # Boucle qui vérifie les tâches planifiées
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

    # Pour tester immédiatement (sans attendre l'heure),
    # tu peux commenter le bloc schedule ci-dessus
    # et décommenter la ligne suivante :
    # send_daily_message()

# Fonction qui récupère l'Almanax du jour et envoie le message
def send_daily_message():

    # Date au format anglais pour l'API et français pour l'affichage
    date_en = datetime.now().strftime("%Y-%m-%d")
    date_fr = datetime.now().strftime("%d/%m/%Y")

    # Requête à l'API pour récupérer l'Almanax du jour
    url = f"https://alm.dofusdu.de/dofus/{lang}/{date_en}"
    response = requests.get(url)
    response_data = response.json()

    # Récupération des infos importantes dans la réponse
    daily_bonus = response_data["data"]["bonus"]["bonus"]
    daily_bonus_description = response_data["data"]["bonus"]["description"]
    item_name = response_data["data"]["item_name"]
    item_quantity = response_data["data"]["item_quantity"]

    # Message envoyé dans le salon Discord
    message = (
        f"🥚 Almanax du {date_fr} 🥚\n\n"
        f"🌍 Bonus du jour : **{daily_bonus}**\n"
        f"📜 Description : {daily_bonus_description}\n"
        f"✅ Offrande : **{item_quantity}× {item_name}**\n"
    )

    # On récupère le salon par son ID (plus fiable que le nom)
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        bot.loop.create_task(channel.send(message))
        print("Message envoyé dans le salon Discord.")
    else:
        print(f"Salon avec l'ID {CHANNEL_ID} introuvable.")

# Lancement du bot
bot.run(TOKEN_BOT)
