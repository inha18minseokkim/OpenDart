from fastapi import APIRouter, Request
import sys,os


sys.path.append("../DBClient") #상위 경로를 현재 경로에 넣어 declaration 파일 임포트 가능
sys.path.append("../..")
sys.path.append(".")

from .models import corpInfo
from pydantic import BaseModel
from loguru import logger
import pymongo
from DBClient.databaseCmn import conn


db = conn.get_database("openDart")
coll = db.get_collection("tbCorpCode")
coll.create_index([("corp_code",pymongo.ASCENDING)],unique=True)

corpCodeRouter = APIRouter(tags=['기업코드정보'])



@corpCodeRouter.get("/tb_corp_code/")
async def codeInfoMain():
    return "codeInfo runs successfully"


@corpCodeRouter.get("/tb_corp_code/selectCorpInfo")
async def selectCorpInfo(corp_code: str):
    res = coll.find_one({"corpCode":corp_code})
    if res == None: return {'code' : 1}
    return res


class RequestBody(BaseModel):
    corp_code: int
    corp_name: str
    stock_code: str
    modify_date: str

@corpCodeRouter.post("/tb_corp_code/insertCorpInfo")
async def insertCorpInfo(body: RequestBody):
    res = {}
    print(body.corp_code)
    res["corp_code"] = body.corp_code
    res["corp_name"] = body.corp_name
    res["stock_code"] = body.stock_code
    res["modify_date"] = body.modify_date
    try:
        coll.insert_one(res)
    except:
        return {"code": 1}
    return {"code" : 0}

@corpCodeRouter.post("/tb_corp_code/updateCorpInfo")
async def updateCorpInfo(body: RequestBody):
    logger.debug("수정중")
    try:
        coll.update_one({"corpCode": body.corp_code},body.dict())
        logger.debug("수정완료")
    except:
        return {"code" : 1}
    return {"code" : 0}

#@corpCodeRouter.post("/tb_corp_code/insertOrUpdateCorpInfoArr")
def insertOrUpdateCorpInfoArr(body: list):
    if len(body) == 0:
        logger.debug("비어있으므로 종료")
        return {'code' : 0}
    #session = conn.sessionmaker()
    logger.debug(body)
    coll.insert_many(body)
    return {'code' : 0}

@corpCodeRouter.get("/tb_corp_code/getCorpStockCodeByName/{corpName}")
async def getCorpStockCodeByName(corpName: str):
    res = coll.find_one({"corp_name" : corpName})
    if res == None: return {"code" : 1}
    return res['corp_code']