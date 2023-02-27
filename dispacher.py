import logging
from aiogram import Bot, Dispatcher
from filters import IsOwnerFilter
import config

logging.basicConfig(level=logging.INFO)

if not config.BOT_TOKEN:
    exit("No token provided")

bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)

dp.filters_factory.bind(IsOwnerFilter)
