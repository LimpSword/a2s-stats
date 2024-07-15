from fastapi import APIRouter
from fastapi_cache.decorator import cache

import internal.a2s_calls as a2s_calls
import internal.servers.servers as servers

router = APIRouter()


@router.get("/api/v1/servers")
@cache(expire=10)
async def get_servers():
    servers_info = await servers.get_all_server_info()
    returned = {"servers": servers_info,
                "total_players": sum([server.players for _, server in servers_info.items()]),
                "max_players": sum([server.max_players for _, server in servers_info.items()])}
    return returned


@router.get("/api/v1/playercount/{ip}")
async def get_player_count(ip: str):
    count = await a2s_calls.get_player_count(ip.split(":")[0], int(ip.split(":")[1]))
    return {"player_count": count}
