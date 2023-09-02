import re
import sys, os

import requests

sys.path.append(".")
sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")
print(sys.path)
print(os.getcwd())
from loguru import logger
from opendart.declaration import crtfc_key
from .stockDispositionSvc import StockDispositionIntf
from .paidIncreaseSvc import PaidIncreaseIntf
from .eventPushSvcIntf import CmnEventPushSvcIntf
from .stockAcquisitionSvc import StockAcquisitionIntf
from .freeIssueSvc import FreeIssueIntf
from .potatoSvc import potatoIntf
from .convertibleBondSvc import ConvertibleBondIntf
from .bondWithWarrentSvc import BondWithWarrantIntf
def eventFactoryFromDB(msgInfo: dict) -> CmnEventPushSvcIntf:
    classification = msgInfo['classification']
    if classification == '유상증자결정':
        return PaidIncreaseIntf(msgInfo)
    else:
        return CmnEventPushSvcIntf(msgInfo)

def createClassFactory(url: str,clsType: CmnEventPushSvcIntf,msgInfo: dict):
    corpName = msgInfo['corp_name']
    rceptDt = msgInfo['rcept_dt']
    reportNm = msgInfo['report_nm']
    corpCode = msgInfo['corp_code']
    requestUrl = url
    param = {"crtfc_key": crtfc_key, "corp_code": corpCode, "bgn_de": rceptDt, "end_de": rceptDt}
    logger.debug(msgInfo)
    res = requests.get(requestUrl, params=param)
    if res.status_code != 200:
        logger.debug("요청 중 오류 발생" + res.status_code)
        return CmnEventPushSvcIntf(msgInfo)
    res = res.json()
    if res['status'] == '013':
        logger.debug("아무 이벤트 없음")
        return CmnEventPushSvcIntf(msgInfo)
    if res['status'] != '000':
        logger.debug("오류 발생")
        raise Exception
    res = res['list'][0]
    res['corp_name'] = corpName
    res['report_nm'] = reportNm
    res['rcept_dt'] = rceptDt
    return clsType(res)
    
def eventFactoryFromApi(msgInfo: dict) -> CmnEventPushSvcIntf:
    corpName = msgInfo['corp_name']
    rceptDt = msgInfo['rcept_dt']
    reportNm = msgInfo['report_nm']
    corpCode = msgInfo['corp_code']
    if re.search('.*유상증자.*', reportNm):
        logger.debug(f'****** {corpName} {reportNm} {rceptDt} 유상증자 결정 팩토리 메서드 실행')
        targetUrl = "https://opendart.fss.or.kr/api/piicDecsn.json"
        return createClassFactory(targetUrl,PaidIncreaseIntf,msgInfo)
    
    if re.search('.*무상증자.*', reportNm) and re.search('.*주요사항.*', reportNm):
        logger.debug(f'****** {corpName} {reportNm} {rceptDt} 무상증자 결정 팩토리 메서드 실행')
        requestUrl = "https://opendart.fss.or.kr/api/fricDecsn.json"
        return createClassFactory(requestUrl,FreeIssueIntf,msgInfo)
    
    if re.search('.*자기주식처분.*', reportNm) and re.search('.*주요사항.*', reportNm):
        logger.debug(f'****** {corpName} {rceptDt} 자기주식처분 결정 팩토리 메서드 실행')
        requestUrl = "https://opendart.fss.or.kr/api/tsstkDpDecsn.json"
        return createClassFactory(requestUrl,StockDispositionIntf,msgInfo)
    
    if re.search('.*자기주식취득.*', reportNm) and re.search('.*주요사항.*', reportNm):
        logger.debug(f'****** {corpName} {rceptDt} 자기주식취득 결정 팩토리 메서드 실행')
        requestUrl = "https://opendart.fss.or.kr/api/tsstkAqDecsn.json"
        return createClassFactory(requestUrl,StockAcquisitionIntf,msgInfo)
    
    if re.search('.*감자.*', reportNm) and re.search('.*주요사항.*', reportNm):
        logger.debug(f'****** {corpName} {rceptDt} 감자 결정 팩토리 메서드 실행')
        requestUrl = "https://opendart.fss.or.kr/api/crDecsn.json"
        return createClassFactory(requestUrl,potatoIntf,msgInfo)
    
    if re.search('.*전환사채.*', reportNm) and re.search('.*주요사항.*', reportNm):
        logger.debug(f'****** {corpName} {rceptDt} 전환사채권발행 결정 팩토리 메서드 실행')
        requestUrl = "https://opendart.fss.or.kr/api/cvbdIsDecsn.json"
        return createClassFactory(requestUrl,ConvertibleBondIntf,msgInfo)

    if re.search('.*신주인수권.*', reportNm) and re.search('.*주요사항.*', reportNm):
        logger.debug(f'****** {corpName} {rceptDt} 신주인수권부사채권발행 결정 팩토리 메서드 실행')
        requestUrl = "https://opendart.fss.or.kr/api/bdwtIsDecsn.json"
        return createClassFactory(requestUrl,BondWithWarrantIntf,msgInfo)

    logger.debug(f'{corpName} {rceptDt} 기타 사항')
    return CmnEventPushSvcIntf(msgInfo)
    
def openDartEventFactory(msgInfo: dict) -> CmnEventPushSvcIntf:
    try:
        logger.debug(msgInfo)
        msgInfo['classification']
        logger.debug("ASDF")
        return eventFactoryFromDB(msgInfo)
    except:
        return eventFactoryFromApi(msgInfo)
    
