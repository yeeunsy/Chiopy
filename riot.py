import discord
from typing import Optional
import requests
from bs4 import BeautifulSoup
from tk import Token
from discord import app_commands
from discord import embeds

client = discord.Client(intents=discord.Intents.default())

baseurl = "https://kr.op.gg/summoner/userName="

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    await client.change_presence(activity=discord.Streaming(name="치오 테스트 중", url='https://www.twitch.tv/yeeunsy'))

@client.event
async def on_message(message):
    if message.content.startswith("?롤"):
        message_content = message.content.replace("?롤 ", "")
        plusurl = message_content.replace(" ", "")
        url = baseurl + plusurl
        res = requests.get(url).text
        soup = BeautifulSoup(res, "html.parser")

        # 티어 이미지 가져오기
        img = soup.find("div", attrs={"class":"SummonerRatingMedium"}).find("img").get('src')

        # 티어, 티어별명 가져오기 (text)
        tiername = soup.find("div", attrs={"class":"TierRank"}).get_text()
        tieraka = soup.find("div", attrs={"class":"LeagueName"}).get_text().strip()

        # LP 가져오기
        userlp = soup.find("span", attrs={"class":"LeaguePoints"}).get_text().strip()

        # 승, 패 , 승률 가져오기
        win = soup.find("span", attrs={"class":"wins"}).get_text().replace("W", "승")
        lose = soup.find("span", attrs={"class":"losses"}).get_text().replace("L", "패")
        odds = soup.find("span", attrs={"class":"winratio"}).get_text()

        # 모스트 챔피언 가져오기
        mostchamp = soup.find_all("div", attrs={"class":"ChampionBox Ranked"}, limit=3)
        mostchamp_list = []
        for most in mostchamp:
            mostchamp_list.append(most.find('div').get('title'))

        embed = discord.Embed(title=message_content + " 님의 플레이어 정보", description="", color=0x62c1cc)
        embed.set_thumbnail(url="http:" + img)

        embed.add_field(name="티어 정보", value="`" + userlp + " | " + tiername + " | " + tieraka + "`", inline=False)
        embed.add_field(name="모스트 챔피언", value="`" + mostchamp_list[0] + ", " + mostchamp_list[1] + ", " + mostchamp_list[2] + "`", inline=False)
        embed.add_field(name="승, 패, 승률", value="`" + win + " " + lose + " | " + odds + "`", inline=False)

        embed.set_footer(text="솔로랭크 기준 티어입니다. | 랭크 정보가 없을 시 출력되지 않습니다.")
        await message.channel.send(embed=embed)
        
client.run(Token)