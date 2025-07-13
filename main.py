import discord, speedtest as spd, asyncio
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

# load the discord token from the env file in order not to leak it - security best practice
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Set up a file to write logs to with the handler
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Set up the things we want the bot to be able to do
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!mn ', intents=intents)

@bot.event
async def on_ready():
    print(f"Engines ready for {bot.user.name}!")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

# Read messages in chat and react
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "69" in message.content.lower():
        await message.channel.send(f"{message.author.mention} nice")

    await bot.process_commands(message)

# Command to respond to hello
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}")

def _speed_test_sync():
    st = spd.Speedtest()
    st.get_best_server()
    return {
        "download": st.download() / 1_000_000,
        "upload":   st.upload()  / 1_000_000,
        "ping":     st.results.ping
    }

@bot.command()
async def speedtest(ctx):
    await ctx.send("Running speedtest... ~10 s ⏳")

    # Make a thread to not block bot from reading events
    results = await asyncio.to_thread(_speed_test_sync)

    msg = (
        f"**Mateo’s speed**\n"
        "```"
        f"Download : {results['download']:.2f} Mbps\n"
        f"Upload   : {results['upload']:.2f} Mbps\n"
        f"Ping     : {results['ping']:.1f} ms"
        "```"
    )

    await ctx.send(msg)



bot.run(token, log_handler=handler, log_level=logging.DEBUG)
