import discord
from datetime import datetime
import threading
import time
import settings as env
import asyncio
from db_helper import DBhelper
db = DBhelper()
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    while(True):
    	await checkTime()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

async def checkTime():
    # This function runs periodically every 1 second
    #threading.Timer(1, checkTime).start()

    #now = datetime.now()

    #current_time = now.strftime("%H:%M:%S")
    #print("Current Time =", current_time)

    #if(current_time == '02:11:00'):  # check if matches with the desired time
    channel = client.get_channel(944884387596619776)#print('sending message')
    messages = db.get_messages()
    for msg in messages:
        messagez,tstamp=msg#await channel.send(f"Periodically checking messages : {message}")
        for keyw in env.keywords:
            if keyw in messagez:
                print(messagez)
                env.log('T',messagez)
                db.set_timestamp(tstamp)
    time.sleep(4)

client.run('ODg0NzczMDcwMTMxMzI2OTg3.YTdXIg.Y2bkYGYWxD-fVlfXzL67WcsF6kw')