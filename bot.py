from aiogram import executor
from dispacher import dp

from dispacher import bot
from aiogram import types
import config
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@dp.message_handler(is_owner=True, commands=['post'])
async def post_cmd(message:types.Message):
    config.IS_POSTING_REQUESTED = True
    await message.answer('Пришлите текст поста с картинкой или без')


@dp.message_handler(is_owner=True, commands=['setlink'])
async def setlink_command(message: types.Message):
    with open('link.txt', 'w+') as f:
        f.write(message.text.replace('/setlink', ' ').strip())
        f.close()

    await message.answer('Ссылка сохранена')


@dp.message_handler(is_owner=True, commands=['getlink'])
async def getlink_command(message: types.Message):
    with  open('link.txt', 'r') as f:
        content = f.readlines()
        f.close()

    await message.answer('Текущая ссылка:{}'.format(content[0].strip()))


@dp.message_handler(is_owner=True)
async def message_handler(message:types.Message):
    if config.IS_POSTING_REQUESTED:
        config.IS_POSTING_REQUESTED = False
        inline_btn = InlineKeyboardButton("Получите ссылку", url="https://t.me/@betinsider55", callback_data="get_link_button")
        inline_kb = InlineKeyboardMarkup().add(inline_btn)

        await message.bot.send_message(config.CHANNEL,message.text, reply_markup=inline_kb)
        await message.answer('Пост опубликован')


# Callback
@dp.callback_query_handler(lambda c: c.data == "get_link_button")
async def process_cq_link_button(c: types.CallbackQuery):
    try:
        member = await bot.get_chat_member(config.CHANNEL, c.from_user.id)

        if (member["status"] in ("member", "creator", "administrator")):
            with open('link.txt', 'r') as f:
                content = f.readlines()
                f.close()

            await bot.answer_callback_query(c.id, 'Ссылка - {}'.format(content[0].strip()), show_alert=True)
        else:
            await bot.answer_callback_query(c.id, "Подпишись на канал!", show_alert=True)
    except:
        await bot.answer_callback_query(c.id, "Подпишись на канал!", show_alert=True)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
