
import discord
import pyttsx3
import requests
import asyncio
import os
from discord.ext import commands

# BOT AYARLARI
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="?", intents=intents)


# BOT BAŞLATMA
@bot.command()
async def start(ctx):
    await ctx.send(
        "Merhaba! Bot başlatıldı. Komutlar için ?list yazın!"
    )


# HAVA DURUMU
def get_weather(city):
    url = f"https://wttr.in/{city}?format=%C+%t"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return response.text.strip()

        return "Hava durumu bilgisine ulaşılamadı."

    except requests.RequestException:
        return "Hava durumu API'sine bağlanılamadı."


# SESLİ OKUMA
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()


# HAVA DURUMU KOMUTU
@bot.command()
async def weather(ctx, *, city):
    await ctx.send("🌤️ Hava durumu getiriliyor...")

    weather_info = await asyncio.to_thread(
        get_weather, city
    )

    await ctx.send(weather_info)

    await asyncio.to_thread(speak, weather_info)


# RASTGELE BİLGİ API
def get_fact():
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return data.get("text", "Bilgi bulunamadı.")

        return "Bilgi alınamadı, tekrar deneyin."

    except (requests.RequestException, ValueError):
        return "API bağlantısında bir hata oluştu."


# RASTGELE BİLGİ KOMUTU
@bot.command()
async def fact(ctx):
    await ctx.send("🔎 Rastgele bir bilgi aranıyor...")

    fact_info = await asyncio.to_thread(get_fact)

    await ctx.send(
        f"🧠 **İlginç Bilgi:**\n\n{fact_info}"
    )

    # BİLGİYİ SESLİ OKU
    await asyncio.to_thread(speak, fact_info)


# KOMUT LİSTESİ
@bot.command(name="list")
async def list_commands(ctx):
    await ctx.send(
        "**📜 BOT KOMUTLARI**\n\n"
        "`?start` - Botu başlatır.\n"
        "`?weather şehir` - Hava durumunu gösterir ve sesli okur.\n"
        "`?fact` - Rastgele bilgi verir ve sesli okur.\n"
        "`?list` - Komutları listeler."
    )


# BOT HAZIR OLDUĞUNDA
@bot.event
async def on_ready():
    print(f"{bot.user} başarıyla giriş yaptı!")

bot.run("Token")