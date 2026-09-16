import os
import threading
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands

# 1. Render 포트 타임아웃 방지용 웹서버
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

@bot.event
async def on_ready():
    print(f"성공적으로 로그인했습니다: {bot.user}")

# '안녕' 반응
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content in ["안녕", "안녕하세요"]:
        await message.channel.send("안녕하세요! 다나와 시세 검색 봇입니다. 🎮 (`!시세 [상품명]`으로 검색해보세요)")

    await bot.process_commands(message)

# 3. 다나와 최저가 시세 검색 명령어 (!시세 상품명)
@bot.command()
async def 시세(ctx, *, keyword: str):
    await ctx.send(f"🔍 **{keyword}** 다나와 시세를 검색 중입니다...")
    
    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://search.danawa.com/dsearch.php?query={encoded_keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 검색 결과 첫 번째 상품 추출
        product = soup.select_one("ul.product_list > li.prod_item")
        
        if not product:
            await ctx.send("❌ 검색 결과를 찾을 수 없습니다.")
            return

        name_elem = product.select_one("p.prod_name a")
        price_elem = product.select_one("p.price_sect a strong")

        if name_elem and price_elem:
            name = name_elem.text.strip()
            price = price_elem.text.strip()
            link = name_elem.get("href", "")
            
            reply = f"📦 **{name}**\n💵 **최저가:** {price}원\n🔗 [다나와 링크]({link})"
            await ctx.send(reply)
        else:
            await ctx.send("❌ 상품 정보를 가져오지 못했습니다.")

    except Exception as e:
        await ctx.send(f"⚠️ 검색 중 오류가 발생했습니다: {e}")

# 4. 봇 실행
token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("DISCORD_TOKEN 환경변수가 설정되지 않았습니다.")
