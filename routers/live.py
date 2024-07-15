from fastapi import APIRouter
import internal.a2s_calls as a2s_calls
import internal.servers.servers as servers

router = APIRouter()


@router.get("/api/v1/servers")
async def get_servers():
    await servers.refresh_servers()
    return servers.get_all_server_info()


@router.get("/api/v1/playercount/{ip}")
async def get_player_count(ip: str):
    count = await a2s_calls.get_player_count(ip.split(":")[0], int(ip.split(":")[1]))
    return {"player_count": count}
