import discord
from discord.ext import commands
import requests

# Configura el bot
DISCORD_TOKEN = 'TU_TOKEN_DISCORD'
STEAM_API_KEY = 'TU_API_KEY_STEAM'

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.command()
async def logro(ctx, steam_id: str, app_id: str):
    """Comando para mostrar logros de un usuario en un juego específico."""
    url = f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
    params = {
        'key': STEAM_API_KEY,
        'steamid': steam_id,
        'appid': app_id
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "playerstats" in data and "achievements" in data["playerstats"]:
            unlocked_achievements = [
                ach for ach in data["playerstats"]["achievements"] if ach["achieved"] == 1
            ]
            if unlocked_achievements:
                latest_achievement = unlocked_achievements[-1]
                name = latest_achievement["apiname"]
                description = latest_achievement.get("description", "Sin descripción")
                await ctx.send(f"📜 Logro desbloqueado: **{name}**\n✍️ Descripción: {description}")
            else:
                await ctx.send("El jugador no ha desbloqueado logros recientemente.")
        else:
            await ctx.send("No se encontraron logros para este juego.")
    else:
        await ctx.send("Error al obtener datos de la API de Steam.")

# Inicia el bot
bot.run(DISCORD_TOKEN)
