import os
import discord
from discord.ext import commands

# 디스코드 인텐트(권한) 설정
intents = discord.Intents.default()
intents.message_content = True  # 메시지 읽기 권한 활성화

# 봇 명령어 접두사 설정 (예: !안녕)
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"성공적으로 로그인했습니다: {bot.user.name}")

@bot.command()
async def 안녕(ctx):
    await ctx.send("안녕하세요! 봇이 정상적으로 작동 중입니다.")

# Render의 환경변수(DISCORD_TOKEN)에서 토큰을 불러옵니다.
TOKEN = os.environ.get("DISCORD_TOKEN")

if TOKEN:
    bot.run(TOKEN)
else:
    print("오류: DISCORD_TOKEN 환경 변수를 찾을 수 없습니다.")
