import json
from loguru import logger
import sys
sys.path.append("../..") #상위 경로를 현재 경로에 넣어 declaration 파일 임포트 가능
sys.path.append("../")
from DBClient.corpCmnAnn import corpCmnAnnMain
from FastApiCore.declaration import dbUrl, sendDiscordMessage

class CmnEventPushSvcIntf:
    def __init__(self,msgInfo: dict):
        self.msgInfo = msgInfo
        self.classification = "일반"
        self.msgInfo['classification'] = self.classification
    def pushMessageLoad(self) -> str:
        logger.debug(self.msgInfo)
        corpName = self.msgInfo['corp_name']
        reportNm = self.msgInfo['report_nm']
        rceptDt = self.msgInfo['rcept_dt']
        rceptNo = self.msgInfo['rcept_no']
        self.msg = f"이벤트 발생 \n 회사명 : {corpName} \n 이벤트 : {reportNm} \n 발생일 : {rceptDt} \n접수번호 : {rceptNo}"
        logger.debug(self.msg)
        # 여기에 푸시 보내는 기능 적재예정
        #res = sendDiscordMessage(msg)
        #logger.debug("메세지 보냄 " + json.dumps(res))
        #self.saveDB(msgInfo)
        return self.msg
    async def saveDB(self):
        logger.debug(self.msgInfo)
        #res = requests.post(dbUrl + "/tb_corp_cmn_ann/insertCorpCmnAnn",json=msgInfo)
        res = corpCmnAnnMain.insertCorpCmnAnn(self.msgInfo)
        logger.debug(res)
        return res

