from fastapi import FastAPI, APIRouter
import requests

from loguru import logger
import sys
import asyncio
sys.path.append('../..') #부모 디렉터리 강제로 import 안하면 안됨 왜??????
sys.path.append("..")
from .batRes import initCodeRoutine
from .mainSvc import openDartAnnouncementSvc
from .declaration import dbUrl
from KafkaProducer import sendKafkaMessage
coreRouter = APIRouter()

@coreRouter.get("/")
def helloWorld():
    return {"Hello" : "World"}

@coreRouter.on_event("startup")
def onStartUp():
    logger.debug("start")


@coreRouter.get("/passiveRoutine/initCodeRoutine", tags=["needs to be scheduled"])
async def execInitCodeRoutine():
    await initCodeRoutine.initCode()
    return "Finished"

@coreRouter.get("/getAnnounceInfo",tags=["needs to be scheduled"])
async def getAnnounceInfo(corpCode: str,startDt: str,endDt: str, pblntfTy: str):
    logger.debug(f"{corpCode} {startDt} {endDt} {pblntfTy}")
    res = await openDartAnnouncementSvc.getAnnounceInfo(corpCode, startDt, endDt, pblntfTy)
    if res is None: return {'list' : []}
    return res
@coreRouter.get("/dailyGetAnnouncementData",tags=["needs to be scheduled"])
async def dailyGetAnnouncementData(startDt:str,endDt:str,lastReportAt:str = "Y",corpCls:str = "Y"):
    logger.debug("모든 종목에 대해 수행")
    try:
        res = await openDartAnnouncementSvc.getAnnounceInfoByDay(startDt,endDt,lastReportAt,corpCls)
        await sendKafkaMessage("push", {"method" : "sendMessage","botIdx" : 2 ,
                                        "msg" : f"{startDt} ~ {endDt} 데이터 정상 수신 완료"})
    except Exception as e :
        logger.debug(f"{e}")
        errorMsg = "내용 없음"
        await sendKafkaMessage("push", {"method" : "sendMessage","botIdx" : 2 ,
                                        "msg" : f'{startDt} ~ {endDt} 데이터 수신 중 오류'})
        await sendKafkaMessage("push", {"method": "sendMessage", "botIdx": 2,
                                        "msg": errorMsg})
        return {'code' : 1, 'msg' : e}
    return {'code' : 0, 'length' : len(res)}


