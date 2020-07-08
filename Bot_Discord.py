import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = "=", description="ScredAIO")

@bot.event
async def on_ready():
    print("Ready !")

@bot.command()
async def coucou(ctx):
    await ctx.send("Coucou !")



bot.run("Kp-KAs4VjwXIN9HA5GNj89XdyTyN6C0J")
#Lien d'invitation : https://discord.com/api/oauth2/authorize?client_id=730372868960944128&permissions=0&scope=bot