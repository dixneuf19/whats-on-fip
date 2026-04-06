import logging
from collections.abc import Callable

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

from whats_on_fip.deezer import add_deezer_external_url
from whats_on_fip.models import (
    FEELGOOD_RADIO,
    FIFTYFIFTY_RADIO,
    FIP_RADIO,
    MEUH_RADIO,
    Radio,
    Track,
)
from whats_on_fip.radio_feelgood_api import RadioFeelGood
from whats_on_fip.radio_fiftyfifty import Radio5050
from whats_on_fip.radio_france_api import LiveUnavailableException, execute_live_query
from whats_on_fip.radio_meuh_api import RadioMeuh
from whats_on_fip.telegram.fmt import track_to_markdown

ERROR_MESSAGE = """Hum something went wrong... \nPing @dixneuf19 !"""


async def _handle_radio(
    update: Update, context: ContextTypes.DEFAULT_TYPE, fetch_track: Callable[[], Track], radio: Radio
):
    message = update.message
    if message is None:
        return

    logging.info(
        f"Got '{message.text}' from {message.from_user.username if message.from_user else '?'} in {message.chat.title}"
    )
    try:
        track = fetch_track()

        try:
            track = add_deezer_external_url(track)
        except Exception as e:
            logging.warning(f"Error enriching with Deezer: {e}")

        logging.info(f"Found this song live: {track}")
        await message.reply_text(
            track_to_markdown(track, radio=radio),
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True,
        )

    except LiveUnavailableException:
        logging.info("No track information available right now")
        await message.reply_text(
            escape_markdown("No live song information right now, is it ", version=2)
            + "_Club Jazzafip_"
            + escape_markdown(" ?", version=2),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    except Exception as e:
        logging.error(e)
        await message.reply_text(
            escape_markdown(ERROR_MESSAGE, version=2),
            parse_mode=ParseMode.MARKDOWN_V2,
        )


async def get_live(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _handle_radio(update, context, lambda: execute_live_query("FIP"), FIP_RADIO)


async def get_meuh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _handle_radio(update, context, lambda: RadioMeuh().get_current_track(), MEUH_RADIO)


async def get_fiftyfifty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _handle_radio(update, context, lambda: Radio5050().get_current_track(), FIFTYFIFTY_RADIO)


async def get_feelgood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _handle_radio(update, context, lambda: RadioFeelGood().get_current_track(), FEELGOOD_RADIO)
