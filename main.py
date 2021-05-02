import datetime
import os
import sys

import discord
import jpholiday
from discord.ext import tasks

sys.path.append(os.pardir)
import data_shirase

client = discord.Client()
channel_id = data_shirase.channel_id()
mention_id = "<@&"+str(data_shirase.role_id())+"> "


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


def is_holiday(weekday, date):
    if weekday >= 5 or jpholiday.is_holiday(date):
        return 1
    else:
        return 0


def url(date, time):
    url = mention_id + "https://radiko.jp/#!/ts/RN1/" + date + time + "00"
    return url


@tasks.loop(seconds=60)
async def loop():
    weekday = datetime.date.today().weekday()
    date = datetime.datetime.now().strftime('%Y%m%d')
    time = datetime.datetime.now().strftime('%H%M')
    if is_holiday(weekday, date) == 1:
        if time == '0850' or time == '1700':  # 土日
            channel = client.get_channel(channel_id)
            await channel.send(url(date, time))
    elif time == '0730' or time == '1253' or time == '1750' or time == '2100':  # 平日
        channel = client.get_channel(channel_id)
        await channel.send(url(date, time))
loop.start()


client.run(data_shirase.token())
