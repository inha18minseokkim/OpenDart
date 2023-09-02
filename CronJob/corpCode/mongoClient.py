from fastapi import Request
import sys,os


sys.path.append("../DBClient") #상위 경로를 현재 경로에 넣어 declaration 파일 임포트 가능
sys.path.append("../..")
sys.path.append(".")

from pydantic import BaseModel
from loguru import logger
import pymongo
from DBClient.databaseCmn import conn
logger.debug(sys.path)

db = conn.get_database("openDart")
coll = db.get_collection("tbCorpCode")
coll.create_index([("corp_code",pymongo.ASCENDING)],unique=True)

class RequestBody():
    corp_code: int
    corp_name: str
    stock_code: str
    modify_date: str

async def insertCorpInfo(body: RequestBody):
    res = {}
    print(body.corp_code)
    res["corp_code"] = body.corp_code
    res["corp_name"] = body.corp_name
    res["stock_code"] = body.stock_code
    res["modify_date"] = body.modify_date
    logger.debug(body.corp_code)
    logger.debug(body.modify_date)
    try:
        coll.insert_one(res)
    except:
        return {"code": 1}
    return {"code" : 0}
async def updateCorpInfo(body: RequestBody):
    logger.debug("수정중")
    try:
        coll.update_one({"corpCode": body.corp_code},body.dict())
        logger.debug("수정완료")
    except:
        return {"code" : 1}
    return {"code" : 0}

def insertOrUpdateCorpInfoArr(body: list):
    if len(body) == 0:
        logger.debug("비어있으므로 종료")
        return {'code' : 0}
    #session = conn.sessionmaker()
    logger.debug(body)
    coll.insert_many(body)
    return {'code' : 0}
