from fastapi import FastAPI
import internal.a2s_calls as a2s_calls

app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/api/v1/playercount/{ip}")
async def get_player_count(ip: str):
    count = await a2s_calls.get_player_count(ip.split(":")[0], int(ip.split(":")[1]))
    return {"player_count": count}
