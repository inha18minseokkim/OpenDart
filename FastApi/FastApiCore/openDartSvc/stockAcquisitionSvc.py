import json
import sys,os
sys.path.append("../..") #상위 경로를 현재 경로에 넣어 declaration 파일 임포트 가능
sys.path.append("../../../CmnUtl/DBClient")
sys.path.append("..")
from FastApiCore.declaration import crtfc_key, dbUrl, sendDiscordMessage
from .eventPushSvcIntf import CmnEventPushSvcIntf
'''
사용 파라미터 : 회사코드, 날짜
주요 내용 조립해서 푸시 서버에 보내줌
서버에서 한번 보내줌
'''
#자기주식 처분 결정
import requests
from loguru import logger
class StockAcquisitionIntf(CmnEventPushSvcIntf):
    def __init__(self,msgInfo: dict):
        self.requestUrl = "https://opendart.fss.or.kr/api/piicDecsn.json"  # 자기주식 취득결정 api url
        self.msgInfo = msgInfo
        self.classification = "자기주식취득결정"
        self.msgInfo['classification'] = self.classification
    def pushMessageLoad(self) -> str:
        self.msg = f"자기주식취득결정" \
                   f"\n회사명 {self.msgInfo['corp_name']}" \
                   f"\n취득예정금액(보통) {self.msgInfo['aqpln_stk_ostk']}" \
                   f"\n취득목적 {self.msgInfo['aq_pp']}" \
                   f"\n취득방법 {self.msgInfo['aq_mth']}" \
                   f"\n취득결정일 {self.msgInfo['aq_dd']}"
        return self.msg

