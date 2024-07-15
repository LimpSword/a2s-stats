import logging
import time

import a2s.players
from a2s import SourceInfo, GoldSrcInfo

default_timeout = 10  # seconds

player_count_cache = {}
player_count_cache_timeout = {}

logger = logging.getLogger("uvicorn.error")


async def get_player_count(ip, port, cache=True) -> int:
    """
    Get player count
    :param ip:
    :param port:
    :param cache:
    :return: player count
    """
    if cache and (ip, port) in player_count_cache and player_count_cache_timeout[(ip, port)] > time.time():
        return player_count_cache[(ip, port)]
    info: SourceInfo | GoldSrcInfo = await a2s.ainfo((ip, port))
    if cache:
        player_count_cache[(ip, port)] = info.player_count
        player_count_cache_timeout[(ip, port)] = time.time() + default_timeout
    return info.player_count


# TODO: cache this
async def get_info(ip, port) -> tuple[int, int, str]:
    """
    Get server info
    :param ip:
    :param port:
    :return: player count, max_players, map
    """
    try:
        info = await a2s.ainfo((ip, port))
    except Exception as e:
        logger.error(f"Failed to get server info for {ip}:{port}. Got {e}")
        return -1, -1, "Unknown"
    return info.player_count, info.max_players, info.map_name
