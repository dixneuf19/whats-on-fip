import logging
import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from whats_on_fip.telegram.handlers import get_feelgood, get_fiftyfifty, get_live, get_meuh

load_dotenv()
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

BOT_TELEGRAM_TOKEN = os.getenv("BOT_TELEGRAM_TOKEN")
BOT_WEBHOOK_PATH = os.getenv("BOT_WEBHOOK_PATH")
BOT_WEBHOOK_URL = os.getenv("BOT_WEBHOOK_URL", "https://fip-telegram-bot.dixneuf19.fr")

USE_POLLING = os.getenv("USE_POLLING") in ("True", "true", "1")


def display_help(update, context):
    help_message = """
This bot helps you share your love of FIP and other radios!

It tries to fetch the live of the radio you are listening to and share it with your friends. It also adds a link to the song on Spotify.

The following radios are supported:
FIP - /live /whatsonFIP
RadioMeuh - /meuh
Radio5050 - /5050
FeelGood - /feelgood /fg
    """
    update.message.reply_text(help_message)


def main():
    if not BOT_TELEGRAM_TOKEN:
        raise RuntimeError("BOT_TELEGRAM_TOKEN environment variable is required")

    updater = Updater(BOT_TELEGRAM_TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("whatsonFIP", get_live))
    updater.dispatcher.add_handler(CommandHandler("live", get_live))
    updater.dispatcher.add_handler(CommandHandler("meuh", get_meuh))
    updater.dispatcher.add_handler(CommandHandler("5050", get_fiftyfifty))
    updater.dispatcher.add_handler(CommandHandler("feelgood", get_feelgood))
    updater.dispatcher.add_handler(CommandHandler("fg", get_feelgood))
    updater.dispatcher.add_handler(CommandHandler("help", display_help))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, display_help))

    if USE_POLLING:
        updater.start_polling()
        logging.info("Start polling")
        updater.idle()
    else:
        if not BOT_WEBHOOK_PATH:
            raise RuntimeError("BOT_WEBHOOK_PATH environment variable is required for webhook mode")
        updater.start_webhook(listen="0.0.0.0", port=80, url_path=BOT_WEBHOOK_PATH)
        updater.bot.set_webhook(f"{BOT_WEBHOOK_URL}/{BOT_WEBHOOK_PATH}")
        updater.idle()


if __name__ == "__main__":
    main()
