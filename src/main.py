import os

from interactions import Client, Intents, listen
from utils.env import get_env
from utils.logging import logger


class TorrentBot(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @listen()
    async def on_ready(self):
        self.load_extensions()
        logger.info("We're online!")
        logger.info("Bot is ready to use!")
        logger.info(f"We've logged in as {bot.app.name}")
        logger.info(f"This bot is owned by {bot.owner}")

    def load_extensions(self):
        for filename in os.listdir("./extensions"):
            if filename.endswith(".py") and filename != "__init__.py":
                try:
                    self.load_extension(f"extensions.{filename[:-3]}")
                    logger.info(f"Loaded extension: {filename[:-3]}")
                except Exception as e:
                    logger.error(f"Failed to load extension {filename[:-3]}: {e}")


bot = TorrentBot(
    intents=Intents.ALL,
    sync_interactions=True,
    # delete_unused_application_cmds=True,
    asyncio_debug=True,
    logger=logger,
)
bot.start(token=get_env("DISCORD_TOKEN"))
