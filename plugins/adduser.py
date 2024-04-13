from pyrogram import Client,filters
from helpers.db import Mydb
db = Mydb()
@Client.on_message(filters.command(["add"]))
async def add(client, message):
    if message.text == "/add":
        await message.reply_text('Send the insta id and email separated by comma\nExample:`/add joe_doe,joedoe@gmail.com`')
    elif '/add ' in message.text:
        insta_id = message.text.split(' ')[1].split(',')[0]
        email = message.text.split(' ')[1].split(',')[1]
        if "@" and "." in email:
            db.add_user(insta_id.strip(),email.strip())
            await message.reply_text('User added')
        else:
            await message.reply_text('Invalid email\nTry Again')