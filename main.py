import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands

# Render의 포트 타임아웃 방지용 가짜 웹서버
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# 백그라운드로 웹서버 실행
threading.Thread(target=run_health_server, daemon=True).start()

# --- 디스코드 봇 메인 코드 ---
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"성공적으로 로그인했습니다: {bot.user.name}")

@bot.command()
async def 안녕(ctx):
    await ctx.send("안녕하세요! 봇이 정상적으로 작동 중입니다.")

TOKEN = os.environ.get("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
