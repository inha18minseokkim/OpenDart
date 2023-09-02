import sys

sys.path.append("../..")
sys.path.append("..") #상위 경로를 현재 경로에 넣어 declaration 파일 임포트 가능
sys.path.append(".")
from declaration import crtfc_key
from KafkaProducer import sendKafkaMessage
import requests
from dataCollect.openDartSvc.openDartAnnouncementSelector import openDartEventFactory
from loguru import logger

url = "https://opendart.fss.or.kr/api/list.json"

async def getAnnounceInfoByDay(startDt,endDt,lastReportAt,corpCls):
    logger.debug(f"날짜별 공시검색 시작{startDt} ~ {endDt}")
    msg = []
    param = {
        'crtfc_key': crtfc_key,
        'bgn_de': startDt,
        'end_de': endDt,
        'last_report_at' : lastReportAt,
        'corp_cls' : corpCls,
        'page_no' : 1
    }
    while True:
        logger.debug(f"{param['page_no']} 번째 호출")
        #logger.debug(param)
        res = requests.get(url,params=param)
        #logger.debug(res.status_code)
        if res.status_code != 200: break
        res = res.json()
        #logger.debug(res)
        try:
            totalPage = int(res['total_page'])
            logger.info(f"TotalPage {totalPage}")
        except:
            logger.info("영업일 아니라 TotalPage 없음")
            totalPage = 0
            return
        for i in res['list']:
            corpName = i['corp_name']
            reportNm = i['report_nm']
            rceptDt = i['rcept_dt']
            rceptNo = i['rcept_no']
            corpCode = i['corp_code']
            logger.debug(f"{corpName}, {reportNm}, {rceptDt}")
            eventCallDict = {"corp_name": corpName, "report_nm": reportNm, "rcept_dt": rceptDt, "corp_code": corpCode,
                             "rcept_no": rceptNo}
            msg.append(eventCallDict)
            targetObj = openDartEventFactory(eventCallDict)  # 해당하는 이벤트가 있는지 탐색하고 후속 조치 수행
            res: dict = await targetObj.saveDB()
            if res['code'] == 1:
                logger.debug("이미 있는 이벤트")
            else:
                logger.debug(targetObj.pushMessageLoad())
                logger.debug("메세지 발송")
                await sendKafkaMessage("push", {"method": "sendMessage", "msg": targetObj.pushMessageLoad() + "\nkafka발송"})
        if param['page_no'] >= totalPage: break
        else: param['page_no'] += 1
    return msg
