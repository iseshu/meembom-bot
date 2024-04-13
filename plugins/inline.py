from helpers.db import Mydb
from pyrogram import Client,filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
db = Mydb()

home_markup = [[InlineKeyboardButton(text="Get Users", callback_data="get-users")],
               [InlineKeyboardButton(text="Get GiveAways", callback_data="page-1")],
             [InlineKeyboardButton(text="Support", url="https://t.me/yssprojects")]]

@Client.on_callback_query(filters.regex('get-users') | filters.regex('home') | filters.regex('user-') | filters.regex('del-') | filters.regex('add-user'))
async def callback(client, query):
    if query.data == 'get-users':
        users = db.get_users()
        text = 'Here are the users:'
        markup = [[InlineKeyboardButton(text=user.email, callback_data=f"user-{user.id}")] for user in users ] if users else []
        markup.append([InlineKeyboardButton(text='➕ Add User',callback_data='add-user')])
        markup.append([InlineKeyboardButton(text='👈 Back',callback_data='home')])
        await query.message.edit_text(text,reply_markup=InlineKeyboardMarkup(markup))
    elif query.data == 'home':
        await query.message.edit_text('Hello! \n\nI am a bot that can send you the latest giveaways from meembom.com\n\nCreate with ❤️ by @iamyss',
                                      reply_markup=InlineKeyboardMarkup(home_markup))
    elif query.data.startswith('user-'):
        id = int(query.data.split('-')[1])
        user = db.get_user(id)
        if user:
            await query.message.edit_text(f'User: {user.email}\nInsta ID: {user.instaid}',
                                          reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='🗑️ Delete',callback_data=f'del-{user.id}')],
                 [InlineKeyboardButton(text='👈 Back',callback_data='get-users')]]
            ))
        else:
            await query.message.edit_text('Hello! \n\nI am a bot that can send you the latest giveaways from meembom.com\n\nCreate with ❤️ by @iamyss',
                                      reply_markup=InlineKeyboardMarkup(home_markup))
            await query.answer(f"User Not Found",show_alert=True)
            
    elif query.data.startswith('del-'):
        id = int(query.data.split('-')[1])
        db.delete_user(id)
        await query.message.edit_text('User deleted',reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='👈 Back',callback_data='get-users')]]
        ))
    elif query.data == 'add-user':
        await query.message.edit_text('Send the insta id and email separated by comma\nExample:`/add joe_doe,example@gmail.com`',
                                      reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='👈 Back',callback_data='get-users')]]
        ))