# coding: utf-8
import os
from threading import Thread

import slack
from slackbot.bot import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

from plugins import umbrella

client = slack.WebClient(token=os.environ['API_TOKEN'])
sched = BlockingScheduler()

# 傘警報の起動
def send_message(channel,message,name,icon):
    client.chat_postMessage(channel=channel,text=message,username=name,icon_url=icon)

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=7, minute=0)
def job_timed():
    send_message('CA798CMV0', umbrella.get_umbrella(),u'晴男の叫ぶ天気bot',"https://i.gyazo.com/4c739950d92831d22c64e4fcb1ab394d.png")
    print(umbrella.get_umbrella())

def main():
    bot = Bot()
    bot.run()
    print("立ち上がリーヨ")

if __name__ == "__main__":
    print('start slackbot')

    # RTMbotの起動
    job = Thread(target=main)
    job.start()

    # 傘警報の起動
    job = Thread(target=sched.start)
    job.start()