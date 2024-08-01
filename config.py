import logging

BOT_TOKEN = "bot_token" # api ключ бота

GUILD_ID = 11212321321 # айди сервера
PRIVATE_CHANNEL_ID = 12321 # айди приватного канала с вопросами
PUBLIC_CHANNEL_ID = 12312321321 # айди публичного канала с ответами

admins = [333544814266286081, 710403299245031585]

logging.basicConfig(filename="logs/logs.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)
