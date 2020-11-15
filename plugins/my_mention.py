# coding: utf-8

from slack import WebClient
from slackbot.bot import respond_to  # @botname: で反応するデコーダ
from slackbot.bot import listen_to  # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
from datetime import datetime
from bs4 import BeautifulSoup
import datetime as dt
import locale
import calendar

import os
import requests
import urllib.request as req
import sys
import json
import pprint
import re
import datetime

client = WebClient(token=os.getenv("API_TOKEN"))

API_KEY = "e2b220b4263af8d026cb5e44abd8f568"  # xxxに自分のAPI_Keyを入力。


@listen_to("(.*)")
def reply_weather(content, msg):

    if re.search("^天気|^傘", msg) is None:
        return

    prefecture_set = {
        "東京": ("35.6181022", "139.7730337", "13"),
        "千葉": ("35.60472", "140.12333", "08"),
        "埼玉": ("35.85694", "139.64889", "12"),
        "茨城": ("36.34139", "140.44667", "09"),
        "群馬": ("36.39111", "139.06083", "11"),
        "山梨": ("35.66389", "138.56833", "19"),
        "神奈川": ("35.44778", "139.6425", "14"),
        "栃木": ("36.56583", "139.88361", "10")
    }

    city = msg.split()
    print(city)
    if len(city) == 1:
        city = "東京"
    elif len(city) == 2:
        city = city[1]

    print(city)
    for key in prefecture_set.keys():
        if city == key:
            TENKI_URL = f"https://api.openweathermap.org/data/2.5/onecall?lat={prefecture_set[city][0]}&lon={prefecture_set[city][1]}&units=metric&exclude=hourly,minutely,alerts&lang=ja&appid={API_KEY}"
            KASA_URL = f"http://www.drk7.jp/weather/xml/{prefecture_set[city][2]}.xml"
            break
    else:
        content.reply("僕を呼ぶ時は[天気スペース首都圏]って入力してね！！！\n※都や県はいらないよッッ！！")
        return "success"

    if "傘" in msg:

        kasa_response = requests.get(KASA_URL)

        # レスポンスの HTML から BeautifulSoup オブジェクトを作る
        soup = BeautifulSoup(kasa_response.content, "html.parser")

        # # 降水確率リスト表記
        items = list(soup.find("rainfallchance").stripped_strings)

        # 一日の降水確率最大
        if 70 <= int(max(items)):
            today_rain = (
                f"今日一日の{city}の降水確率は\n*{max(items)}%*\n:alert::alert:傘絶対忘れないでください！！！:umbrella_with_rain_drops::alert::alert:"
            )
        elif 40 <= int(max(items)):
            today_rain = (
                f"今日一日の{city}の降水確率は\n*{max(items)}%*\n傘持っていってください！！！:umbrella:"
            )
        elif 20 <= int(max(items)):
            today_rain = (
                f"今日一日の{city}の降水確率は\n*{max(items)}%*\n折り畳み傘があった方がいいかも！！！:closed_umbrella::handbag:"
            )
        else:
            today_rain = f"今日一日の{city}の降水確率は\n*{max(items)}%*\n:sunny::sunglasses:"

        morning_rain = "6~12時：" + items[1]
        noon_rain = "12~18時：" + items[2]
        night_rain = "18~24時：" + items[3]

        if "傘" in msg:
            negirai = "\n*お疲れ様です！！！晴男です！！！*"
            syousai = f"\n\n{today_rain}\n\n朝昼晩に分けての降水確率は、\n{morning_rain}%\n{noon_rain}%\n{night_rain}%"

            client.chat_postMessage(
                channel=content.body["channel"],
                blocks=message_format(negirai, syousai),
                username=u'晴男の叫ぶ天気bot',
                icon_url="https://i.gyazo.com/601b4894e87c196c1296d1d0e2f92c51.png"
            )
    elif "天気" in msg:
        tenki_response = requests.get(TENKI_URL).json()
        print(TENKI_URL, tenki_response)

        # mainから取得
        daily = tenki_response.get("daily")
        res_temp = tenki_response.get("current").get("temp")
        res_mark = tenki_response.get("current").get("weather")[0].get("main")

        daily_weather = [daily[0].get("weather")[0].get("main"),
                         daily[1].get("weather")[0].get("main"),
                         daily[2].get("weather")[0].get("main"),
                         daily[3].get("weather")[0].get("main"),
                         daily[4].get("weather")[0].get("main"),
                         daily[5].get("weather")[0].get("main"),
                         daily[6].get("weather")[0].get("main")]

        locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

        # 一週間分の日付と曜日を取得
        dt0 = dt.date.today()
        dt1 = dt0 + dt.timedelta(days=1)
        dt2 = dt0 + dt.timedelta(days=2)
        dt3 = dt0 + dt.timedelta(days=3)
        dt4 = dt0 + dt.timedelta(days=4)
        dt5 = dt0 + dt.timedelta(days=5)
        dt6 = dt0 + dt.timedelta(days=6)

        d0 = calendar.day_name[dt0.weekday()]
        d1 = calendar.day_name[dt1.weekday()]
        d2 = calendar.day_name[dt2.weekday()]
        d3 = calendar.day_name[dt3.weekday()]
        d4 = calendar.day_name[dt4.weekday()]
        d5 = calendar.day_name[dt5.weekday()]
        d6 = calendar.day_name[dt6.weekday()]

        weather_stmp = {
            "Rain": ":umbrella_with_rain_drops:",
            "clear sky": ":sunny:",
            "Clear": ":mostly_sunny:",
            "Thunderstorm": ":lightning_cloud:",
            "Drizzle": ":rain_cloud:",
            "Snow": ":snowman:",
            "Mist": ":new_moon_with_face:",
            "Smoke": ":yosi:",
            "Haze": ":hotsprings:",
            "Dust": ":mask:",
            "Fog": ":dash:",
            "Sand": ":camel:",
            "Ash": ":volcano:",
            "Squall": ":ocean:",
            "Tornado": ":cycrone:",
            "Clouds": ":partly_sunny:",
        }

        # 一週間分の天気をスタンプに置換
        if weather_stmp.get(daily_weather[0]):
            dw = weather_stmp.get(daily_weather[0])
        else:
            dw = ":question:"
        if weather_stmp.get(daily_weather[1]):
            dw1 = weather_stmp.get(daily_weather[1])
        else:
            dw1 = ":question:"
        if weather_stmp.get(daily_weather[2]):
            dw2 = weather_stmp.get(daily_weather[2])
        else:
            dw2 = ":question:"
        if weather_stmp.get(daily_weather[3]):
            dw3 = weather_stmp.get(daily_weather[3])
        else:
            dw3 = ":question:"
        if weather_stmp.get(daily_weather[4]):
            dw4 = weather_stmp.get(daily_weather[4])
        else:
            dw4 = ":question:"
        if weather_stmp.get(daily_weather[5]):
            dw5 = weather_stmp.get(daily_weather[5])
        else:
            dw5 = ":question:"
        if weather_stmp.get(daily_weather[6]):
            dw6 = weather_stmp.get(daily_weather[6])
        else:
            dw6 = ":question:"

        # 呼び出しの年月日を取得
        date_time = str(datetime.date.today())

        # 英語をそれぞれ日本語にしてくれる辞書
        main_weather = {
            "Rain": "雨が降ってますね・・・:umbrella:",
            "clear sky": "晴れてますよ！！良いぞ:sunny::sunny:",
            "Thunderstorm": "雷と雨が襲来します:pika::pika:",
            "Drizzle": "霧雨、防水にお気をつけ下さい:shower:",
            "Snow": "・・・？！雪が降っている？！:snowflake:",
            "Mist": "かすんでます:new_moon_with_face:",
            "Smoke": "けむいですご注意ください:yosi:",
            "Haze": "もやもや気味です:hotsprings:",
            "Dust": "ほこりっぽいです:mask:",
            "Fog": "きりだぁああああ前方注意:dash:",
            "Sand": "砂ぼこりが舞ってます！！僕も舞います:camel::踊る男性:",
            "Ash": "火山灰が降ってます！！お逃げの準備を:volcano:",
            "Squall": "嵐のコンサートですよ:ocean:",
            "Tornado": "竜巻が来日してます:cycrone:",
            "Clouds": "曇ってます:cloud:だけど僕の心は晴れてます:sunglasses:",
        }

        if main_weather.get(res_mark):
            res_mark = main_weather.get(res_mark)
        else:
            res_mark = f"設定辞書に{res_mark}が含まれてないみたいだよ"

        if "天気" in msg:
            aisatu = "\n*こんにちは！！晴男です！！！*"

            nakami = f"\n\n{date_time}\n現在の{city}は{res_mark}！！！\n気温は{res_temp}度です！！！\n\n{d0[0]}{dw}\n{d1[0]}{dw1}\n{d2[0]}{dw2}\n{d3[0]}{dw3}\n{d4[0]}{dw4}\n{d5[0]}{dw5}\n{d6[0]}{dw6}"

            client.chat_postMessage(
                channel=content.body["channel"],
                blocks=message_format(aisatu, nakami),
                username=u'晴男の叫ぶ天気bot',
                icon_url="https://files.slack.com/files-tmb/T9R9L3GJ1-F01BUNB6J10-a43aa31fc5/____________________________360.jpg"
            )


def message_format(aisatu, message):
    blockkit = [
        {"type": "section", "text": {"type": "mrkdwn", "text": aisatu}},
        {"type": "section", "text": {"type": "mrkdwn", "text": message}},
    ]
    return blockkit


# 辞書型の中身の取り出し方
# dict["key_name"] or dict.get("key_name")

# try  key_nameをcloudsとして上のやり方で取ってみよう
# try main

# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？

# message.reply('string')   @発言者名: string でメッセージを送信
# message.send('string')    string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                               文字列中に':'はいらない

# .*でどんなメッセージでも受け付ける状態
# respond_toで指定してもいいし、中でif message=xxx と分岐してもいい

# def listen_func(message):
#     message.send('誰かがリッスンと投稿したようだ')      # ただの投稿
#     message.reply('君だね？')
