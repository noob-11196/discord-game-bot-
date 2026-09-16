import os
import threading
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands

# 1. Render 포트 타임아웃 방지용 가짜 웹서버
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()

# 2. 디스코드 봇 기본 설정
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 3. 봇 이벤트 및 명령어 설정
@bot.event
async def on_ready():
    print(f"성공적으로 로그인했습니다: {bot.user}")

# '안녕' 또는 '!안녕' 입력 시 반응
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content in ["안녕", "안녕하세요", "!안녕"]:
        await message.channel.send("안녕하세요! 봇이 정상 작동 중입니다. 🎮")

    await bot.process_commands(message)

# !ping 명령어
@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

# 4. Render 환경변수에서 토큰을 불러와 봇 실행
token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("DISCORD_TOKEN 환경변수가 설정되지 않았습니다.")
