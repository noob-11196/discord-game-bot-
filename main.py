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

# 아래 큰따옴표("") 안에 복사한 봇 토큰을 넣으세요.
TOKEN = "MTU0OTY2NjU2MTkzMjAwMTM2MQ.GQlLoG.CzJfAEC4Q4xFDfnycoTuFxnNP9exV7moav-zzE"

if __name__ == "__main__":
    bot.run(TOKEN)
