import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from loguru import logger
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore

from whats_on_fip.deezer import add_deezer_external_url
from whats_on_fip.models import FIP_RADIO, MEUH_RADIO
from whats_on_fip.radio_france_api import LiveUnavailableException, execute_live_query
from whats_on_fip.radio_meuh_api import RadioMeuh
from whats_on_fip.slack.fmt import get_blocks, get_text

load_dotenv()

oauth_settings = OAuthSettings(
    client_id=os.environ.get("SLACK_CLIENT_ID"),
    client_secret=os.environ.get("SLACK_CLIENT_SECRET"),
    scopes=["commands", "chat:write"],
    installation_store=FileInstallationStore(base_dir="./data"),
    state_store=FileOAuthStateStore(expiration_seconds=600, base_dir="./data"),
    install_page_rendering_enabled=False,
)

slack_app = App(
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    oauth_settings=oauth_settings,
)
app_handler = SlackRequestHandler(slack_app)


@slack_app.command("/whatsonfip")
def message_live(ack, say, command):
    logger.info(
        f"Received /whatsonfip command from {command['user_name']} "
        f"in {command['channel_name']} - {command['team_domain']}"
    )
    ack()
    try:
        track = execute_live_query("FIP")
        try:
            track = add_deezer_external_url(track)
        except Exception as e:
            logger.warning(f"Error enriching with Deezer: {e}")
    except LiveUnavailableException:
        say(text="No live song information right now, is it _Club Jazzafip_ ?")
    else:
        logger.debug(f"Fetched from FIP API: {track}")
        blocks = get_blocks(track, FIP_RADIO, command["user_id"])
        text = get_text(track)
        say(blocks=blocks, text=text)


@slack_app.command("/meuh")
def message_meuh(ack, say, command):
    logger.info(
        f"Received /meuh command from {command['user_name']} in {command['channel_name']} - {command['team_domain']}"
    )
    ack()
    track = RadioMeuh().get_current_track()
    try:
        track = add_deezer_external_url(track)
    except Exception as e:
        logger.warning(f"Error enriching with Deezer: {e}")
    logger.debug(f"Fetched from Meuh API: {track}")
    blocks = get_blocks(track, MEUH_RADIO, command["user_id"])
    text = get_text(track)
    say(blocks=blocks, text=text)


api = FastAPI()


@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)


@api.get("/slack/install")
async def install(req: Request):
    return await app_handler.handle(req)


@api.get("/slack/oauth_redirect")
async def oauth_redirect(req: Request):
    return await app_handler.handle(req)


@api.get("/health")
async def get_health():
    return {"message": "OK"}
