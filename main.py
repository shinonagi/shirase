import os
import sys
from collections import namedtuple
from datetime import datetime

import discord
import jpholiday
from discord.ext import tasks

sys.path.append(os.pardir)
import data_shirase

client = discord.Client()
channel_id = data_shirase.channel_id()
mention_id = "<@&"+str(data_shirase.role_id())+"> "

Timetables = namedtuple('Timetables', ('weekends_and_holidays', 'weekdays'))
timetables = Timetables(
    weekends_and_holidays=['0850', '1700'],
    weekdays=['0730', '1253', '1750', '2100']
)


@client.event
async def on_ready():
    print('login now')


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if client.user in message.mentions:
        global reply
        reply = ""
        list_content = message.content.split()
        if list_content[1] == 'test':  # test
            reply = mention_id + "test"
        elif list_content[1] == 'shutdown':  # shutdown
            if message.author.guild_permissions.administrator:
                await message.channel.send('shutdown now')
                await client.logout()
                print('logouted')
            else:
                await message.channel.send('you are not admin user')
        if reply == "":
            reply = 'no such commnad'
        await message.channel.send(reply)  # reply


def is_weekend_or_holiday(datetime):
    return datetime.weekday() >= 5 or jpholiday.is_holiday(datetime)


def url(datetime):
    return datetime.strftime("https://radiko.jp/#!/ts/RN1/%Y%m%d%H%M00")


@tasks.loop(seconds=60)
async def loop():
    now = datetime.now()
    timetable = timetables.weekends_and_holidays if is_weekend_or_holiday(
        now) else timetables.weekdays
    if now.strftime('%H%M') in timetable:
        channel = client.get_channel(channel_id)
        await channel.send(mention_id + url(now))
loop.start()


client.run(data_shirase.token())
