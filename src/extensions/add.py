from interactions import (
    Embed,
    Extension,
    OptionType,
    SlashContext,
    slash_command,
    slash_option,
)
from transmission_rpc import Client, TransmissionError
from utils.env import get_env
from utils.logging import logger


class Add(Extension):
    """Cog for adding torrents."""

    def __init__(self, bot: Client):
        self.bot = bot

    async def get_transmission_client(ctx: SlashContext) -> Client | None:
        """Gets the Transmission client, handling potential errors."""
        try:
            return Client(
                host=get_env("TRANSMISSION_HOST"),
                port=get_env("TRANSMISSION_PORT"),
                username=get_env("TRANSMISSION_USERNAME"),
                password=get_env("TRANSMISSION_PASSWORD"),
            )
        except TransmissionError as e:
            logger.error(f"TransmissionError: {e}")
            await ctx.send(
                "Error connecting to Transmission. Please check the settings and try again."
            )
        except Exception as e:
            logger.error(f"Unexpected error connecting to Transmission: {e}")
            await ctx.send(
                "An unexpected error occurred while connecting to Transmission. Please try again later."
            )
        return None  # Indicate failure by returning None

    @slash_command(
        name="torrents",
        description="Manage Transmission",
        scopes=[get_env("SERVER_ID")],
        sub_cmd_name="add",
        sub_cmd_description="Add torrents.",
    )
    @slash_option(
        name="url",
        description="URL of the torrent file or magnet link.",
        opt_type=OptionType.STRING,
        required=True,
    )
    @slash_option(
        name="destination",
        description="The directory where the torrent should be downloaded. (Optional)",
        opt_type=OptionType.STRING,
        required=False,
    )
    async def add(self, ctx: SlashContext, url: str, destination: str = None):
        logger.info("Add command received.")

        tc = await self.get_transmission_client()

        if tc is None:
            return  # Handle the error (connection failed)

        try:
            torrent = tc.add_torrent(url, download_dir=destination)

            embed = Embed(
                title=":white_check_mark: Torrent Added",
                description=f"**ID:** {torrent.id}\n" f"**Name:** {torrent.name}\n",
                color=0x2ECC71,
            )

            await ctx.send(embeds=embed)

        except TransmissionError as e:
            error_message = f":warning: Error adding torrent: {e}"
            await ctx.send(error_message)
            logger.error(error_message)
        except Exception as e:
            error_message = f"Oops, something went wrong: {e}"
            await ctx.message.reply(error_message)
            logger.error(error_message)


def setup(bot: Client):
    Add(bot)
