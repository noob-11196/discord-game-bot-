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

@bot.event
async def on_ready():
    print(f"성공적으로 로그인했습니다: {bot.user.name}")

@bot.command()
async def 안녕(ctx):
    await ctx.send("안녕하세요! 봇이 정상적으로 작동 중입니다.")

# 3. 다나와 최저가 검색 명령어
@bot.command()
async def 다나와(ctx, *, keyword: str = None):
    if not keyword:
        await ctx.send("검색어를 입력해 주세요! 예시: `!다나와 RTX 4060`")
        return

    await ctx.send(f"🔍 **'{keyword}'** 다나와 검색 중...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    
    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://search.danawa.com/dsearch.php?query={encoded_keyword}"

    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        items = soup.select('.product_list > .prod_item')
        results = []

        for item in items:
            if 'prod_ad_item' in item.get('class', []):
                continue

            name_elem = item.select_one('.prod_name a')
            price_elem = item.select_one('.price_sect strong')

            if name_elem and price_elem:
                name = name_elem.text.strip()
                price = price_elem.text.strip() + "원"
                link = name_elem.get('href', url)
                
                if link.startswith('//'):
                    link = 'https:' + link

                results.append((name, price, link))
                if len(results) >= 3:
                    break

        if not results:
            await ctx.send(f"❌ **'{keyword}'**에 대한 검색 결과를 찾을 수 없습니다.")
            return

        embed = discord.Embed(
            title=f"🛒 다나와 검색 결과: {keyword}",
            color=discord.Color.blue(),
            url=url
        )

        for idx, (name, price, link) in enumerate(results, 1):
            embed.add_field(
                name=f"{idx}. {name[:40]}...", 
                value=f"💰 **최저가**: {price}\n🔗 [상품 링크 바로가기]({link})", 
                inline=False
            )

        embed.set_footer(text="Danawa Price Crawler")
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"⚠️ 검색 도중 오류가 발생했습니다: {e}")

# 봇 실행
TOKEN = os.environ.get("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
import os
import sys

# 디스코드 토큰 환경변수 확인
TOKEN = os.environ.get("DISCORD_TOKEN")

if not TOKEN:
    print("❌ [오류] Render Environment에 DISCORD_TOKEN이 설정되지 않았습니다.", flush=True)
    print("👉 Render 대시보드 -> Environment 탭에서 DISCORD_TOKEN을 등록해 주세요.", flush=True)
    sys.exit(1)

print("🔑 토큰 확인 완료. 디스코드 연결을 시도합니다...", flush=True)

try:
    bot.run(TOKEN)
except Exception as e:
    print(f"❌ [실행 오류] 봇을 실행하는 동안 문제가 발생했습니다: {e}", flush=True)
    sys.exit(1)
