import sys
from fastapi import APIRouter
from pydantic import BaseModel
from loguru import logger
import pymongo
sys.path.append("..")
from DBClient.databaseCmn import conn
db = conn.get_database("openDart")
coll = db.get_collection("tbMember")
coll.create_index([("telegramId",pymongo.ASCENDING)],unique=True)
memberRouter = APIRouter(tags=["member"])


class Memberinfo(BaseModel):
    telegramId: str
    pushYN: str
    corpList: list

@memberRouter.post("/setMember")
async def setMember(body: Memberinfo):
    try:
        res = coll.find_one({"telegramId" : body.telegramId})
        if res == None:
            coll.insert_one({"telegramId":body.telegramId, "pushYN" : body.pushYN, "corpList" : body.corpList})
        else:
            logger.debug(body.dict())
            coll.update_one(filter={"telegramId" : body.telegramId}, update={"$set":{"pushYN" : body.pushYN, "corpList" : body.corpList}})
    except Exception as e:
        logger.debug(f"{e}")
        return {'code' : 1, 'Msg' : f"{e}"}
    return body.json()

class appendPopCorpInfoBody(BaseModel):
    telegramId: str
    targetList: list

@memberRouter.post("/appendCorpInfo")
async def appendCorpInfo(body: appendPopCorpInfoBody):
    res = coll.find_one({"telegramId" : body.telegramId},{'_id':0})
    if res == None:
        return {'code' : 1, 'msg' : '대상 사용자 없음'}
    logger.debug(body.dict())
    originalList = res['corpList']
    for ele in body.targetList:
        if ele in originalList: continue
        originalList.append(ele)
    coll.update_one(filter={"telegramId": body.telegramId},
                    update={"$set": {"corpList": originalList}})
    return {'code' : 0, 'telegramId' : body.telegramId , 'corpList' : originalList}

def isIn(ele,li):
    for i in li:
        logger.debug(f"{ele} {i}")
        if i == ele: return True
    return False

@memberRouter.post("/popCorpInfo")
async def popCorpInfo(body: appendPopCorpInfoBody):
    res = coll.find_one({"telegramId": body.telegramId}, {'_id': 0})
    if res == None:
        return {'code': 1, 'msg': '대상 사용자 없음'}
    logger.debug(body.dict())
    originalList = res['corpList']
    newList = []
    for ele in originalList:
        if isIn(ele,body.targetList): continue
        newList.append(ele)
    coll.update_one(filter={"telegramId": body.telegramId},
                    update={"$set": {"corpList": newList}})
    return {'code': 0, 'telegramId': body.telegramId, 'corpList': originalList}