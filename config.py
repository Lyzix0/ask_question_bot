import logging

BOT_TOKEN = "bot_token"

GUILD_ID = 11212321321
PRIVATE_CHANNEL_ID = 12321
PUBLIC_CHANNEL_ID = 12312321321

logging.basicConfig(filename="logs/logs.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
