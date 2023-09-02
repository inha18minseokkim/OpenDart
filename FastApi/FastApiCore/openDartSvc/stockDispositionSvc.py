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
class StockDispositionIntf(CmnEventPushSvcIntf):
    def __init__(self,msgInfo: dict):
        self.requestUrl = "https://opendart.fss.or.kr/api/piicDecsn.json"  # 자기주식 처분결정 api url
        self.msgInfo = msgInfo
        self.classification = "자기주식처분결정"
        self.msgInfo['classification'] = self.classification
    def pushMessageLoad(self) -> str:
        self.msg = f"자기주식 처분 결정 " \
                   f"\n회사 명 {self.msgInfo['corp_name']}" \
                   f"\n처분예저금액 {self.msgInfo['dppln_prc_ostk']}" \
                   f"\n처분예정기간 {self.msgInfo['dpprpd_bgd']} ~ {self.msgInfo['dpprpd_edd']}" \
                   f"\n처분목적 {self.msgInfo['dp_pp']}" \
                   f"\n처분방법 시장매도{self.msgInfo['dp_m_mkt']}주 시간외매도{self.msgInfo['dp_m_ovtm']}주"
        return self.msg