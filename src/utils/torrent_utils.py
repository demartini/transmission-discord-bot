from interactions import Embed
from transmission_rpc import Torrent


async def validate_torrent_command(
    ctx, id: int, torrents: list[Torrent], target_status: str
) -> Embed | None:
    """Handle common functionality for torrent commands."""

    # Check if torrent ID is provided
    if not id:
        return Embed(
            title=":warning: Missing Torrent ID",
            description="Please provide the ID of the torrent you want to process.",
            color=0xF1C40F,
        )

    # Check if the provided ID is a positive integer
    if not isinstance(id, int) or id <= 0:
        return Embed(
            title=":warning: Invalid Torrent ID",
            description="Please provide a positive integer.",
            color=0xF1C40F,
        )

    # Check if there are no active torrents
    if not torrents:
        return Embed(
            title=":warning: No Torrents Found",
            description="No active torrents found.",
            color=0xF1C40F,
        )

    # Check if the provided ID exists in the list of torrents
    ids = [torrent.id for torrent in torrents]
    if id not in ids:
        return Embed(
            title=":warning: Invalid Torrent ID",
            description="This torrent does not exist.",
            color=0xF1C40F,
        )

    # Check if the torrent is already in the desired state
    torrent = next((t for t in torrents if t.id == id), None)
    if torrent.status == target_status:
        return Embed(
            title=":ballot_box_with_check: Torrent is already in the desired state.",
            description=f"Torrent with ID {id} is already {target_status}.",
            color=0x3498DB,
        )

    return None  # Return None if validation passes
