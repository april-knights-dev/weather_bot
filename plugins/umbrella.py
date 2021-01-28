# coding: utf-8

from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
import datetime
from slacker import Slacker
from apscheduler.schedulers.blocking import BlockingScheduler

import os
import requests
import urllib.request as req
import slack
from bs4 import BeautifulSoup


def get_umbrella():

    # スクレイピング対象の URL にリクエストを送り HTML を取得する
    res_url = requests.get('http://www.drk7.jp/weather/xml/13.xml')
    print(res_url)

    # レスポンスの HTML から BeautifulSoup オブジェクトを作る
    soup = BeautifulSoup(res_url.content, 'html.parser')  # BeautifulSoupの初期化

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
        Today_rain = f'今日一日の東京の降水確率は\n' + \
            max(items) + '%:alert:\n' + \
            '傘絶対忘れないでください！！！:umbrella_with_rain_drops:'
    elif 50 <= int(max(items)):
        Today_rain = f'今日一日の東京の降水確率は\n' + \
            max(items) + '%\n' + '傘持っていってください！！！:umbrella:'
    elif 30 <= int(max(items)):
        Today_rain = f'今日一日の東京の降水確率は\n' + \
            max(items) + '%\n' + '折り畳み傘があった方がいいかも！！！:closed_umbrella::handbag:'
    else:
        Today_rain = f'今日一日の東京の降水確率は\n' + \
            max(items) + '%\n' + ':sunny::sunglasses:'

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

    # tenki.jpの目的の地域のページのURL（デフォルト江東区）
    weelly_url = 'https://tenki.jp/forecast/3/16/4410/13108/10days.html'

    # HTTPリクエスト
    w_r = requests.get(weelly_url)

    # HTMLの解析
    bsObj = BeautifulSoup(w_r.content, "html.parser")

    # 5日分の天気情報を取得
    all_info = bsObj.find(class_="forecast-point-10days")
    all_weather = all_info.find_all(class_="forecast-telop")

    # 5日分の天気

    # 5日分の天気
    weekly_weather = all_weather[4].string, all_weather[10].string

    # 気温の取得
    all_temp_max = all_info.find_all(class_="high-temp")  # 最高気温
    temp_max = all_temp_max[0].string, all_temp_max[1].string
    all_temp_min = all_info.find_all(class_="low-temp")  # 最低気温
    temp_min = all_temp_min[0].string, all_temp_min[1].string

    message = f"\nおはようございます！！！\n晴男、朝の叫ぶ降水確率配信です！！！\n\n{Today_rain}\n\n朝昼晩に分けての降水確率は、\n{Morning_rain}%\n{Noon_rain}%\n{Night_rain}%\n\n明日の天気は {weekly_weather[0]}\n:thermometer:最高・最低気温は{temp_max[0]} / {temp_min[0]}\n明後日の天気は{weekly_weather[1]}\n:thermometer:最高・最低気温は{temp_max[1]}{temp_min[1]}\n\n今日も一日頑張りましょう！！！"
    return message
# schedule.every().day.at("12:00").do(job)

# while True:
#   schedule.run_pending()
#   time.sleep(10)
