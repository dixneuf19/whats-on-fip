import logging
import os

from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from whats_on_fip.telegram.handlers import get_feelgood, get_fiftyfifty, get_live, get_meuh

load_dotenv()
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

BOT_TELEGRAM_TOKEN = os.getenv("BOT_TELEGRAM_TOKEN")
BOT_WEBHOOK_PATH = os.getenv("BOT_WEBHOOK_PATH")
BOT_WEBHOOK_URL = os.getenv("BOT_WEBHOOK_URL", "https://fip-telegram-bot.dixneuf19.fr")

USE_POLLING = os.getenv("USE_POLLING") in ("True", "true", "1")


async def display_help(update, context):
    help_message = """
This bot helps you share your love of FIP and other radios!

It tries to fetch the live of the radio you are listening to and share it with your friends. It also adds a link to the song on Spotify.

The following radios are supported:
FIP - /live /whatsonFIP
RadioMeuh - /meuh
Radio5050 - /5050
FeelGood - /feelgood /fg
    """
    await update.message.reply_text(help_message)


def main():
    if not BOT_TELEGRAM_TOKEN:
        raise RuntimeError("BOT_TELEGRAM_TOKEN environment variable is required")

    application = Application.builder().token(BOT_TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("whatsonFIP", get_live))
    application.add_handler(CommandHandler("live", get_live))
    application.add_handler(CommandHandler("meuh", get_meuh))
    application.add_handler(CommandHandler("5050", get_fiftyfifty))
    application.add_handler(CommandHandler("feelgood", get_feelgood))
    application.add_handler(CommandHandler("fg", get_feelgood))
    application.add_handler(CommandHandler("help", display_help))
    application.add_handler(MessageHandler(filters.COMMAND, display_help))

    if USE_POLLING:
        application.run_polling()
    else:
        if not BOT_WEBHOOK_PATH:
            raise RuntimeError("BOT_WEBHOOK_PATH environment variable is required for webhook mode")
        application.run_webhook(
            listen="0.0.0.0",
            port=80,
            url_path=BOT_WEBHOOK_PATH,
            webhook_url=f"{BOT_WEBHOOK_URL}/{BOT_WEBHOOK_PATH}",
        )


if __name__ == "__main__":
    main()
