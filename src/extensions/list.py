from interactions import Embed, Extension, SlashContext, slash_command
from transmission_rpc import Client, TransmissionError
from utils.env import get_env
from utils.logging import logger


class List(Extension):
    """Cog for listing active torrents."""

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
        sub_cmd_name="list",
        sub_cmd_description="Listing torrents.",
    )
    async def list(self, ctx: SlashContext):
        logger.info("List command received.")

        tc = await self.get_transmission_client()

        if tc is None:
            await ctx.send(
                "Error connecting to Transmission. Please check the settings and try again."
            )
            return  # Handle the error (connection failed)

        try:
            torrents = tc.get_torrents()

            no_torrents = Embed(
                title=":man_shrugging: No Torrents Found",
                description="No active torrents found.",
                color=0xF1C40F,
            )

            if not torrents:
                await ctx.send(embeds=no_torrents)
                return

            embed = Embed(
                title="Active Torrents",
                color=0x3498DB,
            )

            for torrent in torrents:
                progress = f"{torrent.percent_done:.1f}%"
                status_emoji = (
                    ":arrow_down:"
                    if torrent.status == "downloading"
                    else ":pause_button:"
                )
                embed.add_field(
                    name=f"{status_emoji} ID: {torrent.id}",
                    value=f"**Name**: {torrent.name}\n**Status**: {torrent.status}\n**Progress**: {progress}",
                    inline=False,
                )

            await ctx.send(embeds=embed)

        except TransmissionError as e:
            error_message = f":warning: Error retrieving torrents: {e}"
            await ctx.send(error_message)
            logger.error(error_message)
        except Exception as e:
            error_message = f"Oops, something went wrong: {e}"
            await ctx.message.reply(error_message)
            logger.error(error_message)


def setup(bot: Client):
    List(bot)
