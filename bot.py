import os

from config import BOT_TOKEN, PRIVATE_CHANNEL_ID, logger

import nextcord
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    logger.info("Бот запущен!")


def setup_bot():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            bot.load_extension(f"cogs.{file[:-3]}")

    bot.run(BOT_TOKEN)


if __name__ == "__main__":
    setup_bot()
