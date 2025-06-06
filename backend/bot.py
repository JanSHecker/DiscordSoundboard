from dotenv import load_dotenv
load_dotenv()

import discord
import asyncio
import os

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
GUILD_ID = 1234567890
VC_CHANNEL_ID = 1234567890
UPLOAD_DIR = "sounds"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
vc = None

@client.event
async def on_ready():
    print(f"{client.user} connected!")

def play(filename):
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        return {"error": "File not found"}
    
    async def run():
        global vc
        if not vc:
            guild = discord.utils.get(client.guilds, id=GUILD_ID)
            channel = discord.utils.get(guild.voice_channels, id=VC_CHANNEL_ID)
            vc = await channel.connect()
        if vc.is_playing():
            vc.stop()
        vc.play(discord.FFmpegPCMAudio(path))

    asyncio.run_coroutine_threadsafe(run(), client.loop)
    return {"status": "playing"}

def start():
    client.run(TOKEN)
