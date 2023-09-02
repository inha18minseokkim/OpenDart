import asyncio

from fastapi import FastAPI
#from DBClient.databaseCmn import engineConn
from CmnUtl.DBClient import corpCodeRouter
from CmnUtl.DBClient.corpCmnAnn.corpCmnAnnMain import corpCmnAnnRouter
from FastApiCore.coreApi import coreRouter
from PushSvc.api import pushRouter
from PushSvc.member import memberRouter
from FastApiCore.frontApi import frontRouter
from KafkaConsumer import consumerEventHandle
from loguru import logger
import nest_asyncio
import threading
app = FastAPI()
nest_asyncio.apply()
#conn = engineConn()
#session = conn.sessionmaker()

app.include_router(corpCodeRouter)
app.include_router(corpCmnAnnRouter)
app.include_router(coreRouter)
app.include_router(coreRouter)
app.include_router(pushRouter)
app.include_router(memberRouter)
app.include_router(frontRouter)
#meta_data = MetaData(bind=conn,reflect=True)
#finServiceTable = meta_data.tables['TB_CORP_CODE']

@app.on_event("startup")
async def onStartUp():
    logger.debug("opendart 시작")
    threading.Thread(target= lambda : asyncio.run(consumerEventHandle())).start()


@app.get("/")
async def test():
    return "Server is in good condition"

@app.get("/raiseError")
async def raiseError():
    raise Exception
    return "Exit"