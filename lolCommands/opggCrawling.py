#op.gg 크롤링 후 정보 가져오기

import requests
from bs4 import BeautifulSoup

def get_UserInfo(soup): #유저 정보 가져오는 코드 (Try Except)
    try:
        #유저 정보 (이름 , 소환사 아이콘)
        user_name = soup.select_one('body > div.l-wrap.l-wrap--summoner > div.l-container > div > div > div.Header > div.Profile > div.Information > span').text
        user_profile = soup.select_one('body > div.l-wrap.l-wrap--summoner > div.l-container > div > div > div.Header > div.Face > div > img')
        user_profile = 'https:'+ str(user_profile['src'])
        USER_INFO = [user_name,user_profile]
        try:
            #솔랭 정보 (티어 사진, 티어, 점수, 승,패,승률)
            solo_img = soup.select_one('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div.SummonerRatingMedium > div.Medal > img')
            solo_img = 'https:' + str(solo_img['src'])
            solo_tear = soup.select_one('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div > div.TierRankInfo > div.TierRank').text
            solo_point = soup.select_one('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div > div.TierRankInfo > div.TierInfo > span.LeaguePoints').text
            solo_point = solo_point.replace('\n','')
            solo_point = solo_point.replace('\t','')
            solo_win = soup.select_one('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div > div.TierRankInfo > div.TierInfo > span.WinLose > span.wins').text
            solo_lose = soup.select_one('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div > div.TierRankInfo > div.TierInfo > span.WinLose > span.losses').text
            solo_winratio = soup.select_one('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div > div.TierRankInfo > div.TierInfo > span.WinLose > span.winratio').text
            SOLO_INFO = [solo_img,solo_tear,solo_point,solo_win,solo_lose,solo_winratio]
        except:
            SOLO_INFO='NONE'

        try:
            #자랭 정보 (티어 사진, 티어, 점수 승패, 승률)
            sub_img = soup.select_one('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.sub-tier > img')
            sub_img = 'https:'+str(sub_img['src'])
            sub_tear = soup.select_one('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.sub-tier > div > div.sub-tier__rank-tier').text
            sub_tear = sub_tear.replace('\n','')
            sub_tear = sub_tear[18:-14]
            sub_point = soup.select_one('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.sub-tier > div > div.sub-tier__league-point').text
            sub_winratio = soup.select_one('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.sub-tier > div > div.sub-tier__gray-text').text
            sub_winratio = sub_winratio.replace('\n','')
            sub_winratio = sub_winratio[10:-8]
            SUB_INFO = [sub_img,sub_tear,sub_point,sub_winratio]
        except:
            SUB_INFO='NONE'

        TOTAL_INFO = [USER_INFO,SOLO_INFO,SUB_INFO]

        return TOTAL_INFO
    except:
        return "존재하지 않는 사용자입니다."

def do_crawl(username):
    URL = "https://www.op.gg/summoner/userName="
    finalName = username.replace(" ","")
    NEW_URL = URL + finalName

    response = requests.get(NEW_URL,headers={'User-Agent': 'Mozilla/5.0'})
    if response.status_code == 200: #접속 성공 시
        html = response.text
        soup = BeautifulSoup(html,'html.parser')
        TOTAL_INFO = get_UserInfo(soup)

        return TOTAL_INFO
    else: #접속 실패 시
        print(response.status_code)