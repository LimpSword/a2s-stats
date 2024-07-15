import json
import logging
import time
from config import get_settings

import requests

from internal import a2s_calls

servers_file_type = get_settings().servers_file_type
servers_file_url = get_settings().servers_file_url

cached_servers: dict = {}
cached_serverinfo: dict = {}

logger = logging.getLogger("uvicorn.error")


class ServerInfo:
    def __init__(self, name, ip, map, players, max_players, tags, timestamp):
        self.name = name
        self.ip = ip
        self.map = map
        self.players = players
        self.max_players = max_players
        self.tags = tags
        self.timestamp = timestamp

    def __str__(self):
        return f"{self.name} ({self.ip}) - {self.players}/{self.max_players} players on {self.map} ({self.tags})"


def _load_servers():
    global cached_servers
    if servers_file_type == "none":
        return
    if servers_file_type == "file":
        if servers_file_url == "":
            logger.error("No server file URL provided")
            return

        try:
            with open(servers_file_url, "r") as f:
                cached_servers = f.read()
                extracted_dict = json.loads(cached_servers)

                # Filter for only numeric keys
                numeric_keys = [k for k in extracted_dict.keys() if k.isnumeric()]
                extracted_dict = {k: extracted_dict[k] for k in numeric_keys}

                cached_servers = extracted_dict
        except FileNotFoundError:
            logger.error("Server file not found")
    elif servers_file_type == "url":
        if servers_file_url == "":
            logger.error("No server file URL provided")
            return

        jsonResponse = requests.get(servers_file_url).text
        extracted_dict = json.loads(jsonResponse)

        # Filter for only numeric keys
        numeric_keys = [k for k in extracted_dict.keys() if k.isnumeric()]
        extracted_dict = {k: extracted_dict[k] for k in numeric_keys}

        cached_servers = extracted_dict
    else:
        logger.error("Invalid server file type")


def get_servers():
    if cached_servers is None or len(cached_servers) == 0:
        _load_servers()
    return cached_servers


def get_all_server_info():
    return cached_serverinfo


async def refresh_servers():
    servers = get_servers()
    for server in servers:
        server = servers[server]

        ip = server["ip"]
        name = server["name"]
        players, max_players, map = await a2s_calls.get_info(ip.split(":")[0], int(ip.split(":")[1]))
        timestamp = time.time_ns() // 1000000
        tags = server.get("tags", [])
        cached_serverinfo[ip] = ServerInfo(name, ip, map, players, max_players, tags, timestamp)


_load_servers()
