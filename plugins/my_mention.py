# coding: utf-8

from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
from datetime import datetime

import os
import requests
import urllib.request as req
import sys
import json

city_name = "Tokyo" # 主要な都市名はいけるっぽい。
API_KEY = "e2b220b4263af8d026cb5e44abd8f568" # xxxに自分のAPI Keyを入力。
api = "http://api.openweathermap.org/data/2.5/weather?units=metric&q={city}&APPID={key}&lang=ja"

url = api.format(city = city_name, key = API_KEY)
print(url)
response = requests.get(url)
data = response.json()
jsonText = json.dumps(data, indent=4)
print(jsonText)


res_api = json.loads(jsonText)
#mainから取得
res_main = res_api.get("main")
res_pressure = res_main.get("pressure")
res_temp = res_main.get("temp")
#weatherから取得
res_weather = res_api.get("weather")
res_weatherlist = res_weather[0]
res_description = res_weatherlist.get("description")
res_mark = res_weatherlist.get("main")
#その他res_apiから取得
res_cityname = res_api.get("name")
res_timezone = res_api.get("dt")

main_weather ={ "Rain":"雨",  "clear sky":"晴", "Thunderstorm":"雷雨", "Drizzle":"霧雨", "Snow":"雪", 
"Mist":"かすみ", "Smoke":"煙", "Haze":"もや", "Dust":"ほこり", "Fog":"きり", "Sand":"砂ぼこり", "Ash":"火山灰", 
"Squall":"嵐", "Tornado":"竜巻"}
main_weather[res_mark] 

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
@listen_to("^天気")
def mention_func(message):
 message.reply(f"\n{datetime.fromtimestamp(res_timezone)}の{res_cityname}は{main_weather[res_mark]}です。\n平均気温は{res_temp}度で、{res_description}です") # メンション
# @listen_to('リッスン')
# def listen_func(message):
#     message.send('誰かがリッスンと投稿したようだ')      # ただの投稿
#     message.reply('君だね？')

