from pyrogram import Client
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from os import environ
from helpers.db import Mydb
from helpers.meembom import Meembom
from datetime import datetime ,timezone,timedelta
from helpers.notify import send_notification
log_channel = environ.get('LOG_CHANNEL')

meembom= Meembom()
db = Mydb()

def get_time():
    utc_timezone = timezone.utc
    ist_offset = timedelta(hours=5, minutes=30)
    utc_now = datetime.now(utc_timezone)
    ist_now = utc_now + ist_offset
    time = ist_now.strftime("%Y-%m-%d %H:%M:%S IST")
    return time


async def do_task():
    message = await bot.send_message(log_channel,'Task started')
    item = meembom.get_last()
    latest = db.get_latest()
    if item.code > latest:
        db.set_latest(item.code)
        if db.get_users():
            for user in db.get_users():
                meembom.login(user.instaid,user.email)
                await message.edit_text('Logged in')
                meembom.get_page(item.code)
                print('Got page')
                meembom.send_api()
                print('Api sent')
                await bot.send_photo(log_channel,photo=item.image,caption=f'New giveaway: {item.title}\nExpire: {item.expire}')
                send_notification('New Giveaway',f'{item.title}\nExpire: {item.expire}',item.url,item.image)
        else:
            await message.edit_text('No users')
    else:
        await message.edit_text('No new giveaway\nchecked at '+get_time())

api_id = environ.get("API_ID")
api_hash = environ.get("API_HASH")
bot_token = environ.get("BOT_TOKEN")

bot = Client("meembom_bot",
             api_id=api_id,
             api_hash=api_hash,
             bot_token=bot_token,
             plugins=dict(root="plugins"))

scheduler = AsyncIOScheduler()


scheduler.add_job(do_task,  'interval', minutes=30)
scheduler.start()

if __name__ == '__main__':
    bot.run()
