# coding: utf-8
import os
from threading import Thread

import slack
from slackbot.bot import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

client = slack.WebClient(token=os.environ['API_TOKEN'])
sched = BlockingScheduler()

def send_message(channel, message):
    client.chat_postMessage(channel=channel, text=message)

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=7, minute=30)
def timed_job():
    # みぎに降雨情報のメッセージ引数わたす  IDは放牧部屋
    send_message('G0149FE9SAW', "send_umbrella")


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    print('start slackbot')

    # RTMbotの起動
    job = Thread(target=main)
    job.start()

    # APSchedulerの起動
    job = Thread(target=sched.start)
    job.start()