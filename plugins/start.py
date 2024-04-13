from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command(["start"]))
async def start(client, message):
    text = f"Hello {message.from_user.mention}! \n\nI am a bot that can send you the latest giveaways from meembom.com\n\nCreate with ❤️ by @iamyss"
    await message.reply_photo(photo='https://www.meembom.com/static/images/meembom-logo-with-text.png',caption=text,
                              reply_markup=InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Get Users", callback_data="get-users")],
         [InlineKeyboardButton(text="Get GiveAways", callback_data="page-1")],
         [InlineKeyboardButton(text="Support", url="https://t.me/yssprojects")]]
    ))
