import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'성공적으로 로그인했습니다: {bot.user}')

@bot.command()
async def 안녕(ctx):
    await ctx.send('반가워요!')

TOKEN = "MTU0OTY2NjU2MTkzMjAwMTM2MQ.Gtmuke.DfGx_80DyMT..."

if __name__ == "__main__":
    bot.run(TOKEN)
