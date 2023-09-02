import asyncio
import json
from FastApiCore.coreApi import dailyGetAnnouncementData
from PushSvc.api import dailyPushJob
from kafka import KafkaConsumer, consumer
from loguru import logger
import os
from pydantic import BaseModel
KAFKA_SERVER = os.environ['KAFKA_SERVER']
KAFKA_PORT = int(os.environ['KAFKA_PORT'])

# consumer 객체 생성
consumer = KafkaConsumer(
    'openDart',
    bootstrap_servers=[f'{KAFKA_SERVER}:{KAFKA_PORT}'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    consumer_timeout_ms=1000
)
async def consumerEventHandle():
    logger.debug("consumerEventHandle 시작")
    while True:
        await asyncio.sleep(1)
        for message in consumer:
            print(message.topic, message.partition, message.offset, message.key, message.value)
            msgValue = message.value.decode("utf-8")
            logger.debug(msgValue)
            await jsonParse(msgValue)

class KafkaTransferDTO:
    def __init__(self,json_str: dict):
        self.method = json_str['method']
        self.startDt = json_str['startDt']
        self.endDt = json_str['endDt']
        self.lastReportAt = json_str.get("lastReportAt")
        self.corpCls = json_str.get("corpCls")
async def jsonParse(msgValue: str):
    logger.debug(msgValue)
    try:
        msgValueDict = json.loads(msgValue,strict=False)
    except Exception as e:
        logger.debug(f"{e} json decode error 발생")
        return
    logger.debug(msgValueDict)
    try:
        await bindFunction(KafkaTransferDTO(msgValueDict))
    except Exception as e:
        logger.debug(f"{e}")
async def bindFunction(msgValue: KafkaTransferDTO):
    logger.debug(msgValue.method)
    if msgValue.method == "dailyPushJob":
        await dailyPushJob(msgValue.startDt,msgValue.endDt)
    if msgValue.method == "dailyGetAnnouncementData":
        await dailyGetAnnouncementData(msgValue.startDt,msgValue.endDt,msgValue.lastReportAt,msgValue.corpCls)