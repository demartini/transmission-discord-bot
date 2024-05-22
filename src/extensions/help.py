from interactions import Client, Embed, Extension, SlashContext, slash_command
from utils.env import get_env
from utils.logging import logger


class Help(Extension):
    """Provides help information about the bot's commands."""

    def __init__(self, bot: Client):
        self.bot = bot
        self.bot_name = bot.app.name

    @slash_command(
        name="torrents",
        description="Manage Transmission",
        scopes=[get_env("SERVER_ID")],
        sub_cmd_name="help",
        sub_cmd_description="Get help about available commands.",
    )
    async def help(self, ctx: SlashContext):
        logger.info("Help command received.")

        bot_name = self.bot_name

        embed = Embed(
            title=f"🤖 {bot_name} Help",
            description=f"Welcome to the {bot_name}! Here's a list of available commands:",
            color=0x11806A,
        )

        embed.add_field(
            name="/torrents add",
            value="Add a new torrent.\n**Options**:\n- `url` (required): Torrent file URL or magnet link.\n- `destination` (optional): Directory to save the torrent.",
            inline=False,
        )

        embed.add_field(
            name="/torrents list",
            value="List active torrents.",
            inline=False,
        )

        embed.add_field(
            name="/torrents pause",
            value="Pause an active torrent.\n**Options**:\n - `id` (required): ID of the torrent to pause.",
            inline=False,
        )

        embed.add_field(
            name="/torrents remove",
            value="Remove a torrent.\n**Options**:\n - `id` (required): ID of the torrent to remove.",
            inline=False,
        )

        embed.add_field(
            name="/torrents resume",
            value="Resume a paused torrent.\n**Options**:\n - `id` (required): ID of the torrent to resume.",
            inline=False,
        )

        embed.add_field(
            name="/torrents help",
            value="Show this help message.",
            inline=False,
        )

        await ctx.send(embeds=embed)


def setup(bot):
    Help(bot)
