# coding: utf-8
import os
import re
from threading import Thread

import slack
# from slackbot.bot import Bot
from apscheduler.schedulers.blocking import BlockingScheduler
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from flask import Flask

from plugins import umbrella, my_mention

client = slack.WebClient(token=os.environ['API_TOKEN'])
sched = BlockingScheduler()


app = Flask(__name__)
signing_secret = os.environ["SLACK_SIGINING"]
slack_events_adapter = SlackEventAdapter(signing_secret, "/slack/events", app)

# 傘警報の起動
def send_message(channel,message,name,icon):
    client.chat_postMessage(channel=channel,text=message,username=name,icon_url=icon)

@slack_events_adapter.on("message")
def events_adapter(slack_request):
    message = slack_request["event"]
    channel = message["channel"]

    if message.get("subtype") is None and re.search("^天気($|!+?|！+?|\s)|^傘($|!+?|！+?|\s)", message["text"]):
        my_mention.reply_weather(message["text"], channel)

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=7, minute=0)
def job_timed():
    send_message('CA798CMV0', umbrella.get_umbrella(),u'晴男の叫ぶ天気bot',"https://i.gyazo.com/4c739950d92831d22c64e4fcb1ab394d.png")
    print(umbrella.get_umbrella())

def main():
    # flaskの起動
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    print('start flask')

    # RTMbotの起動
    # flaskの起動
    job = Thread(target=main)
    job.start()

    # 傘警報の起動
    job = Thread(target=sched.start)
    job.start()