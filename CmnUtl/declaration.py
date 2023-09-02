import requests
from loguru import logger

crtfc_key = "bfb1272f4109ed5e959ff0b82b40bb08291ffb45"
dbUrl = "http://db-client-service.default.svc.cluster.local:8081"
pushUrl = "http://fastapi-push.util.svc.cluster.local:8084"#"http://fastapi-push.default.svc.cluster.local:8084"

async def sendMessage(txt: str):
    res = requests.get(pushUrl + f"/sendDiscordMessage/{txt}")
    logger.debug(res)
    if res.status_code == 200:
        return res.json()
    else:
        return {'code' : 1, 'status_code' : res.status_code}