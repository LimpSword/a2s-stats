import time

import a2s.players
from a2s import SourceInfo, GoldSrcInfo

default_timeout = 10  # seconds
player_count_cache = {}
player_count_cache_timeout = {}


async def get_player_count(ip, port):
    if (ip, port) in player_count_cache and player_count_cache_timeout[(ip, port)] > time.time():
        return player_count_cache[(ip, port)]
    info: SourceInfo | GoldSrcInfo = await a2s.ainfo((ip, port))
    player_count_cache[(ip, port)] = info.player_count
    player_count_cache_timeout[(ip, port)] = time.time() + default_timeout
    return info.player_count
