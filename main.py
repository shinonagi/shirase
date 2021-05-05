import os
import sys
from collections import namedtuple
from datetime import datetime, time

import discord
import jpholiday
from discord.ext import tasks

import data_shirase

client = discord.Client()
channel_id = data_shirase.channel_id()
mention_id = "<@&"+str(data_shirase.role_id())+"> "

Timetables = namedtuple('Timetables', ('weekends_and_holidays', 'weekdays'))
timetables = Timetables(
    weekends_and_holidays=[time(8, 50), time(17)],
    weekdays=[time(7, 30), time(12, 53), time(17, 50), time(21)]
)


@client.event
async def on_ready():
    print('login now')


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if client.user in message.mentions:
        list_content = message.content.split()
        if list_content[1] == 'test':  # test
            await message.channel.send(mention_id + 'test')
        elif list_content[1] == 'shutdown':  # shutdown
            if message.author.guild_permissions.administrator:
                await message.channel.send('shutdown now')
                await client.logout()
                print('logouted')
            else:
                await message.channel.send('you are not admin user')
        else:
            await message.channel.send('no such commnad')


def is_weekend_or_holiday(datetime):
    return datetime.weekday() >= 5 or jpholiday.is_holiday(datetime)


def url(datetime):
    return datetime.strftime("https://radiko.jp/#!/ts/RN1/%Y%m%d%H%M00")


@tasks.loop(seconds=60)
async def loop():
    now = datetime.now().replace(second=0, microsecond=0)
    timetable = timetables.weekends_and_holidays if is_weekend_or_holiday(
        now) else timetables.weekdays
    if now.time() in timetable:
        channel = client.get_channel(channel_id)
        await channel.send(mention_id + url(now))
loop.start()


client.run(data_shirase.token())
