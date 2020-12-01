# coding: utf-8

from slack import WebClient
from slackbot.bot import respond_to  # @botname: で反応するデコーダ
from slackbot.bot import listen_to  # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
from datetime import datetime
from bs4 import BeautifulSoup

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
        "東京": ("35.676192","139.650311","13"), 
        "千葉": ("35.335416","140.183252","08"), 
        "埼玉": ("35.996251","139.446601","12"), 
        "茨城": ("36.219357","140.183252","09"), 
        "群馬": ("36.560539","138.879997","11"),
        "山梨": ("35.663511","138.638888","19"), 
        "神奈川": ("35.491354","139.284143","14"), 
        "栃木": ("36.671474","139.854727","10") 
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
        # openweatherの降水量が日本はまだ適用外なのでjjwdから持ってきています
        umb_url = 'https://jjwd.info/api/v2/station/44056'
        umb_data = requests.get(umb_url)
        all_data = umb_data.json()
        # print(json.dumps(rall_data, indent=3))
        pre_day = all_data.get("station").get("preall").get("precip_daily")
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
            syousai = f"\n\n{today_rain}\n\n朝昼晩に分けての降水確率は、\n{morning_rain}%\n{noon_rain}%\n{night_rain}%\n一日の降水量は{pre_day}mmです！！！"

            client.chat_postMessage(
                channel=content.body["channel"],
                blocks=message_format(negirai, syousai),
            )
    elif "天気" in msg:
        tenki_response = requests.get(TENKI_URL).json()

        #現在の気象データを取得
        daily = tenki_response["daily"]
        current = tenki_response["current"]

        try:
        #現在の天気のパラメータ（雨・晴・曇りなどなど）
            res_mark = current["weather"][0]["main"]
        except KeyError as e:
            print("キーが無いらしいよ:",e)
        # 呼び出しの年月日を取得
        now = datetime.datetime.now()
        now_year = str(now.year)
        now_month = str(now.month)
        now_day = str(now.day)

        #服着ろ警報(体感温度取得)
        feels_like = daily[0].get("feels_like")
        #朝の気温
        temp_morn = feels_like["morn"]
        #昼の気温
        temp_day = feels_like["day"]
        #夜の気温
        temp_night = feels_like["night"]


        #おすすめ服分岐用
        if 40 <= max(feels_like.values()):
            get_dress = "裸でいいんじゃないかなってレベルで暑いね！！！水分をこまめに取ろう！！！！！"
        elif 30 <= max(feels_like.values()) <= 39:
            get_dress = "う〜ん、暑いね！！半袖シャツで十分！！！！日焼け止めとか紫外線対策も忘れずにね！！！！！"
        elif 25 <= max(feels_like.values()) <= 29:
            get_dress = "ちょっと暑く感じるかも！！薄手の長袖シャツ〜暑がりさんは半袖シャツがおすすめ！！！！！"
        elif 20 <= max(feels_like.values()) <= 24:
            get_dress = "そろそろ袖が欲しくなるかも！！長袖シャツがおすすめだよ！！！"
        elif 16 <= max(feels_like.values()) <= 19:
            get_dress = "ちょっと肌寒く感じるかも！！！長袖シャツと軽く羽織っていくと良いと思うよ！！！！"
        elif 12 <= max(feels_like.values()) <= 15:
            get_dress = "うん、普通に寒いね！！！セーターか長袖シャツ＋ジャケットがおすすめだよ！！！！！"
        elif 7 <= max(feels_like.values()) <= 11:
            get_dress = "寒いね！！！！！！！冬服の上に薄手のコートが欲しいね！！！！"
        else:
            get_dress = "めっっっちゃ寒いね！？！？！？！とにかくしっかり防寒対策してね！！！！！"


        # 英語をそれぞれ日本語にしてくれる辞書
        main_weather = {
            "Rain": "雨が降ってますね・・・:umbrella:",
            "Clear": "晴れてますよ〜！！！:sunny::sunny:",
            "Clear sky": ":sparkles::sunny:雲ひとつない最高の晴れですよ！！！！:sunny::sparkles:",
            "Thunderstorm": "雷と雨が襲来します！！！！:pika::pika:",
            "Drizzle": "霧雨！！防水にお気をつけ下さい！！！:shower:",
            "Snow": "・・・？！雪が降っている？！:snowflake:",
            "Mist": "かすんでます！！！！:new_moon_with_face:",
            "Smoke": "けむいですご注意ください！！！！！:yosi:",
            "Haze": "もやもや気味です！！！！:hotsprings:",
            "Dust": "ほこりっぽいです！！！:mask:",
            "Fog": "きりだぁああああ前方注意！！！！！！:dash:",
            "Sand": "砂ぼこりが舞ってます！！僕も舞います！！！！:camel::踊る男性:",
            "Ash": "火山灰が降ってます！！お逃げの準備を！！！！:volcano:",
            "Squall": "嵐ですよ！！！！！:ocean:",
            "Tornado": "竜巻が来日してます！！！:cycrone:",
            "Clouds": "曇ってます:cloud:でも僕の心はいつでも晴れてますよ！！:sunglasses:",
        }

        if main_weather.get(res_mark):
            res_mark = main_weather.get(res_mark)
        else:
            res_mark = f"設定辞書に{res_mark}が含まれてないみたいだよ"

        if "天気" in msg:
            aisatu = "\n*こんにちは！！晴男です！！！*"

            nakami = f"\n\n{now_year}年{now_month}月{now_day}日\n現在の{city}は{res_mark}！！！\n\n朝は{temp_morn}度！！！\n昼は{temp_day}度！！！！\n夜は{temp_night}度！！！！！\n\n{get_dress}"

            client.chat_postMessage(
                channel=content.body["channel"],
                blocks=message_format(aisatu, nakami),
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
