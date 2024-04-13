from pyrogram import Client,filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton,InputMediaPhoto
from helpers.meembom import Meembom
from helpers.notify import send_notification
from math import ceil
def display_items(current_page, items_per_page, items_list):
    total_pages = ceil(len(items_list) / items_per_page)
    start_index = (current_page - 1) * items_per_page
    end_index = start_index + items_per_page
    display_items = items_list[start_index:end_index]
    return total_pages, display_items

meembom = Meembom()
@Client.on_callback_query(filters.regex('page-'))
async def giveaways(client, query):
    items = meembom.get_all()
    length =  len(items)
    page = int(query.data.split('-')[1])
    items_per_page = 7
    total_pages, items = display_items(page, items_per_page, items[::-1])
    text = f"Total Giveaways: {length}\n\nyou are in page {page} of {total_pages}\n\n"
    inline = [[InlineKeyboardButton(text=f"{item.title} | {item.expire}", callback_data=f"item-{item.code}")] for item in items]
    if page == 1:
        inline.append([InlineKeyboardButton(text="Next 👉", callback_data=f"page-{page+1}")])
    elif page == total_pages:
        inline.append([InlineKeyboardButton(text="👈 Previous", callback_data=f"page-{page-1}")])
    else:
        inline.append([InlineKeyboardButton(text="👈 Previous", callback_data=f"page-{page-1}"),InlineKeyboardButton(text="Next 👉", callback_data=f"page-{page+1}")])
    inline.append([InlineKeyboardButton(text="🏠 Home", callback_data="home")])
    await query.message.edit_text(text,reply_markup=InlineKeyboardMarkup(inline))

@Client.on_callback_query(filters.regex('item-'))
async def gives(client, query):
    items = meembom.get_all()
    code = int(query.data.split('-')[1])
    item = [item for item in items if item.code == code][0]
    text = f"title: {item.title}\n\nExpire: {item.expire}"
    notify = send_notification('New Giveaway',f'{item.title}\nExpire: {item.expire}',item.url,item.image)
    print(notify)
    await query.answer(text,show_alert=True)