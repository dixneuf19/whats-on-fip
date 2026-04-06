import logging
from typing import Callable

from telegram import ParseMode
from telegram.utils.helpers import escape_markdown

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
from whats_on_fip.spotify import add_spotify_external_url
from whats_on_fip.telegram.fmt import track_to_markdown

ERROR_MESSAGE = """Hum something went wrong... \nPing @dixneuf19 !"""

TRACK_PROVIDERS = ["spotify", "youtube", "deezer", "itunes"]


def _handle_radio(update, context, fetch_track: Callable[[], Track], radio: Radio):
    update_message = update.message
    logging.info(f"Got '{update_message.text}' from {update_message.from_user.username} in {update_message.chat.title}")
    try:
        track = fetch_track()

        # Enrich with Spotify URL
        try:
            track = add_spotify_external_url(track)
        except Exception as e:
            logging.warning(f"Error enriching with Spotify: {e}")

        logging.info(f"Found this song live: {str(track)}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=track_to_markdown(track, radio=radio),
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True,
        )

        # Send a link with the music
        for provider in TRACK_PROVIDERS:
            if provider in track.external_urls:
                msg = f"Found this on {provider.title()} !\n\n{track.external_urls[provider]}"
                logging.info(msg.replace("\n", " "))
                context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
                return

        logging.info("No external urls found")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Not found on Spotify",
            parse_mode=ParseMode.MARKDOWN_V2,
        )

    except LiveUnavailableException:
        logging.info("No track information available right now")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=escape_markdown("No live song information right now, is it ", version=2)
            + "_Club Jazzafip_"
            + escape_markdown(" ?", version=2),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    except Exception as e:
        logging.error(e)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=escape_markdown(ERROR_MESSAGE, version=2),
            parse_mode=ParseMode.MARKDOWN_V2,
        )


def get_live(update, context):
    _handle_radio(update, context, lambda: execute_live_query("FIP"), FIP_RADIO)


def get_meuh(update, context):
    _handle_radio(update, context, lambda: RadioMeuh().get_current_track(), MEUH_RADIO)


def get_fiftyfifty(update, context):
    _handle_radio(update, context, lambda: Radio5050().get_current_track(), FIFTYFIFTY_RADIO)


def get_feelgood(update, context):
    _handle_radio(update, context, lambda: RadioFeelGood().get_current_track(), FEELGOOD_RADIO)
