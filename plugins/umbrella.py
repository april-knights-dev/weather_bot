# coding: utf-8

from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
from datetime import datetime
from slacker import Slacker

import os
import requests
import urllib.request as req
import datetime
from bs4 import BeautifulSoup
import schedule
import time

def job():

    # def send_umbrella(message):

        # 地域指定
        # @listen_to('(.*)')
        # def reply_umbrella(message, arg):

        #     if re.search('^傘', arg) is None:
        #         return

        #     if "千葉" in arg:
        #         city_name = "08"
        #         city = "千葉"
        #     elif "栃木" in arg:
        #         city_name = "09"
        #         city = "栃木"
        #     elif "群馬" in arg:
        #         city_name = "10"
        #         city = "群馬"
        #     elif "埼玉" in arg:
        #         city_name = "11"
        #         city = "埼玉"
        #     elif "千葉" in arg:
        #         city_name = "12"
        #         city = "千葉"
        #     elif "神奈川" in arg:
        #         city_name = "14"
        #         city = "神奈川"
        #     elif "山梨" in arg:
        #         city_name = "19"
        #         city = "山梨"
        #     else:
        #         city_name ="13"
        #         city = "東京"
        
        # return reply_umbrella

        #地域テスト
        city = ""
        if "千葉" in city:
            city_name = "08"
            city = "千葉"
        elif "栃木" in city:
            city_name = "09"
            city = "栃木"
        elif "群馬" in city:
            city_name = "10"
            city = "群馬"
        elif "埼玉" in city:
            city_name = "11"
            city = "埼玉"
        elif "千葉" in city:
            city_name = "12"
            city = "千葉"
        elif "神奈川" in city:
            city_name = "14"
            city = "神奈川"
        elif "山梨" in city:
            city_name = "19"
            city = "山梨"
        else:
            city_name ="13"
            city = "東京"

        
        # スクレイピング対象の URL にリクエストを送り HTML を取得する
        res = requests.get(f'http://www.drk7.jp/weather/xml/{city_name}.xml')

        # レスポンスの HTML から BeautifulSoup オブジェクトを作る
        soup = BeautifulSoup(res.content, 'html.parser')# BeautifulSoupの初期化

        #print(soup.prettify()) 


        # 降水確率リスト表記
        items = list(soup.find("rainfallchance").stripped_strings)

        # 6時間毎の降水確率
        # rain06 = int(items[0])
        rain612 = int(items[1])
        rain1218 = int(items[2])
        rain1824 = int(items[3])



        # 一日の降水確率最大
        if 70 <= int(max(items)):
            print (f'今日一日の{city}の降水確率は\n' + max(items)+ '%だから' + '傘絶対忘れないで！！！')
        elif 40 <= int(max(items)):
            print(f'今日一日の{city}の降水確率は\n' + max(items) + '%だから' + '傘持っていって！風邪ひくよ！')
        elif 20 <= int(max(items)):
            print(f'今日一日の{city}の降水確率は\n' + max(items) + '%だから' + '折り畳み傘あった方がいいかも！')
        else:
            print (f'今日一日の{city}の降水確率は\n' + max(items) + '%だから' + '傘いらないよー')

        # 雨警報条件分岐 6~24時
        if 70 <= int(rain612):
            print (' 6~12時：' + items[1] + '%' + '\n傘をもって' + 'ちょっと早めに家でた方が良いかも！')
        elif 40 <= int(rain612):
            print(' 6~12時：' + items[1] + '%')
        elif 20 <= int(rain612):
            print(' 6~12時：' + items[1] + '%')
        else:
            print (' 6~12時：' + items[1] + '%')

        if 70 <= int(rain1218):
            print ('12~18時：' + items[2] + '%')
        elif 40 <= int(rain1218):
            print('12~18時：' + items[2] + '%')
        elif 20 <= int(rain1218):
            print('12~18時：' + items[2] + '%')
        else:
            print ('12~18時：' + items[2] + '%')

        if 70 <= int(rain1824):
            print ('18~24時：' + items[3] + '%')
        elif 40 <= int(rain1824):
            print('18~24時：' + items[3] + '%')
        elif 20 <= int(rain1824):
            print('18~24時：' + items[3] + '%' + '\n雨降っててもわんちゃん気合いで帰れるよ！')
        else:
            print ('18~24時：' + items[3] + '%' + '\n晴男が仕事してる！！！')


        # message.send(text='こんにちは！！！',channel='#test_umbrella')
        # return send_umbrella

schedule.every().day.at("12:00").do(job)
  
while True:
  schedule.run_pending()
  time.sleep(30)