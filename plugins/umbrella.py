# coding: utf-8

from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
from datetime import datetime
from slacker import Slacker
from apscheduler.schedulers.blocking import BlockingScheduler

import os
import requests
import urllib.request as req
import datetime
import slack
from bs4 import BeautifulSoup

def job_u(message):
    
    # スクレイピング対象の URL にリクエストを送り HTML を取得する
    res_url = requests.get('http://www.drk7.jp/weather/xml/13.xml')
    print(res_url)

    # レスポンスの HTML から BeautifulSoup オブジェクトを作る
    soup = BeautifulSoup(res_url.content, 'html.parser')# BeautifulSoupの初期化

    print(soup.prettify()) 

    # 降水確率リスト表記
    items = list(soup.find("rainfallchance").stripped_strings)

    # 6時間毎の降水確率
    # rain06 = int(items[0])
    rain612 = int(items[1])
    rain1218 = int(items[2])
    rain1824 = int(items[3])



    # 一日の降水確率最大
    if 70 <= int(max(items)):
        Today_rain = f'今日一日の東京の降水確率は\n' + max(items)+ '%\nだから' + '傘絶対忘れないで！！！:umbrella_with_rain_drops:'
    elif 40 <= int(max(items)):
        Today_rain = f'今日一日の東京の降水確率は\n' + max(items) + '%\nだから' + '傘持っていって！風邪ひくよ！！！'
    elif 20 <= int(max(items)):
        Today_rain = f'今日一日の東京の降水確率は\n' + max(items) + '%\nだから' + '折り畳み傘あった方がいいかも！！！'
    else:
        Today_rain = f'今日一日の東京の降水確率は\n' + max(items) + '%\nだから' + '傘いらないよ！！！'

    # 雨警報条件分岐 6~24時
    if 70 <= int(rain612):
        Morning_rain = f' 6~12時：' + items[1] + '%' + '\n傘をもって' + 'ちょっと早めに家でた方が良いかも！！！'
    elif 40 <= int(rain612):
        Morning_rain = f' 6~12時：' + items[1] + '%'
    elif 20 <= int(rain612):
        Morning_rain = f' 6~12時：' + items[1] + '%'
    else:
        Morning_rain = f' 6~12時：' + items[1] + '%'

    if 70 <= int(rain1218):
        Noon_rain = f'12~18時：' + items[2] + '%'
    elif 40 <= int(rain1218):
        Noon_rain = f'12~18時：' + items[2] + '%'
    elif 20 <= int(rain1218):
        Noon_rain = f'12~18時：' + items[2] + '%'
    else:
        Noon_rain = f'12~18時：' + items[2] + '%'

    if 70 <= int(rain1824):
        Night_rain = f'18~24時：' + items[3] + '%'
    elif 40 <= int(rain1824):
        Night_rain = f'18~24時：' + items[3] + '%'
    elif 20 <= int(rain1824):
        Night_rain = f'18~24時：' + items[3] + '%' + '\n雨降っててもわんちゃん気合いで帰れるよ！！！'
    else:
        Night_rain = f'18~24時：' + items[3] + '%' + '\n晴男が仕事してる！！！'

    message =('G018FNK81CZ',f"\nおはようございます！！！\n{Today_rain}\n朝昼晩に分けての降水確率は、\n{Morning_rain}\n{Noon_rain}\n{Night_rain}\n\n今日も一日頑張りましょう！！！")
    return job_u
# schedule.every().day.at("12:00").do(job)
  
# while True:
#   schedule.run_pending()
#   time.sleep(10)
