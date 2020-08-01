# coding: utf-8
import os
from threading import Thread

import slack
from slackbot.bot import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

client = slack.WebClient(token=os.environ['API_TOKEN'])
sched = BlockingScheduler()

# 傘警報の起動
def send_message(channel,message):
    client.chat_postMessage(channel=channel,text=message)

@sched.scheduled_job('cron', day_of_week='mon-sat', hour=11, minute=46)
def job_timed():
    send_message('G0149FE9SAW', '')

def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    print('start slackbot')

    # RTMbotの起動
    job = Thread(target=main)
    job.start()

    # 傘警報の起動
    job = Thread(target=sched.start)
    job.start()