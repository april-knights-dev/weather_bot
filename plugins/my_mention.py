# coding: utf-8

from slack import WebClient
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
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

client = WebClient(token=os.getenv('SLACK_CLIENT_TOKEN'))

API_KEY = "e2b220b4263af8d026cb5e44abd8f568" # xxxに自分のAPI_Keyを入力。
@listen_to('(.*)')
def reply_weather(message, arg):

    if re.search('^天気|^傘', arg) is None:
        return

    # prefecture_set = {"東京":("Tokyo", "13"), "千葉":("Chiba", "08"), "埼玉":("Saitama", "12"), "茨城":("Ibaraki", "09"), 
    # "群馬":("Gunma", "11"), "山梨":("Yamanashi", "19"), "神奈川":("Kanagawa", "14"), "栃木":("Tochigi", "10") }
    # if msg in prefecture_set.keys():
        #Trueの時だけ次の処理をする
    # TENKI_URL =f"http://api.openweathermap.org/data/2.5/weather?units=metric&q={msg}/{prefecture_set[msg][0]}&APPID={API_KEY}&lang=ja"
    # KASA_URL =f"http://www.drk7.jp/weather/xml.{msg}/{prefecture_set[msg][1]}.xml"

    if "千葉" in arg:
        city_name = "Chiba"
        city_id = "08"
        city = "千葉県"
    elif "埼玉" in arg:
        city_name = "Saitama"
        city_id = "12"
        city = "埼玉県"
    elif "茨城" in arg:
        city_name = "Ibaraki"
        city_id = "09"
        city = "茨城県"
    elif "群馬" in arg:
        city_name = "Gunma"
        city_id = "11"
        city = "群馬県"
    elif "山梨" in arg:
        city_name = "Yamanashi"
        city_id = "19"
        city = "山梨県"
    elif "神奈川" in arg:
        city_name = "Kanagawa"
        city_id = "14"
        city = "神奈川県"
    elif "栃木" in arg:
        city_name = "Tochigi"
        city_id = "10"
        city = "栃木県"
    else:
        city_name ="Tokyo"
        city_id = "13"
        city = "東京都"

    # スクレイピング対象の URL にリクエストを送り HTML を取得する
    res_url = requests.get(f'http://www.drk7.jp/weather/xml/{city_id}.xml')

    # レスポンスの HTML から BeautifulSoup オブジェクトを作る
    soup = BeautifulSoup(res_url.content, 'html.parser')

    # 降水確率リスト表記
    items = list(soup.find("rainfallchance").stripped_strings)

    # 6時間毎の降水確率
    # rain06 = int(items[0])
    rain612 = int(items[1])
    rain1218 = int(items[2])
    rain1824 = int(items[3])



    # 一日の降水確率最大
    if 70 <= int(max(items)):
        Today_rain = f'今日一日の{city}の降水確率は\n' + max(items)+ '%\n:alert:' + '傘絶対忘れないでください！！！:umbrella_with_rain_drops:'
    elif 40 <= int(max(items)):
        Today_rain = f'今日一日の{city}の降水確率は\n' + max(items) + '%\n' + '傘持っていってください！！！:umbrella:'
    elif 20 <= int(max(items)):
        Today_rain = f'今日一日の{city}の降水確率は\n' + max(items) + '%\n' + '折り畳み傘があった方がいいかも！！！:closed_umbrella::handbag:'
    else:
        Today_rain = f'今日一日の{city}の降水確率は\n' + max(items) + '%\n' + ':sunny::sunglasses:'

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




    # city_nameで指定した地域のお天気結果取得
    res_api = get_api_response(city_name)
    # pprint.pprint(res_api)


    #mainから取得
    res_main = res_api.get("main")
    #res_pressure = res_main.get("pressure")
    res_temp = str(res_main.get("temp"))

    #weatherから取得
    res_weather = res_api.get("weather")
    res_weatherlist = res_weather[0]
    res_mark = res_weatherlist.get("main")

    

    date_time = str(datetime.date.today())

    #英語をそれぞれ日本語にしてくれる辞書
    main_weather ={"Rain":"雨が降ってますね・・・:umbrella:",  "clear sky":"晴れてますよ！！良いぞ:sunny::sunny:", "Thunderstorm":"雷と雨が襲来します:pika::pika:", "Drizzle":"霧雨、防水にお気をつけ下さい:shower:", "Snow":"・・・？！雪が降っている？！:snowflake:", 
 "Mist":"かすんでます:new_moon_with_face:", "Smoke":"けむいですご注意ください:yosi:", "Haze":"もやもや気味です:hotsprings:", "Dust":"ほこりっぽいです:mask:", "Fog":"きりだぁああああ前方注意:dash:", "Sand":"砂ぼこりが舞ってます！！僕も舞います:camel::踊る男性:", "Ash":"火山灰が降ってます！！お逃げの準備を:volcano:", 
 "Squall":"嵐のコンサートですよ:ocean:", "Tornado":"竜巻が来日してます:cycrone:", "Clouds":"曇ってます:cloud:だけど僕の心は晴れてます:sunglasses:"}

    # main_weather[res_mark]

    if main_weather.get(res_mark):
        res_mark = main_weather.get(res_mark)
    else:
        res_mark = f"設定辞書に{res_mark}が含まれてないみたいだよ"
    
    if "天気" in arg:
        message.reply(f"\nこんにちは！晴男です！！！\n{date_time} 現在の{city}は{res_mark}！！！\n気温は{res_temp}度です！！！") 
        # client.chat_postMessage(
        #     channel=message.body['channel'],
        #     blocks=message_format("*こんにちは！！晴男です！！！*",date_time + "\n現在の"+ city + "は" + res_mark + "！！！\n気温は" + res_temp + "度です！！！")
        #     )

    if "傘" in arg :
        message.send(f"\nお疲れ様です！！！晴男です！！！\n\n{Today_rain}\n\n朝昼晩に分けての降水確率は、\n{Morning_rain}%\n{Noon_rain}%\n{Night_rain}%\n\n今日も一日頑張りましょう！！！")
        # client.chat_postMessage(
        #     channel=message.body['channel'],
        #     blocks=message_format("*お疲れ様です！！！晴男です！！！*",Today_rain +"\n\n朝昼晩に分けての降水確率は、"+ Morning_rain + "%\n" + Noon_rain + "%\n" + Night_rain +"%\n\nですよ〜！！！")
        # )

# if msg in "傘" or "天気":
#      prefectre_set.get()

# if 傘 in msg:
#     result_message = unbrella()
#     post_message("G0149FE9SAW", result_message)
    
# if 天気 in msg:
#      result_message = weather()
#      post_message("G0149FE9SAW", result_message)
    


def get_api_response(city):
  request_url = f"http://api.openweathermap.org/data/2.5/weather?units=metric&q={city}&APPID={API_KEY}&lang=ja"
  response = requests.get(request_url)
  data = response.json()

  return data

# def message_format(aisatu,message):
#     blockkit = [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": aisatu
#                 }
#             },
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": message
#                 }
#             }
#         ]
#     return blockkit
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