from fastapi import APIRouter, Request
import sys,os

sys.path.append("../DBClient") #상위 경로를 현재 경로에 넣어 declaration 파일 임포트 가능

from pydantic import BaseModel
from loguru import logger
import pymongo
from DBClient.databaseCmn import conn

corpCmnAnnRouter = APIRouter(tags=['일반공시'])


db = conn.get_database("openDart")
coll = db.get_collection("tbCorpCmnAnn")
coll.create_index([("rcept_no",pymongo.ASCENDING)],unique=True)

@corpCmnAnnRouter.get("/tb_corp_cmn_ann/")
async def codeInfoMain():
    return "CommonAnnouncement runs successfully"

def insertCorpCmnAnn(json_str: dict):
    try:
        coll.insert_one(json_str)
    except Exception as e:
        logger.debug("삽입 중 오류 {e}", e=e, exc_info=True)
        return {'code' : 1}
    return {'code': 0}

async def selectCorpCmnAnnByDate(startDt: str, endDt: str):
    try:
        res = coll.find({"$and": [{"rcept_dt" : {"$gte":startDt}},{"rcept_dt" : {"$lte" : endDt}}]},{"_id":False})
        logger.debug(res)
        return list(res)
    except Exception as e:
        logger.debug("탐색 오류")
        return {'code' : 1}
