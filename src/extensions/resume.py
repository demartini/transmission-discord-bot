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
from utils.torrent_utils import validate_torrent_command


class Resume(Extension):
    """Cog for resuming paused torrents."""

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
        sub_cmd_name="resume",
        sub_cmd_description="Resume paused torrents.",
    )
    @slash_option(
        name="id",
        description="The ID of the torrent to resume",
        opt_type=OptionType.INTEGER,
        required=True,
    )
    async def resume(self, ctx: SlashContext, id: int):
        logger.info("Resume command received.")

        tc = await self.get_transmission_client()

        if tc is None:
            return  # Handle the error (connection failed)

        try:
            torrents = tc.get_torrents()
            error_embed = await validate_torrent_command(
                ctx, id, torrents, "downloading"
            )
            if error_embed:
                await ctx.send(embeds=error_embed)
                return

            tc.start_torrent(id)

            embed = Embed(
                title=":arrow_forward: Torrent Resumed",
                description=f"Torrent with ID {id} resumed.",
                color=0xF1C40F,
            )

            await ctx.send(embeds=embed)

        except TransmissionError as e:
            error_message = f":warning: Error resuming torrent with ID {id}: {e}"
            await ctx.send(error_message)
            logger.error(error_message)
        except Exception as e:
            error_message = f"Oops, something went wrong: {e}"
            await ctx.message.reply(error_message)
            logger.error(error_message)


def setup(bot: Client):
    Resume(bot)
