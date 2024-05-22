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


class Remove(Extension):
    """Cog for removing torrents."""

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
        sub_cmd_name="remove",
        sub_cmd_description="Remove torrents.",
    )
    @slash_option(
        name="id",
        description="The ID of the torrent to remove",
        opt_type=OptionType.INTEGER,
        required=True,
    )
    async def remove(self, ctx: SlashContext, id: int):
        logger.info("Remove command received.")

        tc = await self.get_transmission_client()

        if tc is None:
            return  # Handle the error (connection failed)

        try:
            tc.remove_torrent(id, delete_data=True)

            embed = Embed(
                title=":wastebasket: Torrent Removed",
                description=f"Torrent with ID {id} removed.",
                color=0x9B59B6,
            )

            await ctx.send(embeds=embed)

        except TransmissionError as e:
            error_message = f":warning: Error removing torrent: {e}"
            await ctx.send(error_message)
            logger.error(error_message)
        except Exception as e:
            error_message = f"Oops, something went wrong: {e}"
            await ctx.message.reply(error_message)
            logger.error(error_message)


def setup(bot: Client):
    Remove(bot)
