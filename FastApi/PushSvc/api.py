from fastapi import APIRouter
from loguru import logger
import sys
import nest_asyncio
sys.path.append("..")
from KafkaProducer import sendKafkaMessage
from FastApiCore.openDartSvc.openDartAnnouncementSelector import openDartEventFactory
from DBClient.databaseCmn import conn
db = conn.get_database("openDart")
tbMembercoll = db.get_collection("tbMember")
tbCorpCmnAnn = db.get_collection("tbCorpCmnAnn")
nest_asyncio.apply()
pushRouter = APIRouter(tags=["Push"])

@pushRouter.get("/dailyPushJob")
async def dailyPushJob(startDt: str, endDt: str):
    #푸시대상 탐색
    userRes = list(tbMembercoll.find({"pushYN" : "Y"}))
    #리스트 받았으면 각각 유저에 해당하는 공시내용 뒤져서 푸시 보내기
    for ele in userRes:
        logger.debug(ele)
        tmpCorpList = ele['corpList']
        msgList = list(tbCorpCmnAnn.find({"$and" : [{"corp_code" : {"$in" : tmpCorpList}},
        {"rcept_dt" : {"$gte":startDt}},{"rcept_dt":{"$lte":endDt}}]},{'_id':0}))
        for i in msgList:
            targetObj = openDartEventFactory(i)
            msg = targetObj.pushMessageLoad()
            logger.debug(msg)
            #await sendMessage(msg)
            await sendKafkaMessage("push",{"method":"sendMessage","msg" : msg + "\nkafka발송"})
        if len(msgList) == 0:
            #await sendMessage(f"{startDt} ~ {endDt} 해당종목정보 없음")
            await sendKafkaMessage("push",{"method":"sendMessage","msg":f"{startDt} ~ {endDt} 해당종목정보 없음 \nkafka발송"})
    return {'code' : 0}



