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

def get_umbrella():
    
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
        Today_rain = f'今日一日の東京の降水確率は\n' + max(items)+ '%:alert:\n' + '傘絶対忘れないで！！！:umbrella_with_rain_drops:'
    elif 50 <= int(max(items)):
        Today_rain = f'今日一日の東京の降水確率は\n' + max(items) + '%\n' + '傘持っていって！！！:umbrella:'
    elif 30 <= int(max(items)):
        Today_rain = f'今日一日の東京の降水確率は\n' + max(items) + '%\n' + '折り畳み傘があった方がいいかもね！！！:closed_umbrella::handbag:'
    else:
        Today_rain = f'今日一日の東京の降水確率は\n' + max(items) + '%\n' + '俺の日だ！！！！！:sunny::sunglasses:'

    # 雨警報条件分岐 6~24時
    if 70 <= int(rain612):
        Morning_rain = f' 6~12時：' + items[1]
    elif 50 <= int(rain612):
        Morning_rain = f' 6~12時：' + items[1]
    elif 30 <= int(rain612):
        Morning_rain = f' 6~12時：' + items[1]
    else:
        Morning_rain = f' 6~12時：' + items[1]

    if 70 <= int(rain1218):
        Noon_rain = f'12~18時：' + items[2]
    elif 50 <= int(rain1218):
        Noon_rain = f'12~18時：' + items[2]
    elif 30 <= int(rain1218):
        Noon_rain = f'12~18時：' + items[2]
    else:
        Noon_rain = f'12~18時：' + items[2]

    if 70 <= int(rain1824):
        Night_rain = f'18~24時：' + items[3]
    elif 50 <= int(rain1824):
        Night_rain = f'18~24時：' + items[3]
    elif 30 <= int(rain1824):
        Night_rain = f'18~24時：' + items[3] 
    else:
        Night_rain = f'18~24時：' + items[3] 

    message = f"\nおはようございます！！！\n晴男、朝の叫ぶ降水確率配信です！！！\n\n{Today_rain}\n\n朝昼晩に分けての降水確率は、\n{Morning_rain}%\n{Noon_rain}%\n{Night_rain}%\n\n今日も一日頑張りましょう！！！"
    return message
# schedule.every().day.at("12:00").do(job)
  
# while True:
#   schedule.run_pending()
#   time.sleep(10)
